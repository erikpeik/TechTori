DROP TABLE IF EXISTS listings_categories;
DROP TABLE IF EXISTS listings;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS conditions;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE conditions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    condition_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (condition_id) REFERENCES conditions(id)
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE listings_categories (
    listing_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (listing_id, category_id),
    FOREIGN KEY (listing_id) REFERENCES listings(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE INDEX idx_listing_title ON listings(title);
CREATE INDEX idx_category_name ON categories(name);
