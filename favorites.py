from flask import session
import db


def get_favorited_ids():
    user_id = session.get('user_id', None)
    if user_id is None:
        return []

    sql = """
    SELECT listing_id
    FROM favorites
    WHERE user_id = ?
    """
    res = db.fetch_query(sql, (user_id,))
    return [row[0] for row in res]


def is_favorited(listing_id):
    user_id = session.get('user_id', None)
    if user_id is None:
        return False

    sql = """
    SELECT 1
    FROM favorites
    WHERE user_id = ? AND listing_id = ?
    """
    result = db.fetch_query(sql, (user_id, listing_id))
    return len(result) > 0


def remove_favorite(listing_id):
    user_id = session.get('user_id', None)
    if user_id is None:
        return

    sql = """
    DELETE FROM favorites
    WHERE user_id = ? AND listing_id = ?
    """
    db.execute_query(sql, (user_id, listing_id))


def add_favorite(listing_id):
    user_id = session.get('user_id', None)
    if user_id is None:
        return

    sql = """
    INSERT INTO favorites (user_id, listing_id)
    VALUES (?, ?)
    """
    db.execute_query(sql, (user_id, listing_id))
