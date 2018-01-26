import sys
import os
import time
import datetime

import cv2
import base64
import imutils
import dlib
import arrow
import numpy as np
from scipy.spatial import distance
from socketIO_client import SocketIO, LoggingNamespace

import inception_resnet_v1
import tensorflow as tf
from imutils.face_utils import FaceAligner

from logger import Logger
from face_session import FaceSession
from face import Face
from storage import Storage

def draw_label(image, point, label, font=cv2.FONT_HERSHEY_SIMPLEX,
               font_scale=1, thickness=2):
    size = cv2.getTextSize(label, font, font_scale, thickness)[0]
    x, y = point
    cv2.rectangle(image, (x, y - size[1]), (x + size[0], y), (255, 0, 0), cv2.FILLED)
    cv2.putText(image, label, point, font, font_scale, (255, 255, 255), thickness)

def main(sess,age,gender,train_mode,images_pl):
    LOCAL_MODE = os.getenv('LOCAL_MODE', 'True') == 'True'
    TIME_BETWEEN_READS = float(os.getenv('TIME_BETWEEN_READS', .3))
    TIME_BETWEEN_DEMO = float(os.getenv('TIME_BETWEEN_DEMO', .5))
    LIVE_VIDEO =  os.getenv('LIVE_VIDEO', 'True') == 'True'
    REMOVE_USER_TIMEOUT_SECONDS = int(
        os.getenv('REMOVE_USER_TIMEOUT_SECONDS', 60))  # seconds
    FACE_MATCH = .5

    Logger.log('running in Local mode: {}'.format(LOCAL_MODE))

    # if not LOCAL_MODE:
    socketIO = SocketIO('localhost', 3001, LoggingNamespace)
    Logger.log("Connected to socket.io")

    Logger.log("LIVE_VIDEO: {}".format(LIVE_VIDEO))

    camera_port = 0
    if not LOCAL_MODE:
        camera_port = -1

    # capture video
    cap = cv2.VideoCapture(camera_port)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # for face detection
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("dlib/shape_predictor_68_face_landmarks.dat")
    fa = FaceAligner(predictor, desiredFaceWidth=160)
    faceRecog = dlib.face_recognition_model_v1(
        'dlib/dlib_face_recognition_resnet_model_v1.dat')

    if LOCAL_MODE:
        Logger.log('opening window...')
        win = dlib.image_window()

    # load model and weights
    img_size = 160

    faces_tracked = -1
    tracked_faces = []

    last_read = arrow.now()
    last_demo = arrow.now()

    while True:
        now = arrow.now()

        rd = (now - last_read).total_seconds()
        if (rd > TIME_BETWEEN_READS):
            
            t = time.time()

            last_read = arrow.now()

            ret, img = cap.read()
            if not ret:
                print("error: failed to capture image")
                return -1

            #img = imutils.resize(img, width=MAX_FRAME_WIDTH)
            #img = cv2.flip(img, 1)

            input_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_h, img_w, _ = np.shape(input_img)

            # The 1 in the second argument indicates that we should upsample the image
            # 1 time.  This will make everything bigger and allow us to detect more
            # faces.
            d = datetime.datetime.now()
            detected = detector(gray, 0)
            d_2 = float((datetime.datetime.now() - d).microseconds) / 1000000

            people_in_last_frame = len(detected)
            faces = np.empty((len(detected), img_size, img_size, 3))

            # compute the ages / genders
            ld = (now - last_demo).total_seconds()
            ages = []
            genders = []
            g_2 = 0
            if people_in_last_frame > 0 and ld > TIME_BETWEEN_DEMO:
                
                # align the faces
                for i, d in enumerate(detected):
                    faces[i, :, :, :] = fa.align(input_img, gray, detected[i])
                
                g = datetime.datetime.now()
                ages,genders = sess.run([age, gender], feed_dict={images_pl: faces, train_mode: False})
                g_2 = float((datetime.datetime.now() - g).microseconds) / 1000000

                last_demo = arrow.now()
                
            check_session_timeout(REMOVE_USER_TIMEOUT_SECONDS, now, tracked_faces)

            current_usr = ''
            biggest_img = 0

            fd_2 = 0
            #tmp = imutils.resize(img, width=640)

            d_ct = 0
            for k, d in enumerate(detected):

                if (len(ages)>0):
                    Logger.log("age: {}".format(int(ages[d_ct])))

                shape = predictor(img, d)

                fd = datetime.datetime.now()
                face_descriptor = faceRecog.compute_face_descriptor(img, shape)
                fd_2 = float((datetime.datetime.now() - fd).microseconds) / 1000000

                found = False
                area = d.width() * d.height()

                deets = ''
                best_match = 100
                best_face = None
                for face in tracked_faces:
                    dst = distance.euclidean(face_descriptor, face.descriptor)

                    # Logger.log("age: {0}, gender:{1}".format(ages[i], genders[i]))
                    if dst < FACE_MATCH and dst<best_match:
                        # Logger.log("match {}: {}".format(t, dst))
                        best_match = dst
                        best_face = face

                if best_face is not None:
                    # matches a face we're already tracking
                    found = True
                    best_face.recordVisit()
                    # face.descriptor = face_descriptor

                    if len(ages) > 0:
                        best_face.add_age(int(ages[d_ct]))
                        best_face.add_sex(genders[d_ct])

                    deets = best_face.detailStr()

                Logger.log("-------")

                if not found:
                    newFace = Face(face_descriptor)
                    tracked_faces.append(newFace)

                    if len(ages) > 0:
                        newFace.add_age(int(ages[d_ct]))
                        newFace.add_sex(genders[d_ct])

                    deets = newFace.detailStr()

                    Logger.log("NEW FACE! {}".format(newFace.id))

                if area > biggest_img:
                    biggest_img = area
                    current_usr = deets

                if LIVE_VIDEO:
                    # drawing the rectangle & label
                    x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    draw_label(img, (d.left(), d.top()), deets)

                d_ct += 1

                if faces_tracked != len(tracked_faces):
                    Logger.log('{} tracked face'.format(len(tracked_faces)))
                    faces_tracked = len(tracked_faces)

                if not LOCAL_MODE and LIVE_VIDEO:
                    socketIO.emit('current-user',{'details': current_usr})

                if LOCAL_MODE:
                    win.set_image(img)
                if LIVE_VIDEO:
                    frame4 = imutils.resize(img, width=320)
                    #frame4 = cv2.flip(frame4, 1)

                    encImg = cv2.imencode('.png', frame4[:])
                    buff = base64.b64encode(encImg[1])

                    socketIO.emit('frame', {"buffer": buff.decode(
                    'utf-8')})
            
            t_2 = time.time()-t

            if fd_2 > 0:
                Logger.log('total {0}s | detector {1}s | gender {2}s | descriptor {3}s '.format(t_2, d_2, g_2, fd_2))
            #
            #   n_sync = '{}_{}'.format(now.minute, now.second)
            #
            # if n_sync != ms_sync:
            #     ms_sync = n_sync
            #     unsyncd = storage.getUnsyncedSessions()
            #
            #     if len(unsyncd) > 0:
            #         Logger.log("syncing")
            #
            #         r = start_new_thread(iot.updateSessions, (unsyncd,))
            #
            #         if r is not False:
            #             storage.updateSessionSyncStatus(unsyncd)

def check_session_timeout(REMOVE_USER_TIMEOUT_SECONDS, now, tracked_faces):
    # iterate all the existing tracked_faces we know of and clean them up
    for face in tracked_faces:
        latest_session = face.mostRecentSession()
        face.checkSessionTimeout()

        if latest_session is not None:
            if (now - latest_session.lastSeen).total_seconds() >= REMOVE_USER_TIMEOUT_SECONDS:
                tracked_faces.remove(face)


def load_network(model_path):
    sess = tf.Session()
    images_pl = tf.placeholder(tf.float32, shape=[None, 160, 160, 3], name='input_image')
    images_norm = tf.map_fn(lambda frame: tf.image.per_image_standardization(frame), images_pl)

    train_mode = tf.placeholder(tf.bool)
    age_logits, gender_logits, _ = inception_resnet_v1.inference(images_norm, keep_probability=0.8,
                                                                 phase_train=train_mode,
                                                                 weight_decay=1e-5)
    gender = tf.argmax(tf.nn.softmax(gender_logits), 1)
    age_ = tf.cast(tf.constant([i for i in range(0, 101)]), tf.float32)
    age = tf.reduce_sum(tf.multiply(tf.nn.softmax(age_logits), age_), axis=1)
    init_op = tf.group(tf.global_variables_initializer(),
                       tf.local_variables_initializer())
    sess.run(init_op)
    saver = tf.train.Saver()
    ckpt = tf.train.get_checkpoint_state(model_path)
    if ckpt and ckpt.model_checkpoint_path:
        saver.restore(sess, ckpt.model_checkpoint_path)
        print("restore model!")
    else:
        pass
    return sess,age,gender,train_mode,images_pl

if __name__ == '__main__':
    sess, age, gender, train_mode,images_pl = load_network("./models")
    main(sess,age,gender,train_mode,images_pl)