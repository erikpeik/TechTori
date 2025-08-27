from flask import session
import db
from datetime import datetime


def get_listings():
    user_id = session.get('user_id', None)
    sql = """
    SELECT  listings.id,
            listings.user_id,
            users.username AS username,
            listings.title,
            listings.description,
            listings.price,
            conditions.name AS condition,
            categories.name AS category,
            listings.created_at,
            listings.is_sold
    FROM listings
    JOIN users ON listings.user_id = users.id
    JOIN conditions ON listings.condition_id = conditions.id
    JOIN categories ON listings.category_id = categories.id
    WHERE listings.user_id IS NOT ? AND listings.is_sold = FALSE
    """
    return db.fetch_query(sql, (user_id,))


def add_listing(user_id, title, description, price, condition_id, category_id):
    sql = """
    INSERT INTO listings (user_id, title, description, price, condition_id, category_id)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    db.execute_query(sql, (user_id, title, description,
                     price, condition_id, category_id))
    return db.last_insert_id()


def get_listing(listing_id):
    sql = """
    SELECT  listings.id,
            listings.user_id,
            users.username AS username,
            listings.title,
            listings.description,
            listings.price,
            conditions.name AS condition,
            categories.name AS category,
            listings.category_id,
            listings.condition_id,
            listings.created_at,
            listings.is_sold
    FROM listings
    JOIN users ON listings.user_id = users.id
    JOIN conditions ON listings.condition_id = conditions.id
    JOIN categories ON listings.category_id = categories.id
    WHERE listings.id = ?
    """
    res = db.fetch_query(sql, (listing_id,))

    res = res[0] if res else None

    if res is not None:
        dt = datetime.strptime(res['created_at'], '%Y-%m-%d %H:%M:%S')
        res = dict(res)
        res['created_at'] = dt.strftime('%d.%m.%Y %H:%M:%S')
    return res


def update_listing(listing_id, title, description, price, condition_id, category_id):
    sql = """
    UPDATE listings
    SET title = ?, description = ?, price = ?, condition_id = ?, category_id = ?
    WHERE id = ?
    """
    db.execute_query(sql, (title, description, price,
                     condition_id, category_id, listing_id))


def mark_listing_as_sold(listing_id):
    sql = """
    UPDATE listings
    SET is_sold = TRUE, sold_by_user_id = ?
    WHERE id = ?
    """
    db.execute_query(sql, (session["user_id"], listing_id))


def mark_listing_as_unsold(listing_id):
    sql = """
    UPDATE listings
    SET is_sold = FALSE, sold_by_user_id = NULL
    WHERE id = ?
    """
    db.execute_query(sql, (listing_id,))


def delete_listing(listing_id):
    sql = """
    DELETE FROM listings
    WHERE id = ?
    """
    db.execute_query(sql, (listing_id,))


def get_user_listings(user_id):
    sql = """
    SELECT  listings.id,
            listings.user_id,
            listings.title,
            listings.description,
            listings.price,
            conditions.name AS condition,
            categories.name AS category,
            listings.created_at,
            listings.is_sold
    FROM listings
    JOIN conditions ON listings.condition_id = conditions.id
    JOIN categories ON listings.category_id = categories.id
    WHERE listings.user_id = ?
    """
    return db.fetch_query(sql, (user_id,))


def is_listing_sold(listing_id):
    sql = """
    SELECT is_sold
    FROM listings
    WHERE id = ?
    """
    res = db.fetch_query(sql, (listing_id,))
    return res[0]["is_sold"] if res else None
