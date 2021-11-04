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

def limbo_match(p1_id,p2_id,p1_score,p2_score,start_time):
    try:
        conn = get_database_connection()
        cur = conn.cursor()
        query = "delete from active_game"
        cur.execute(query)
        conn.commit()

        query = "INSERT INTO active_game (ongoing,player1_id,player2_id,player1_score,player2_score,start_time) values(%s,%s,%s,%s,%s,%s)"

        cur.execute(query,(2,int(p1_id),int(p2_id),int(p1_score),int(p2_score),str(start_time)))
        conn.commit()
        cur.close()
        conn.close()
        update_elo(p1_id,p2_id,p1_score,p2_score)
        return True
    except Exception:
        return False

def update_elo(p1_id,p2_id,p1_score,p2_score):
    if p1_score > p2_score:
        winner = "p1"
    else:
        winner = "p2"

    player1_elo = get_player_elo(p1_id)
    player2_elo = get_player_elo(p2_id)

    new_player1_elo, new_player2_elo = new_scores(player1_elo,player2_elo,winner)

    conn = get_database_connection()
    cur = conn.cursor()

    query = f"UPDATE pongdog_users SET elo = {new_player1_elo} WHERE cardid = {p1_id}"
    cur.execute(query)
    conn.commit()
    query = f"UPDATE pongdog_users SET elo = {new_player2_elo} WHERE cardid = {p2_id}"
    cur.execute(query)
    conn.commit()

    cur.close()
    conn.close()


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



def get_match_stats():
    conn = get_database_connection()
    cur = conn.cursor()
    query = "SELECT * FROM active_game"
    cur.execute(query)
    set = cur.fetchall()[0]

    cur.close()
    conn.close()
    return set

def get_player_name(id):
    conn = get_database_connection()
    cur = conn.cursor()

    query = f"SELECT * FROM pongdog_users WHERE cardid = {id}"
    cur.execute(query)
    data = cur.fetchall()[0]

    cur.close()
    conn.close()
    return data[2]

def get_player_elo(id):
    conn = get_database_connection()
    cur = conn.cursor()

    query = f"SELECT * FROM pongdog_users WHERE cardid = {id}"
    cur.execute(query)
    data = cur.fetchall()[0]

    cur.close()
    conn.close()

    return data[3]





# ------------------------- ELO ----------------------------#

# ELO
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 18:11:27 2021

@author: mathiasrammhaugland
"""

def elo_at_stake(p1_ELO,p2_ELO):
    adv = 1800 #if you have adv more points than your opponent you are 10 times more likely to win
    k = 50

    pow1 = ((p1_ELO-p2_ELO)/adv)
    exp_score1 = 1/(1+10**pow1)
    p1_win = k*exp_score1 #p1_win is what p1 wins and p2 looses

    pow2 = ((p2_ELO-p1_ELO)/adv)
    exp_score2 = 1/(1+10**pow2)
    p2_win = k*exp_score2 #p2_win is what p2 wins and p1 looses

    return round(p1_win), round(p2_win)


def new_scores(p1_ELO,p2_ELO,winner): #winner is 'p1' or 'p2'
    p1_win, p2_win = elo_at_stake(p1_ELO, p2_ELO)
    if winner == 'p1':
        p1_ELO_new = p1_ELO + p1_win
        p2_ELO_new = p2_ELO - p1_win
    elif winner == 'p2':
        p1_ELO_new = p1_ELO - p2_win
        p2_ELO_new = p2_ELO + p2_win
    else:
        print("Theres a bloody problem here, wankers, arrrrrghhh")

    if p1_ELO_new <= 0:
        p1_ELO_new = 0

    if p2_ELO_new <=0:
        p2_ELO_new = 0

    return p1_ELO_new, p2_ELO_new

