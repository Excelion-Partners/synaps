import json
import cv2
from random import randint
import arrow
import threading
import boto3
import math

from face_session import FaceSession
from logger import Logger
from storage import Storage
import numpy as np

USER_SESSION_TIMEOUT_SECONDS = 6
MIN_SESSION_LENGTH = 2

class Face:

    def __init__(self, descriptor):

        self.id = randint(1000000, 100000000)
        self.descriptor = descriptor
        self.sessions = []

        self.storage = Storage()
        self.sexes = []
        self.ages = []
        self.largest_img = 0
     
        self.appendNewSession()

    def currentSession(self):
        for session in self.sessions:
            if (session.complete == False):
                return session

    def secondsSinceLastSeen(self):
        return (arrow.now() - self.currentSession().lastSeen).total_seconds()

    def mostRecentSession(self):
        ct = len(self.sessions)
        if (ct == 0):
            return None

        return self.sessions[ct-1]

    def checkSessionTimeout(self):
        if self.currentSession() is None:
            return False

        if (self.secondsSinceLastSeen() >= USER_SESSION_TIMEOUT_SECONDS):
            self.endCurrentSession()
            return True

    def recordVisit(self):
        if self.currentSession() is None:
            self.appendNewSession()

        self.currentSession().lastSeen = arrow.now()

    def add_age(self, age):
        self.ages.append(age)

    def add_sex(self, sex):
        self.sexes.append(sex)

    def sex(self):
        sx = self.gender()

        if sx == 0:
            return '--'

        return 'Male' if sx > .5 else 'Female'

    def gender(self):
        if len(self.sexes) < 4:
            return 0

        skip = int(math.floor(float(len(self.sexes)) / 4))
        sx = np.mean(sorted(self.sexes)[skip:(skip * 2)])

        return sx

    def age(self):
        if len(self.ages) < 4:
            return 0

        skip = int(math.floor(float(len(self.ages)) / 4))

        age = np.mean(sorted(self.ages)[skip:(skip*2)])

        return age

    def detailStr(self):
        if self.age() == 0:
            return "--"

        return '{0} {1}'.format(int(self.age()), self.sex())

    def endCurrentSession(self):
        ses = self.currentSession()

        if ses is None:
            return

        if ses.session_length() < MIN_SESSION_LENGTH:
            self.sessions.remove(ses)
            Logger.log("Killed a user session because it was too short")
        else:
            self.storage.insert_session(self, self.currentSession())
            self.currentSession().complete = True

    def appendNewSession(self):
        Logger.log('new user session')
        self.sessions.append(FaceSession())

    def secondsInCurrentSession(self):
        sess = self.currentSession()
        if sess is not None:
            return self.currentSession().session_length()

        return 0