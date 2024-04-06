import uuid
import time


class dbCommands:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

    def create_user_table(self):
        self.cur.execute('DROP TABLE IF EXISTS users;')
        self.cur.execute("""
            CREATE TABLE users (
            uid varchar (100) PRIMARY KEY,
            user_name varchar (100) NOT NULL,
            daily_reps NUMERIC NOT NULL);
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
            description varchar (1000) NOT NULL,
            isTime BOOLEAN NOT NULL,
            start_time NUMERIC,
            end_time NUMERIC,
            target NUMERIC NOT NULL);
        """)
        self.conn.commit()

    def create_joined_challenge_table(self):
        self.cur.execute('DROP TABLE IF EXISTS joined_challenge;')
        self.cur.execute("""
            CREATE TABLE joined_challenge (
            id varchar (100) PRIMARY KEY,
            uid varchar (100) NOT NULL,
            user_name varchar (100) NOT NULL,
            challenge_id varchar (100) NOT NULL,
            chellenge_name varchar (100) NOT NULL,
            current_progress NUMERIC NOT NULL
        );
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

    def create_challenge(self, challenge_name, award, description, is_time, end_time, target):
        self.cur.execute(f"""
            INSERT INTO challenges
            VALUES (
                '{uuid.uuid1()}', '{challenge_name}', '{award}', '{description}', '{is_time}', '{time.time()}', '{end_time}', {target}
            );
        """)
        self.conn.commit()

    def get_user_name(self, user_uid):
        self.cur.execute(f"""
            SELECT user_name FROM users WHERE uid = '{user_uid}';
        """)
        user_name = self.cur.fetchone()[0]
        return user_name
    
    def get_user_stats(self, user_uid):
        self.cur.execute(f"""
            SELECT daily_reps, time, calories FROM users WHERE uid = '{user_uid}';
        """)
        user_name = self.cur.fetchone()
        return user_name

    def get_challenge(self):
        self.cur.execute(f"""
            SELECT challenge_name, award, description, istime, start_time, end_time, target, id FROM challenges;
        """)
        # WHERE end_time > {time.time()}
        challenges = list(self.cur.fetchall())
        return challenges

    def find_challenge(self, challenge_id):
        self.cur.execute(f"""
            SELECT id, challenge_name, award, description, istime, start_time, end_time, target FROM challenges WHERE id='{challenge_id}';
        """)
        challenges = self.cur.fetchone()
        return challenges

    def join_challenge(self, uid, user_name, challenge_id):
        self.cur.execute(f"""
            SELECT challenge_name FROM challenges WHERE id='{challenge_id}';
        """)
        challenge_name = self.cur.fetchone()[0]
        self.cur.execute(f"""
            INSERT INTO joined_challenge VALUES (
                '{uuid.uuid1()}', '{uid}', '{user_name}', '{challenge_id}', '{challenge_name}', 0
            );
        """)
        self.conn.commit()

    def get_challenge_rank(self, challenge_id):
        self.cur.execute(f"""
            SELECT user_name, current_progress, RANK() OVER (ORDER BY current_progress DESC) as rank FROM joined_challenge WHERE challenge_id='{challenge_id}';
        """)
        try:
            rank_result = list(self.cur.fetchall())[:5]
        except:
            try:
                rank_result = list(self.cur.fetchall())
            except:
                rank_result = []
        return rank_result

    def show_joined_challenge(self, user_uid):
        self.cur.execute(f"""
            SELECT challenge_id from joined_challenge WHERE uid='{user_uid}';
        """)
        joined_result = list(self.cur.fetchall())
        return joined_result

    def join_data(self, user_uid, challenge_id):
        self.cur.execute(f"""
            SELECT current_progress from joined_challenge WHERE uid='{user_uid}' and challenge_id='{challenge_id}';
        """)
        try:
            data = self.cur.fetchone()
        except:
            data = None

        self.cur.execute(f"""
            SELECT uid, user_name, current_progress, RANK() OVER (ORDER BY current_progress DESC) as rank FROM joined_challenge WHERE challenge_id='{challenge_id}';
        """)
        rank_result = list(self.cur.fetchall())
        data_result = []
        for i in range(len(rank_result)):
            if rank_result[i][0] == user_uid:
                data_result = list(rank_result[i])

        result = {
            "rank_result": data_result,
            "data_result": data
        }
        return result

    def join_rank(self, user_uid, challenge_id):
        self.cur.execute(f"""
            SELECT uid, current_progress, RANK() OVER (ORDER BY current_progress DESC) as rank FROM joined_challenge WHERE challenge_id='{challenge_id}';
        """)
        rank_result = list(self.cur.fetchall())
        data_result = []
        for i in range(len(rank_result)):
            if rank_result[i][0] == user_uid:
                data_result = list(rank_result[i])
        return data_result

    def update_data(self, current_progress, challenge_id, user_uid):
        print(current_progress)
        self.cur.execute(f"""
            Update joined_challenge set current_progress={current_progress} where challenge_id='{challenge_id}' and uid='{user_uid}';
        """)
        self.conn.commit()
    
    def find_joined_challenge(self, user_uid):
            # def show_joined_challenge(self, user_uid):
        joined_challenge = self.show_joined_challenge(user_uid)
        result = []
        for i in range(len(joined_challenge)):
            self.cur.execute(f"""
                SELECT id, challenge_name, award, description, istime, start_time, end_time, target FROM challenges WHERE id='{joined_challenge[i][0]}';
            """)
            challenges = self.cur.fetchone()
            result.append(challenges)
        return result
    
    def update_reps(self, user_uid, reps):
        self.cur.execute(f"""
            Update users set daily_reps={reps} where uid='{user_uid}';
        """)
        self.conn.commit()
    
    def update_time(self, user_uid, time):
        self.cur.execute(f"""
            Update users set time=time+{time} where uid='{user_uid}';
        """)
        self.conn.commit()
    
    def update_calories(self, user_uid, calories):
        self.cur.execute(f"""
            Update users set calories={calories} where uid='{user_uid}';
        """)
        self.conn.commit()