import MySQLdb

DATABASE_LOGIN_DETAILS = {
	"host":"jakvah.mysql.pythonanywhere-services.com",
	"user":"jakvah",
	"password":"passord123",
	"database":"jakvah$coffeedog"
}

# Returns a datbase connection object.
def get_database_connection():
    try:
        db_conn = MySQLdb.connect(DATABASE_LOGIN_DETAILS["host"],DATABASE_LOGIN_DETAILS["user"],DATABASE_LOGIN_DETAILS["password"],DATABASE_LOGIN_DETAILS["database"],use_unicode=True, charset="utf8")
        return db_conn
    except Exception as e:
        #print("Could not establish connection to the database. Is the server running?")
        return f"Failed, {e}"

def add_pong_dog_user(card_id,user_name):
    conn = get_database_connection()
    cur = conn.cursor()
    query = "INSERT INTO pongdog_users (cardid,name,elo,games_played,wins) values (%s,%s,%s,%s,%s)"
    cur.execute(query,(int(card_id),str(user_name),1000,0,0))
    conn.commit()
    cur.close()
    conn.close()

def pong_user_exists(id,table_name = "pongdog_users"):
    conn = get_database_connection()
    cur = conn.cursor()
    query = f"SELECT * FROM {table_name}"
    cur.execute(query)
    set = cur.fetchall()
    for row in set:
        if int(row[1]) == int(id):
            cur.close()
            conn.close()
            return True
    else:
        cur.close()
        conn.close()
        return False


def is_match_ongoing():
    conn = get_database_connection()
    cur = conn.cursor()
    query = "SELECT * FROM active_game"
    cur.execute(query)
    set = cur.fetchall()[0]
    if int(set[0]) == 1:
        return True
    else:
        return False


def reset_match_status():
    conn = get_database_connection()
    cur = conn.cursor()
    query = "delete from active_game"
    cur.execute(query)
    conn.commit()

    query = "INSERT INTO active_game (ongoing,player1_id,player2_id,player1_score,player2_score,start_time) values(%s,%s,%s,%s,%s,%s)"

    cur.execute(query,(0,-1,-1,-1,-1,"-"))
    conn.commit()
    cur.close()
    conn.close()


def init_match(p1_id,p2_id,start_time):
    try:
        conn = get_database_connection()
        cur = conn.cursor()
        query = "delete from active_game"
        cur.execute(query)
        conn.commit()

        query = "INSERT INTO active_game (ongoing,player1_id,player2_id,player1_score,player2_score,start_time) values(%s,%s,%s,%s,%s,%s)"

        cur.execute(query,(1,int(p1_id),int(p2_id),0,0,str(start_time)))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception:
        return False

def increment_score(player_num):
    try:
        conn = get_database_connection()
        cur = conn.cursor()

        if player_num == 1:
            query = "UPDATE active_game SET player1_score = player1_score + 1 WHERE ongoing = 1"
        elif player_num == 2:
            query = "UPDATE active_game SET player2_score = player2_score + 1 WHERE ongoing = 1"

        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception:
        return False


def get_sorted_pongdog_leaderboard():
    conn = get_database_connection()
    cur = conn.cursor()
    query = "SELECT * FROM pongdog_users ORDER BY elo DESC"

    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data












