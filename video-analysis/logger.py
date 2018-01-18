import sys, os, time, datetime
from time import gmtime, strftime

class Logger:

    @staticmethod
    def log(msg):
        sys.stdout.write('{}: {} \n'.format(strftime("%H:%M:%S", gmtime()), msg))
