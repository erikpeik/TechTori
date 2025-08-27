import db


def get_conditions():
    sql = "SELECT id, name FROM conditions"
    return db.fetch_query(sql)


def get_condition_by_id(condition_id):
    sql = "SELECT id, name FROM conditions WHERE id = ?"
    result = db.fetch_query(sql, (condition_id,))
    if result:
        return result[0]
    return None
