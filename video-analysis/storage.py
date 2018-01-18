import sys
import os
import time
import datetime

from face_session import FaceSession
from logger import Logger

class Storage:
    
    def __init__(self, descriptor):
        
    
    def insert_session(self, face, session):
        try:
            conn = psycopg2.connect("dbname=synaps user=synaps password=3wPUBimpTH6Y")
            cur = conn.cursor()

            sql = """INSERT INTO sessions(start_date, duration, age, sex) values (%s, %s, %s, %s);"""

            cur.execute(sql, (session.sessionStart(), session.sessionLength(), face.age(), face.sex()))

            conn.commit()
            cur.close()
        except(Exception, psycopg2.DatabaseError) as error:
            Logger.log(error)
        finally:
            if conn is not None:
                conn.close()