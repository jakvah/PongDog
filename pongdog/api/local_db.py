import mysql.connector

DATABASE_LOGIN_DETAILS = {
	"host":"localhost",
	"user":"root",
	"password":"passord123",
	"database":"test"
}

def get_database_connection():
    try:
        db_conn = mysql.connector.connect(host = DATABASE_LOGIN_DETAILS["host"],user = DATABASE_LOGIN_DETAILS["user"],password = DATABASE_LOGIN_DETAILS["password"],database = DATABASE_LOGIN_DETAILS["database"],use_unicode=True, charset="utf8")
        return db_conn
    except Exception as e:
        #print("Could not establish connection to the database. Is the server running?")
        raise e

def init_match(p1_id,p2_id,p1_elo,p2_elo,p1_name,p2_name,timestamp):
    try:
        conn = get_database_connection()
        cur = conn.cursor()

        query = "delete from game"
        cur.execute(query)
        conn.commit()

        query = "INSERT INTO game (ongoing,p1_id,p2_id,p1_elo,p2_elo,p1_name,p2_name,p1_score,p2_score,timestamp) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        cur.execute(query,(1,int(p1_id),int(p2_id),p1_elo,p2_elo,p1_name,p2_name,0,0,str(timestamp)))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        raise e

def reset_match():
    try:
        conn = get_database_connection()
        cur = conn.cursor()

        query = "delete from game"
        cur.execute(query)
        conn.commit()

        query = "INSERT INTO game (ongoing,p1_id,p2_id,p1_elo,p2_elo,p1_name,p2_name,p1_score,p2_score,timestamp) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        cur.execute(query,(0,int(-1),int(-1),-1,-1,"NaN","NaN",-1,-1,str("-")))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        raise e

def is_match_ongoing():
    conn = get_database_connection()
    cur = conn.cursor()

    query = "SELECT * FROM game"
    cur.execute(query)
    set = cur.fetchall()[0]
    if int(set[0]) == 1:
        return True
    else:
        return False

def increment_score_by_id(player_id):
    pass


def get_local_game_state():
    conn = get_database_connection()
    cur = conn.cursor()

    query =  "SELECT * FROM game"
    cur.execute(query)
    set = cur.fetchall()[0]
    return set

def get_player_id(player_num):
    if player_num != 1 and player_num != 2: raise ValueError(f"Invalid player number:{player_num}")

    conn = get_database_connection()
    cur = conn.cursor()

    query =  "SELECT * FROM game"
    cur.execute(query)
    set = cur.fetchall()[0]
    return set[player_num]

def increment_score(player_num):
    """
    Accepts the player num identifier. Either p1 or p2
    """
    if player_num != "p1" and player_num != "p2": raise ValueError(f"Invalid indentifier:{player_num}")

    try:
        conn = get_database_connection()
        cur = conn.cursor()

        if player_num == "p1":
            query = "UPDATE game set p1_score = p1_score + 1"
        else:
            query = "UPDATE game set p2_score = p2_score + 1"
        
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        raise e

def limbo_match():
    try:
        conn = get_database_connection()
        cur = conn.cursor()

        query = "UPDATE game set ongoing = 2"

        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        raise e
