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

def draw_label(image, point, label, font=cv2.FONT_HERSHEY_SIMPLEX,
               font_scale=1, thickness=2):
    size = cv2.getTextSize(label, font, font_scale, thickness)[0]
    x, y = point
    cv2.rectangle(image, (x, y - size[1]), (x + size[0], y), (255, 0, 0), cv2.FILLED)
    cv2.putText(image, label, point, font, font_scale, (255, 255, 255), thickness)

def main(sess,age,gender,train_mode,images_pl):
    LOCAL_MODE = os.getenv('LOCAL_MODE', 'True') == 'True'
    FRAME_SKIP = int(os.getenv('FRAME_SKIP', 4))
    REMOVE_USER_TIMEOUT_SECONDS = int(
        os.getenv('REMOVE_USER_TIMEOUT_SECONDS', 60))  # seconds
    FACE_MATCH = .6

    Logger.log('running in Local mode: {}'.format(LOCAL_MODE))

    socketIO = SocketIO('localhost', 3003, LoggingNamespace)
    Logger.log("Connected to socket.io")

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

    people_in_last_frame = -1
    faces_tracked = -1
    tracked_faces = []
    frame_ct = 0

    while True:
        face_descs = []
        now = arrow.now()

        ret, img = cap.read()
        if not ret:
            print("error: failed to capture image")
            return -1

        #img = imutils.resize(img, width=MAX_FRAME_WIDTH)
        #img = cv2.flip(img, 1)

        input_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_h, img_w, _ = np.shape(input_img)

        detected = detector(input_img, 1)

        people_in_last_frame = len(detected)
        faces = np.empty((len(detected), img_size, img_size, 3))

        # align the faces
        for i, d in enumerate(detected):
            faces[i, :, :, :] = fa.align(input_img, gray, detected[i])

        # compute the ages / genders
        if people_in_last_frame > 0:
            ages,genders = sess.run([age, gender], feed_dict={images_pl: faces, train_mode: False})

        # iterate all the existing tracked_faces we know of and clean them up
        for face in tracked_faces:
            latest_session = face.mostRecentSession()
            face.checkSessionTimeout()

            if latest_session is not None:
                if (now - latest_session.lastSeen).total_seconds() >= REMOVE_USER_TIMEOUT_SECONDS:
                    tracked_faces.remove(face)

        if faces_tracked != len(tracked_faces):
            Logger.log('{} tracked face'.format(len(tracked_faces)))
            faces_tracked = len(tracked_faces)

        frame_mod = frame_ct % FRAME_SKIP

        current_usr = ''
        biggest_img = 0
        for k, d in enumerate(detected):
            if frame_mod == 0:

                shape = predictor(img, d)
                face_descriptor = faceRecog.compute_face_descriptor(img, shape)

                found = False

                # drawing the rectangle & label
                x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

                area = d.width() * d.height()

                deets = ''
                for face in tracked_faces:
                    dst = distance.euclidean(face_descriptor, face.descriptor)

                    # Logger.log("age: {0}, gender:{1}".format(ages[i], genders[i]))
                    if dst < FACE_MATCH:
                        # matches a face we're already tracking
                        found = True
                        face.recordVisit()
                        face.descriptor = face_descriptor

                        face.add_age(int(ages[i]))
                        face.add_sex(genders[i])

                        deets = face.detailStr()

                if not found:
                    newFace = Face(face_descriptor)
                    tracked_faces.append(newFace)

                    newFace.add_age(int(ages[i]))
                    newFace.add_sex(genders[i])

                    deets = newFace.detailStr()

                    Logger.log("NEW FACE! {}".format(newFace.id))

                if area > biggest_img:
                    biggest_img = area
                    current_usr = deets

                if LOCAL_MODE:
                    draw_label(img, (d.left(), d.top()), deets)

        if biggest_img>0:
            socketIO.emit('current-user', deets)

        if LOCAL_MODE:
            win.set_image(img)

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