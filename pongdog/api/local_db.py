import mysql.connector

DATABASE_LOGIN_DETAILS = {
	"host":"localhost",
	"user":"root",
	"password":"passord123",
	"database":"test"
}
def get_database_connection(docker = True):
    if docker:
        try:
            db = mysql.connector.connect(host = 'gamedb', user = 'root', password = 'root', port = 3306)
            return db
        except Exception as e:
            raise e
        
    else:
        try:
            db_conn = mysql.connector.connect(
                                                host = DATABASE_LOGIN_DETAILS["host"],
                                                user = DATABASE_LOGIN_DETAILS["user"],
                                                password = DATABASE_LOGIN_DETAILS["password"],
                                                database = DATABASE_LOGIN_DETAILS["database"],
                                                use_unicode=True, 
                                                charset="utf8")
            return db_conn
        except Exception as e:
            #print("Could not establish connection to the database. Is the server running?")
            raise e

def table_exists(dbcon,dbcur,tablename):
    	dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    	if dbcur.fetchone()[0] >= 1:
        	return True


    	return False

def setup(docker = True):
    try:
        #db = mysql.connector.connect(host = 'gamedb', user = 'root', password = 'root', port = 3306)
        db = get_database_connection(docker)
        cur = db.cursor()
        
        query = "CREATE database IF NOT EXISTS game_db"
        cur.execute(query)
        db.commit()
            
        query = "USE game_db"
        cur.execute(query)
        db.commit()
        query = "CREATE TABLE IF NOT EXISTS game (ongoing INT, p1_id INT, p2_id INT, p1_elo INT, p2_elo INT, p1_name VARCHAR(255), p2_name VARCHAR(255), p1_score INT, p2_score INT, timestamp VARCHAR(255))"
        
        cur.execute(query)
        db.commit()

        query = "INSERT INTO game (ongoing,p1_id,p2_id,p1_elo,p2_elo,p1_name,p2_name,p1_score,p2_score,timestamp) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(query,(0,int(-1),int(-1),-1,-1,"NaN","NaN",-1,-1,str("-")))
        db.commit()
        cur.close()
        db.close()
        print("Sucessfully initialized local game database!")
    
    except Exception as e:
        raise(e)


def init_match(conn,cur,p1_id,p2_id,p1_elo,p2_elo,p1_name,p2_name,timestamp):
    try:
        #conn = get_database_connection()
        #cur = conn.cursor()

        query = "delete from game"
        cur.execute(query)
        conn.commit()

        query = "INSERT INTO game (ongoing,p1_id,p2_id,p1_elo,p2_elo,p1_name,p2_name,p1_score,p2_score,timestamp) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        cur.execute(query,(1,int(p1_id),int(p2_id),p1_elo,p2_elo,p1_name,p2_name,0,0,str(timestamp)))
        conn.commit()


    except Exception as e:
        raise e

def reset_match(conn,cur):
    try:
        query = "delete from game"
        cur.execute(query)
        conn.commit()

        query = "INSERT INTO game (ongoing,p1_id,p2_id,p1_elo,p2_elo,p1_name,p2_name,p1_score,p2_score,timestamp) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        cur.execute(query,(0,int(-1),int(-1),-1,-1,"NaN","NaN",-1,-1,str("-")))
        conn.commit()

    except Exception as e:
        raise e

def is_match_ongoing(conn,cur):
    query = "SELECT * FROM game"
    cur.execute(query)
    set = cur.fetchall()[0]
    if int(set[0]) != 0:
        return True
    else:
        return False


def get_local_game_state(conn,cur):
    query =  "SELECT * FROM game"
    cur.execute(query)
    set = cur.fetchall()[0]
    return set

def get_player_id(conn,cur,player_num):
    if player_num != 1 and player_num != 2: raise ValueError(f"Invalid player number:{player_num}")

    query =  "SELECT * FROM game"
    cur.execute(query)
    set = cur.fetchall()[0]
    return set[player_num]

def increment_score(conn,cur,player_num):
    """
    Accepts the player num identifier. Either p1 or p2
    """
    if player_num != "p1" and player_num != "p2": raise ValueError(f"Invalid indentifier:{player_num}")

    try:
        if player_num == "p1":
            query = "UPDATE game set p1_score = p1_score + 1"
        else:
            query = "UPDATE game set p2_score = p2_score + 1"
        
        cur.execute(query)
        conn.commit()

    except Exception as e:
        raise e

def limbo_match(conn,cur):
    try:
        query = "UPDATE game set ongoing = 2"

        cur.execute(query)
        conn.commit()

    except Exception as e:
        raise e
