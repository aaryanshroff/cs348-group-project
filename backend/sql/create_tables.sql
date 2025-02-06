DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Restaurants;
DROP TABLE IF EXISTS RestaurantImages;
DROP TABLE IF EXISTS RestaurantTypes;
DROP TABLE IF EXISTS RestaurantTypeAssignments;
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Followers;

-- Create tables required by the application
CREATE TABLE Users (
  uid INT NOT NULL PRIMARY KEY,
  username TEXT UNIQUE,
  first_name TEXT NOT NULL,
  last_name TEXT,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE Restaurants (
  restaurant_id INT NOT NULL PRIMARY KEY,
  name TEXT NOT NULL,
  address TEXT,
  city TEXT,
  state TEXT,
  zip_code TEXT,
  phone TEXT,
  created_at TEXT NOT NULL,
  average_rating DECIMAL(3, 2) CHECK(average_rating IS NULL OR average_rating = 0 OR average_rating BETWEEN 1 and 5)
);

CREATE TABLE RestaurantImages (
  image_id INT NOT NULL PRIMARY KEY,
  restaurant_id INT NOT NULL REFERENCES Restaurants(restaurant_id),
  image_url TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE RestaurantTypes (
  type_id INT NOT NULL PRIMARY KEY,
  type_name TEXT NOT NULL
);

CREATE TABLE RestaurantTypeAssignments (
  restaurant_id INT NOT NULL REFERENCES Restaurants(restaurant_id),
  type_id INT NOT NULL REFERENCES RestaurantTypes(type_id),
  PRIMARY KEY(restaurant_id, type_id)
);

CREATE TABLE Reviews (
  uid INT NOT NULL REFERENCES Users(uid),
  restaurant_id INT NOT NULL REFERENCES Restaurants(restaurant_id),
  rating INT NOT NULL CHECK(rating BETWEEN 1 AND 5),
  review_text TEXT,
  created_at TEXT NOT NULL,
  PRIMARY KEY(uid, restaurant_id)
);

CREATE TABLE Followers (
  uid INT NOT NULL REFERENCES Users(uid),
  follower_id INT NOT NULL REFERENCES Users(uid),
  CHECK(uid != follower_id)
);
