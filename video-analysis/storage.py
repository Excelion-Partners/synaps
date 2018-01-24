import sys
import os
import time
import datetime
import json

import psycopg2

from face_session import FaceSession
from logger import Logger

class Storage:
    
    def __init__(self):
        # self.conn_str = "dbname='synaps' user='synaps' password='3wPUBimpTH6Y' host='localhost'"
        self.conn_str = "dbname='redpanda' user='sa' password='redpanda' host='redpanda-dev.cd7qb5oqj1aq.us-east-1.rds.amazonaws.com'"

    def get_changes(self):
        conn = psycopg2.connect(self.conn_str)
        cur = conn.cursor()
        cur.execute("""
          SELECT
             row_to_json(sessions)
             FROM sessions
             LIMIT 10
        """)

        result = cur.fetchall()

        cur.close()
        conn.close()

        return list(result)

    def insert_session(self, face, session):
        try:
            conn = psycopg2.connect(self.conn_str)
            cur = conn.cursor()

            # sql = """INSERT INTO sessions(start_date, duration, age, sex) values (%s, %s, %s, %s);"""
            sql = """INSERT INTO sessions (start_time, end_time, age_low, age_high, male) VALUES (%s, %s, %s, %s, %s)"""

            sx = 'false'
            if face.sex() == 'Male':
                sx = 'true'

            cur.execute(sql, (session.firstSeen.datetime, session.lastSeen.datetime, face.age(), face.age(), sx))

            conn.commit()
            cur.close()
            Logger.log('inserted session')
        except(Exception, psycopg2.DatabaseError) as error:
            Logger.log(error)
        finally:
            if conn is not None:
                conn.close()