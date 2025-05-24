import sqlite3


def get_db_connection():
    con = sqlite3.connect('database.db')
    con.execute('PRAGMA foreign_keys = ON')
    con.row_factory = sqlite3.Row
    return con


def initialize_database():
    con = get_db_connection()

    with open('schema.sql', encoding="utf-8") as f:
        schema_script = f.read()

    con.executescript(schema_script)

    with open('init.sql', encoding="utf-8") as f:
        init_script = f.read()

    con.executescript(init_script)


if __name__ == '__main__':
    initialize_database()
