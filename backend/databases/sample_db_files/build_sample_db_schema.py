import sqlite3
import os
import sys # Explicitly exiting with error code allows us to catch failures in our setup script

############################ SQL QUERY DEFINITIONS ############################
# For simplicity, we define the setup SQL queries in the same file as the setup script itself

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS Users (
    uid INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

# NOTABLE CONSTRAINTS:
# The combination of name and address is unique, individually name and address are not unique
# Average rating is a real number 
# 1 and 5 or is 0 in the case that no reviews exist for the restaurant.
CREATE_RESTAURANTS_TABLE = """
CREATE TABLE IF NOT EXISTS Restaurants (
    restaurant_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip_code TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE,
    avg_rating REAL NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (name, address)
    CHECK ((avg_rating BETWEEN 1 AND 5) OR (avg_rating IS 0)),
    CHECK (avg_rating = ROUND(avg_rating, 1))
);
"""

CREATE_RESTAURANT_TYPES_TABLE = """
CREATE TABLE IF NOT EXISTS RestaurantTypes (
    type_id INTEGER PRIMARY KEY,
    type_name TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

# NOTABLE CONSTRAINTS:
# A restaurant cannot have the same restaurant type twice. Enforced by PRIMARY KEY
CREATE_RESTAURANT_TYPES_ASSIGNMENTS_TABLE = """
CREATE TABLE IF NOT EXISTS RestaurantTypesAssignments (
    restaurant_id INTEGER NOT NULL,
    type_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id),
    FOREIGN KEY (type_id) REFERENCES RestaurantTypes(type_id),

    PRIMARY KEY (restaurant_id, type_id)
);
"""

# NOTABLE CONSTRAINTS:
# review_text is no longer than 250 chars
# rating is between 1 and 5 inclusive
# only 1 review per user per restaurant
CREATE_REVIEWS_TABLE = """
CREATE TABLE IF NOT EXISTS Reviews (
    uid INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    review_text VARCHAR(250),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (uid) REFERENCES Users(uid),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id),

    CHECK (rating BETWEEN 1 AND 5),

    PRIMARY KEY (uid, restaurant_id)
);
"""

# NOTABLE CONSTRAINTS:
# A user cannot follow the same user more than once, enforced by the PRIMARY KEY
# A user cannot follow themselves
CREATE_FOLLOWS_TABLE = """
CREATE TABLE IF NOT EXISTS Follows (
    follower_id INTEGER NOT NULL,
    followed_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (follower_id) REFERENCES Users(uid),
    FOREIGN KEY (followed_id) REFERENCES Users(uid),

    CHECK (follower_id <> followed_id),

    PRIMARY KEY (follower_id, followed_id)
);
"""

# Full text search

CREATE_RESTAURANTS_FTS_VTABLE = """
-- Creates a virtual table for full-text search that mirrors the Restaurants table.
-- Uses the 'content' option to reference existing data, avoiding duplication.
-- 'content_rowid' links to the primary key of the source table.
CREATE VIRTUAL TABLE restaurants_fts USING fts5(
    name, 
    address, 
    city, 
    state,
    zip_code,
    phone,
    content='restaurants', 
    content_rowid='restaurant_id'
);
"""

CREATE_TRIGGER_RESTAURANTS_FTS_INSERT = """
-- Trigger: Automatically updates FTS index when new restaurants are added.
-- Inserts only the rowid - FTS5 automatically pulls content from source table.
CREATE TRIGGER restaurants_ai AFTER INSERT ON restaurants BEGIN
    INSERT INTO restaurants_fts(rowid) VALUES (new.restaurant_id);
END;
"""

CREATE_TRIGGER_FTS_UPDATE = """
-- Trigger: Handles updates to restaurant data by:
-- 1. Deleting old FTS index entry (using FTS5's 'delete' command)
-- 2. Adding new entry with updated data
CREATE TRIGGER restaurants_au AFTER UPDATE ON restaurants BEGIN
    INSERT INTO restaurants_fts(restaurants_fts, rowid) VALUES('delete', old.restaurant_id);
    INSERT INTO restaurants_fts(rowid) VALUES (new.restaurant_id);
END;
"""


CREATE_TRIGGER_FULL_TEXT_SEARCH_DELETE = """
-- Trigger: Removes entries from FTS index when restaurants are deleted.
-- Uses FTS5's internal 'delete' command rather than standard SQL DELETE.
CREATE TRIGGER restaurants_ad AFTER DELETE ON restaurants BEGIN
    INSERT INTO restaurants_fts(restaurants_fts, rowid) VALUES('delete', old.restaurant_id);
END;
"""

CWD = os.getcwd()

SAMPLE_DATASET = os.path.join( CWD, "sample_dataset.db" )

############################ SAMPLE DB SETUP ############################
try:
    # Try connect to locally stored sample dataset
    conn = sqlite3.connect( SAMPLE_DATASET )
    cursor = conn.cursor()

    # Setup all of the initial tables
    cursor.execute( CREATE_USERS_TABLE )
    cursor.execute( CREATE_RESTAURANTS_TABLE )

    # Full text search
    cursor.execute( CREATE_RESTAURANTS_FTS_VTABLE )
    cursor.execute( CREATE_TRIGGER_RESTAURANTS_FTS_INSERT )
    cursor.execute( CREATE_TRIGGER_FTS_UPDATE )
    cursor.execute( CREATE_TRIGGER_FULL_TEXT_SEARCH_DELETE )

    cursor.execute( CREATE_RESTAURANT_TYPES_TABLE )
    cursor.execute( CREATE_RESTAURANT_TYPES_ASSIGNMENTS_TABLE )
    cursor.execute( CREATE_REVIEWS_TABLE )
    cursor.execute( CREATE_FOLLOWS_TABLE )

    conn.commit()
    if conn:
        conn.close()
except sqlite3.Error as e:
    print( f"FAILED: build_sample_db_schema.py: {e}" )

    if conn:
        conn.close()

    sys.exit( 1 )

sys.exit( 0 )
