import db


def get_categories():
    sql = "SELECT id, name FROM categories"
    return db.fetch_query(sql)
