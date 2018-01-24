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
        self.conn_str = "dbname=synaps user=synaps password=3wPUBimpTH6Y"

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

            sql = """INSERT INTO sessions(start_date, duration, age, sex) values (%s, %s, %s, %s);"""

            cur.execute(sql, (session.session_start(), session.session_length(), face.age(), face.sex()))

            conn.commit()
            cur.close()
            Logger.log('inserted session')
        except(Exception, psycopg2.DatabaseError) as error:
            Logger.log(error)
        finally:
            if conn is not None:
                conn.close()