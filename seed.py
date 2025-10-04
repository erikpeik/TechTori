import random
import secrets
import sqlite3

DB = sqlite3.connect("database.db")

DB.execute("DELETE FROM users")
DB.execute("DELETE FROM listings")


USER_COUNT = 1000
LISTING_COUNT = 10**5
FAVORITE_COUNT = 10**5

for i in range(1, USER_COUNT + 1):
    password_hash = secrets.token_hex(16)
    DB.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
               ["user" + str(i), password_hash])

for i in range(1, LISTING_COUNT + 1):
    user_id = random.randint(1, USER_COUNT)
    category_id = random.randint(1, 11)
    condition_id = random.randint(1, 4)
    listing_price = random.randint(1, 10000)
    DB.execute("""
               INSERT INTO listings (title, user_id, category_id, condition_id, price)
               VALUES (?, ?, ?, ?, ?)
               """,
               ["listing" + str(i), user_id, category_id, condition_id, listing_price])

for i in range(1, FAVORITE_COUNT + 1):
    user_id = random.randint(1, USER_COUNT)
    listing_id = random.randint(1, LISTING_COUNT)
    DB.execute("""INSERT INTO favorites (user_id, listing_id)
                  VALUES (?, ?)""",
               [user_id, listing_id])

DB.commit()
DB.close()
