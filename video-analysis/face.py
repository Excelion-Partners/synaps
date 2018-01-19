import json
import cv2
from random import randint
import arrow
import threading
import boto3

from face_session import FaceSession
from logger import Logger

USER_SESSION_TIMEOUT_SECONDS = 6
MIN_SESSION_LENGTH = 2

class Face:

    def __init__(self, descriptor):

        self.id = randint(1000000, 100000000)
        self.descriptor = descriptor
        self.sessions = []

        self.age_tot = 0
        self.age_ct = 0
        self.sex_tot = 0
        self.sex_ct = 0
     
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
        self.age_tot += age
        self.age_ct += 1

    def add_sex(self, sex):
        # Logger.log('{0}, {1}'.format(self.sex_tot, self.sex_ct))
        self.sex_tot += sex
        self.sex_ct += 1

    def sex(self):
        sx = float(self.sex_tot) / float(self.sex_ct)
        return 'Male' if sx > .5 else 'Female'

    def age(self):
        age = float(self.age_tot) / float(self.age_ct)
        return age

    def detailStr(self):
       return '{0}{1} {2}'.format(int(self.age()), self.sex(), self.id)

    def endCurrentSession(self):
        ses = self.currentSession()

        if ses is None:
            return

        if ses.session_length() < MIN_SESSION_LENGTH:
            self.sessions.remove(ses)
            Logger.log("Killed a user session because it was too short")
        else:
            self.currentSession().complete = True

    def appendNewSession(self):
        Logger.log('new user session')
        self.sessions.append(FaceSession())

    def secondsInCurrentSession(self):
        sess = self.currentSession()
        if sess is not None:
            return self.currentSession().session_length()

        return 0