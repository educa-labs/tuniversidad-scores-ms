import psycopg2 as psql
import json
import datetime
# Test
from score_regressor import get_best
from numpy import array

class DB():

    def __init__(self):
        while True:
            try:
                self.conn = psql.connect("dbname=tuniversidad_production user=pguser password=tuniversidad host=api.tuniversidad.cl port=5432")
                self.cur = self.conn.cursor()
                break
            except:
                pass

    def get_essays(self, uid, subject_id):
        self.cur.execute("SELECT score, date_full FROM essays WHERE subject_id=%s AND user_id=%s ORDER BY date_full", (subject_id, uid))
        result = self.cur.fetchall()
        return self.calculate_relative_days(result)

    def get_id_by_email(self, email):
        self.cur.execute("SELECT id FROM users WHERE email=%s", (email,))
        return self.cur.fetchone()[0]

    def calculate_relative_days(self, essays_tuples):
        if len(essays_tuples) == 0:
            return []
        main_day = essays_tuples[0][1]

        result = {
                "days": array(list(map(lambda x: (x[1] - main_day).days, essays_tuples))),
                "scores": array(list(map(lambda x: x[0], essays_tuples)))
                }

        return result



if __name__ == "__main__":
    db = DB()
    essays_dict = db.get_essays(db.get_id_by_email("cadizv.in@gmail.com"), 2)
    print(essays_dict)
    prediction = get_best(essays_dict["days"], essays_dict["scores"])
    print(prediction)
    db.conn.close()
