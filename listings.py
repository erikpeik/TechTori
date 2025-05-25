import db


def get_listings():
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
            listings.is_active
    FROM listings
    JOIN users ON listings.user_id = users.id
    JOIN conditions ON listings.condition_id = conditions.id
    JOIN categories ON listings.category_id = categories.id
    """
    return db.fetch_query(sql)


def add_listing(user_id, title, description, price, condition_id, category_id):
    sql = """
    INSERT INTO listings (user_id, title, description, price, condition_id, category_id)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    db.execute_query(sql, (user_id, title, description,
                     price, condition_id, category_id))
    return db.last_insert_id()


def mark_listing_as_sold(listing_id):
    sql = """
    UPDATE listings
    SET is_active = 0
    WHERE id = ?
    """
    db.execute_query(sql, (listing_id,))
