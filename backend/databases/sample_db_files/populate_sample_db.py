import csv
import os
import sys
import sqlite3

############################ SAMPLE CSV SETUP ############################
INSERT_USERS = """
INSERT INTO Users (uid, username, first_name, last_name, email, password_hash, created_at)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

INSERT_RESTAURANTS = """
INSERT INTO Restaurants (restaurant_id, name, address, city, state, zip_code, phone, avg_rating, created_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

INSERT_RESTAURANT_TYPES = """
INSERT INTO RestaurantTypes (type_id, type_name, created_at)
VALUES (?, ?, ?)
"""

INSERT_RESTAURANT_TYPES_ASSIGNMENTS = """
INSERT INTO RestaurantTypesAssignments (restaurant_id, type_id, created_at)
VALUES (?, ?, ?)
"""

INSERT_REVIEWS = """
INSERT INTO Reviews (uid, restaurant_id, rating, review_text, created_at)
VALUES (?, ?, ?, ?, ?)
"""

INSERT_FOLLOWS = """
INSERT INTO Follows (follower_id, followed_id, created_at)
VALUES (?, ?, ?)
"""

INSERT_RESTAURANTS_FTS_REBUILD = """
-- Rebuilds the search index
INSERT INTO restaurants_fts(restaurants_fts) VALUES('rebuild');
"""

CWD = os.getcwd()
SAMPLE_DB_FILES = os.path.join( CWD, "sample_db_files" )

SAMPLE_DATASET = os.path.join( CWD, "sample_dataset.db" )
SAMPLE_CSV_DIR = os.path.join( SAMPLE_DB_FILES, "sample_csv_files" )

csv_files = ['sample_users.csv',
             'sample_restaurants.csv',
             'sample_restaurant_types.csv',
             'sample_restaurant_types_assignments.csv',
             'sample_reviews.csv',
             'sample_follows.csv']

for i in range(len(csv_files)):
    csv_files[i] = os.path.join( SAMPLE_CSV_DIR, csv_files[i] )

QUERIES = [INSERT_USERS,
           INSERT_RESTAURANTS,
           INSERT_RESTAURANT_TYPES,
           INSERT_RESTAURANT_TYPES_ASSIGNMENTS,
           INSERT_REVIEWS,
           INSERT_FOLLOWS]

# We only assert that every file has a corresponding query
# Any file DNE, permissions, or syntactic errors should be caught in our try-catch
assert( len( csv_files ) == len( QUERIES ) )

############################ SAMPLE DB POPULATION ############################
try:
    # Try connect to locally stored sample dataset
    conn = sqlite3.connect( SAMPLE_DATASET )
    cursor = conn.cursor()

    for i in range( len( csv_files ) ):
        with open( csv_files[i], 'r' ) as file:
            csv_reader = csv.reader( file )

            data = [tuple(row) for row in csv_reader]
            
            cursor.executemany( QUERIES[i], data )
    
    cursor.execute(INSERT_RESTAURANTS_FTS_REBUILD);

    conn.commit()
    if conn:
        conn.close()
except sqlite3.Error as e:
    print( f"FAILED: populate_sample_db.py: {e}" )

    if conn:
        conn.close()

    sys.exit( 1 )

sys.exit( 0 )
