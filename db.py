import psycopg2 as psql
import json
import datetime

class DB():

    def __init__(self):
        while True:
            try:
                self.conn = psql.connect("dbname=scores_predictor user=fahaase password=123asd456 host=localhost port=5432")
                self.cur = self.conn.cursor()
                break
            except:
                pass
        

    def poblar(self):
        self.cur.execute("""DROP TABLE simulaciones;""")
        a = self.cur.execute("""
            CREATE TABLE predictions(id serial, id_user int)
            """)
        

        self.conn.commit()




if __name__ == "__main__":
    db = DB()

    db.poblar()

    db.conn.close()