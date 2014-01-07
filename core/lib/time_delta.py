class TimeDelta:
    def __init__(self, _seconds):
        self.seconds = _seconds

    @property
    def minutes(self):
        return self.seconds / 60.0

    @property
    def hours(self):
        return self.minutes / 60.0

    @property
    def days(self):
        return self.hours / 24.0
