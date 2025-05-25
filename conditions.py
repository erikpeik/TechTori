import db


def get_conditions():
    sql = "SELECT id, name FROM conditions"
    return db.fetch_query(sql)
