import random
import secrets
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM listings")


user_count = 1000
listing_count = 10**5
favorite_count = 10**5

for i in range(1, user_count + 1):
    password_hash = secrets.token_hex(16)
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
               ["user" + str(i), password_hash])

for i in range(1, listing_count + 1):
    user_id = random.randint(1, user_count)
    category_id = random.randint(1, 11)
    condition_id = random.randint(1, 4)
    listing_price = random.randint(1, 10000)
    db.execute("""
               INSERT INTO listings (title, user_id, category_id, condition_id, price)
               VALUES (?, ?, ?, ?, ?)
               """,
               ["listing" + str(i), user_id, category_id, condition_id, listing_price])

for i in range(1, favorite_count + 1):
    user_id = random.randint(1, user_count)
    listing_id = random.randint(1, listing_count)
    db.execute("""INSERT INTO favorites (user_id, listing_id)
                  VALUES (?, ?)""",
               [user_id, listing_id])

db.commit()
db.close()
