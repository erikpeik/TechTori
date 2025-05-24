import sqlite3
from flask import g


def get_db_connection():
    con = sqlite3.connect('database.db')
    con.execute('PRAGMA foreign_keys = ON')
    con.row_factory = sqlite3.Row
    return con


def execute_query(query, params=()):
    con = get_db_connection()
    result = con.execute(query, params)
    con.commit()
    g.last_insterted_id = result.lastrowid
    con.close()


def last_insert_id():
    return g.last_insterted_id


def fetch_query(query, params=()):
    con = get_db_connection()
    result = con.execute(query, params)
    rows = result.fetchall()
    con.close()
    return rows
