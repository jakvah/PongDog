import MySQLdb

DATABASE_LOGIN_DETAILS = {
    "host": "jakvah.mysql.pythonanywhere-services.com",
    "user": "jakvah",
    "password": "passord123",
    "database": "jakvah$coffeedog"
}

#conn = MySQLdb.connect(DATABASE_LOGIN_DETAILS["host"],DATABASE_LOGIN_DETAILS["user"],DATABASE_LOGIN_DETAILS["password"],DATABASE_LOGIN_DETAILS["database"],use_unicode=True, charset="utf8")
#cur = conn.cursor()

# Returns a datbase connection object.


def get_database_connection():
    try:
        db_conn = MySQLdb.connect(DATABASE_LOGIN_DETAILS["host"], DATABASE_LOGIN_DETAILS["user"],
                                  DATABASE_LOGIN_DETAILS["password"], DATABASE_LOGIN_DETAILS["database"], use_unicode=True, charset="utf8")
        return db_conn
    except Exception as e:
        #print("Could not establish connection to the database. Is the server running?")
        return f"Failed, {e}"


def get_rooms(conn, cur):
    query = "SELECT id, name FROM logdog_rooms"
    cur.execute(query)
    response = cur.fetchall()
    ret = []
    for row in response:
        ret.append({"id": row[0], "name": row[1]})
    return ret


def get_room(conn, cur, id):
    query = f"SELECT room.id AS roomId, room.name AS roomName, user.id AS userId, user.name AS userName, user.lastSeenAt AS lastSeenAt FROM logdog_rooms room LEFT JOIN logdog_users user ON user.primaryRoomId = room.id WHERE room.id = %s"
    cur.execute(query, (int(id),))
    response = cur.fetchall()
    ret = {"id": response[0][0], "name": response[0][1], "users": []}
    for row in response:
        if type(row[2]) == int:
            ret["users"].append(
                {"id": row[2], "name": row[3], "lastSeenAt": row[4]})
    return ret


def get_devices(conn, cur):
    query = f"SELECT d.id, d.userId, d.macAddress, DATE_FORMAT( CONVERT_TZ(u.lastSeenAt, @@session.time_zone, '+00:00')  ,'%Y-%m-%dT%TZ') FROM logdog_devices d LEFT JOIN logdog_users u ON d.userId = u.id"
    cur.execute(query)
    response = cur.fetchall()
    ret = []
    for row in response:
        ret.append({"id": row[0], "userId": row[1],
                    "macAddress": row[2], "lastSeenAt": row[3]})
    return ret


def register_visit(conn, cur, user_id):
    query = f"UPDATE logdog_users SET lastSeenAt = CURRENT_TIMESTAMP WHERE id = %s"
    cur.execute(query, (int(user_id),))
    conn.commit()


def register_logdog_user(conn, cur, body):
    # Register user
    query_user = f"INSERT INTO logdog_users (name, primaryRoomId) VALUES (%s, %s)"
    cur.execute(query_user, (body["name"], body["roomId"]))

    user_id = cur.lastrowid

    # Register devices
    query_device = f"INSERT INTO logdog_devices (userId, name, macAddress) VALUES(%s, %s, %s)"
    for device in body["devices"]:
        cur.execute(
            query_device, (user_id, device["name"], device["macAddress"]))

    conn.commit()


def insert_new_coffee(conn, cur, id, timestamp, table_name="history"):
    query = f"INSERT INTO {table_name} (id,timestamp) VALUES (%s,%s)"
    cur.execute(query, (int(id), str(timestamp)))
    conn.commit()


def user_exists(conn, cur, id, table_name="user_stats"):
    query = f"SELECT * FROM {table_name}"
    cur.execute(query)
    set = cur.fetchall()
    for row in set:
        if int(row[0]) == int(id):
            return True
    else:
        return False


def add_new_user_id(conn, cur, id, name, num_coffees=0):
    query = "INSERT INTO user_stats (id,name,num_coffees) values (%s,%s,%s)"
    cur.execute(query, (int(id), str(name), int(num_coffees)))
    conn.commit()


def set_user_name(conn, cur, id, new_name):
    query = f"UPDATE user_stats SET name = {new_name} WHERE id = {id}"
    cur.execute(query)
    conn.commit()


def update_user_stats(conn, cur, id):
    if not user_exists(id):
        add_new_user_id(id, "Unknown user")
    query = f"UPDATE user_stats SET num_coffees = num_coffees + 1 WHERE id = {id}"
    cur.execute(query)
    conn.commit()


def get_latest_dogger(conn, cur):

    query = "SELECT * FROM history ORDER BY regid DESC LIMIT 1"
    cur.execute(query)

    data = cur.fetchall()

    return data[0]


def get_user_data(conn, cur, id):

    query = f"SELECT * FROM user_stats WHERE id = {id}"
    cur.execute(query)

    data = cur.fetchall()[0]

    return data


def get_sorted_leaderboard(conn, cur):

    query = "SELECT * FROM user_stats ORDER BY num_coffees DESC"

    cur.execute(query)
    data = cur.fetchall()
    return data

# --------------------------------- PONG DOG FUNCTIONS --------------------------------- #


def add_pong_dog_user(conn, cur, card_id, user_name):

    query = "INSERT INTO pongdog_users (cardid,name,elo,games_played,wins) values (%s,%s,%s,%s,%s)"
    cur.execute(query, (int(card_id), str(user_name), 1000, 0, 0))
    conn.commit()


def pong_user_exists(conn, cur, id, table_name="pongdog_users"):

    query = f"SELECT * FROM {table_name}"
    cur.execute(query)
    set = cur.fetchall()
    for row in set:
        if int(row[1]) == int(id):

            return True
    else:

        return False


def is_match_ongoing(conn, cur):

    query = "SELECT * FROM active_game"
    cur.execute(query)
    set = cur.fetchall()[0]
    if int(set[0]) == 1:
        return True
    else:
        return False


def reset_match_status(conn, cur):

    query = "delete from active_game"
    cur.execute(query)
    conn.commit()

    query = "INSERT INTO active_game (ongoing,player1_id,player2_id,player1_score,player2_score,start_time) values(%s,%s,%s,%s,%s,%s)"

    cur.execute(query, (0, -1, -1, -1, -1, "-"))
    conn.commit()


def init_match(conn, cur, p1_id, p2_id, start_time):
    try:

        query = "delete from active_game"
        cur.execute(query)
        conn.commit()

        query = "INSERT INTO active_game (ongoing,player1_id,player2_id,player1_score,player2_score,start_time) values(%s,%s,%s,%s,%s,%s)"

        cur.execute(query, (1, int(p1_id), int(p2_id), 0, 0, str(start_time)))
        conn.commit()
        return True
    except Exception:
        return False


def limbo_match(conn, cur, p1_id, p2_id, p1_score, p2_score, start_time):
    try:
        query = "delete from active_game"
        cur.execute(query)
        conn.commit()

        query = "INSERT INTO active_game (ongoing,player1_id,player2_id,player1_score,player2_score,start_time) values(%s,%s,%s,%s,%s,%s)"

        cur.execute(query, (2, int(p1_id), int(p2_id), int(
            p1_score), int(p2_score), str(start_time)))
        conn.commit()
        update_elo(conn, cur, p1_id, p2_id, p1_score, p2_score)

        if p1_score > p2_score:
            increment_wins(conn, cur, p1_id)
        else:
            increment_wins(conn, cur, p2_id)

        increment_games_played(conn, cur, p1_id)
        increment_games_played(conn, cur, p2_id)
        return True
    except Exception:
        return False


def update_elo(conn, cur, p1_id, p2_id, p1_score, p2_score):
    if p1_score > p2_score:
        winner = "p1"
    else:
        winner = "p2"

    player1_elo = get_player_elo(conn, cur, p1_id)
    player2_elo = get_player_elo(conn, cur, p2_id)

    new_player1_elo, new_player2_elo = new_scores(
        player1_elo, player2_elo, winner)

    query = f"UPDATE pongdog_users SET elo = {new_player1_elo} WHERE cardid = {p1_id}"
    cur.execute(query)
    conn.commit()
    query = f"UPDATE pongdog_users SET elo = {new_player2_elo} WHERE cardid = {p2_id}"
    cur.execute(query)
    conn.commit()


def increment_wins(conn, cur, card_id):

    query = f"UPDATE pongdog_users SET wins = wins + 1 WHERE cardid = {card_id}"

    cur.execute(query)
    conn.commit()


def increment_games_played(conn, cur, card_id):

    query = f"UPDATE pongdog_users SET games_played = games_played + 1 WHERE cardid = {card_id}"

    cur.execute(query)
    conn.commit()


def increment_score(conn, cur, player_num):
    try:

        if player_num == 1:
            query = "UPDATE active_game SET player1_score = player1_score + 1 WHERE ongoing = 1"
        elif player_num == 2:
            query = "UPDATE active_game SET player2_score = player2_score + 1 WHERE ongoing = 1"

        cur.execute(query)
        conn.commit()

        return True
    except Exception:
        return False


def get_sorted_pongdog_leaderboard(conn, cur):

    query = "SELECT * FROM pongdog_users where games_played > 2 ORDER BY elo DESC"

    cur.execute(query)
    data = cur.fetchall()

    return data


def get_match_stats(conn, cur):

    query = "SELECT * FROM active_game"
    cur.execute(query)
    set = cur.fetchall()[0]

    return set


def get_player_name(conn, cur, id):

    query = f"SELECT * FROM pongdog_users WHERE cardid = {id}"
    cur.execute(query)
    data = cur.fetchall()[0]

    return data[2]


def get_player_elo(conn, cur, id):

    query = f"SELECT * FROM pongdog_users WHERE cardid = {id}"
    cur.execute(query)
    data = cur.fetchall()[0]

    return data[3]


def get_number_of_players(conn, cur):

    query = "select * from pongdog_users"
    cur.execute(query)
    data = cur.fetchall()

    return len(data)


def get_total_games(conn, cur):

    total = 0
    query = "SELECT * FROM pongdog_users"
    cur.execute(query)
    data = cur.fetchall()
    for row in data:
        total += row[5]

    return total


# ------------------------- ELO ----------------------------#
# ELO
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 18:11:27 2021

@author: mathiasrammhaugland
"""


def elo_at_stake(p1_ELO, p2_ELO):
    adv = 1800  # if you have adv more points than your opponent you are 10 times more likely to win
    k = 50

    pow1 = ((p1_ELO-p2_ELO)/adv)
    exp_score1 = 1/(1+10**pow1)
    p1_win = k*exp_score1  # p1_win is what p1 wins and p2 looses

    pow2 = ((p2_ELO-p1_ELO)/adv)
    exp_score2 = 1/(1+10**pow2)
    p2_win = k*exp_score2  # p2_win is what p2 wins and p1 looses

    return round(p1_win), round(p2_win)


def new_scores(p1_ELO, p2_ELO, winner):  # winner is 'p1' or 'p2'
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

    if p2_ELO_new <= 0:
        p2_ELO_new = 0

    return p1_ELO_new, p2_ELO_new


if __name__ == "__main__":
    p = get_sorted_pongdog_leaderboard()
    print(p)
