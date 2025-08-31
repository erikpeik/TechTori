from flask import session
import db
from datetime import datetime


def get_listings(search, category, condition, exclude_own, page, page_size):
    user_id = session.get('user_id', None)
    offset = (page - 1) * page_size
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
            listings.is_sold,
            CASE WHEN favorites.id IS NOT NULL THEN TRUE ELSE FALSE END AS is_favorited
    FROM listings
    JOIN users ON listings.user_id = users.id
    JOIN conditions ON listings.condition_id = conditions.id
    JOIN categories ON listings.category_id = categories.id
    LEFT JOIN favorites ON favorites.listing_id = listings.id AND favorites.user_id = ?
    """

    where = ["listings.is_sold = FALSE"]
    params = [user_id]

    if exclude_own and user_id is not None:
        where.append("listings.user_id IS NOT ?")
        params.append(user_id)
    if search:
        where.append("listings.title LIKE ?")
        params.append(f"%{search}%")
    if category:
        where.append("listings.category_id = ?")
        params.append(category)
    if condition:
        where.append("listings.condition_id = ?")
        params.append(condition)

    sql += "\nWHERE " + " AND ".join(where) + \
        "\nORDER BY listings.created_at DESC" + \
        "\nLIMIT ? OFFSET ?"

    params.append(page_size)
    params.append(offset)

    return db.fetch_query(sql, tuple(params))


def listing_count(search, category, condition, exclude_own):
    user_id = session.get('user_id', None)
    sql = """
    SELECT COUNT(*) as count
    FROM listings
    JOIN users ON listings.user_id = users.id
    JOIN conditions ON listings.condition_id = conditions.id
    JOIN categories ON listings.category_id = categories.id
    WHERE listings.is_sold = FALSE
    """

    params = []

    if exclude_own and user_id is not None:
        sql += " AND listings.user_id IS NOT ?"
        params.append(user_id)
    if search:
        sql += " AND listings.title LIKE ?"
        params.append(f"%{search}%")
    if category:
        sql += " AND listings.category_id = ?"
        params.append(category)
    if condition:
        sql += " AND listings.condition_id = ?"
        params.append(condition)

    res = db.fetch_query(sql, tuple(params))
    return res[0]["count"] if res else 0


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
