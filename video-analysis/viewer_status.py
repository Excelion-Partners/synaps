class ViewerStatus:

    def __init__(self):
        self.avg_age = None
        self.avg_gender = None
        self.closest_age = None
        self.closest_gender = None
        self.viewer_ct = 0
        self.last_viewer_ct = 0

        self.dirty = False

    def set_viewer_ct(self, ct):
        if ct != self.last_viewer_ct:
            self.last_viewer_ct = self.viewer_ct
            self.dirty = True

        self.viewer_ct = ct

    def set_viewer_demos(self, age, gender):
        if self.closest_age != age or self.closest_gender != gender:
            self.closest_age = age
            self.closest_gender = gender

            self.dirty = True
