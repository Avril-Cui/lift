import uuid
import time

class DB:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

    def create_user_table(self):
        self.cur.execute('DROP TABLE IF EXISTS users;')
        self.cur.execute("""
            CREATE TABLE users (
            uid varchar (100) PRIMARY KEY,
            user_name varchar (100) NOT NULL,
            score NUMERIC NOT NULL);
        """)
        self.conn.commit()
    
    def create_award_table(self):
        self.cur.execute('DROP TABLE IF EXISTS awards;')
        self.cur.execute("""
            CREATE TABLE awards (
            award varchar (100) PRIMARY KEY,
            user_name varchar (100) NOT NULL);
        """)
        self.conn.commit()

    def create_challenge_table(self):
        self.cur.execute('DROP TABLE IF EXISTS challenges;')
        self.cur.execute("""
            CREATE TABLE challenges (
            id varchar (100) PRIMARY KEY,
            challenge_name varchar (100) NOT NULL,
            award varchar (100) NOT NULL,
            description varchar (100) NOT NULL,
            start_time NUMERIC NOT NULL,
            end_time NUMERIC NOT NULL);
        """)
        self.conn.commit()
    
    def add_user(self, uid, user_name):
        self.cur.execute(f"""
            INSERT INTO users
            VALUES (
                '{uid}', '{user_name}', 0
            );
        """)
        self.conn.commit()
    
    def create_challenge(self, challenge_name, award, description, end_time):
        self.cur.execute(f"""
            INSERT INTO challenges
            VALUES (
                '{uuid.uuid1()}', '{challenge_name}', '{award}', '{description}', '{time.time()}', '{end_time}'
            );
        """)
        self.conn.commit()
        