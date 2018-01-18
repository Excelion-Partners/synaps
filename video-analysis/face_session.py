import arrow

USER_SESSION_TIMEOUT_SECONDS = 6

class FaceSession:
    def __init__(self):
        self.firstSeen = arrow.utcnow()
        self.lastSeen = arrow.utcnow()
        self.complete = False
        self.ads = []

    def sessionStart(self):
        return self.firstSeen.datetime

    def sessionLength(self):
        return (self.lastSeen - self.firstSeen).total_seconds()