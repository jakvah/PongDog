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
    query = "INSERT INTO pongdog_users (cardid,name,elo,games_played) values (%s,%s,%s,%s)"
    cur.execute(query,(int(card_id),str(user_name),1000,0))
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




# --------------------------------- PONG DOG FUNCTIONS --------------------------------- #

def add_pong_dog_user(card_id,user_name):
    conn = get_database_connection()
    cur = conn.cursor()
    query = "INSERT INTO pongdog_users (cardid,name,elo,games_played) values (%s,%s,%s,%s)"
    cur.execute(query,(int(card_id),str(user_name),1000,0))
    conn.commit()
    cur.close()
    conn.close()















