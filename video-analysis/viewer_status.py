
from logger import Logger

class ViewerStatus:

    def __init__(self):
        self.avg_age = 0
        self.avg_gender = 0
        self.closest_age = 0
        self.closest_gender = 0
        self.viewer_ct = 0
        self.last_viewer_ct = 0

        self.dirty = False

    def set_viewer_ct(self, ct):
        if ct != self.last_viewer_ct:
            self.last_viewer_ct = ct
            self.viewer_ct = ct

            Logger.log('viewer count dirty')
            self.dirty = True

    def set_viewer_avg_demos(self, age, gender):
        if self.avg_age != age:
            self.avg_age = age
            self.avg_gender = gender

            Logger.log('avg dirty')
            self.dirty = True

    def set_viewer_demos(self, age, gender):
        if self.closest_age != age or self.closest_gender != gender:
            self.closest_age = age
            self.closest_gender = gender

            Logger.log('demos dirty')
            self.dirty = True
