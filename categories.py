import db


def get_categories():
    sql = "SELECT id, name FROM categories"
    return db.fetch_query(sql)


def get_category_by_id(category_id):
    sql = "SELECT id, name FROM categories WHERE id = ?"
    result = db.fetch_query(sql, (category_id,))
    if not result:
        return None
    return result[0]
