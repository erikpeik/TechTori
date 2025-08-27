from werkzeug.security import check_password_hash, generate_password_hash

import db


def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute_query(sql, (username, password_hash))
    return db.last_insert_id()


def authenticate_user(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.fetch_query(sql, (username,))
    if not result:
        return None

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]

    if check_password_hash(password_hash, password):
        return user_id

    return None


def get_user_info(user_id):
    sql = "SELECT id, username, created_at FROM users WHERE id = ?"
    result = db.fetch_query(sql, (user_id,))
    if not result:
        return None
    return result[0]


def get_user_by_username(username):
    sql = "SELECT id, username, created_at FROM users WHERE username = ?"
    result = db.fetch_query(sql, (username,))
    if not result:
        return None
    return result[0]
