-- Adding a Restaurant Query
INSERT INTO Restaurants (restaurant_id, name, address, city, state, zip_code, phone, average_rating)
VALUES(1, 'McDonalds', '123 Rose St', 'Toronto', 'ON', '11111', '111-111-1111', 0.0);

INSERT INTO RestaurantImages(image_id, restaurant_id, image_url)
VALUES(1, 1, 'image_url');

-- Adding a Review Query
INSERT INTO Reviews (uid, restaurant_id, rating, review_text)
VALUES (1, 1, 5, 'great store');

-- Finding all reviews for a Restaurant Query to show on the page:
SELECT * FROM Reviews WHERE restaurant_id = 1;

-- Finding the current user’s reviews for a restaurant:
SELECT * FROM Reviews WHERE restaurant_id = 1 AND uid = 1;

-- R7 List all restaurants and filter restaurants by city and type (Aaryan)

-- 1. List all restaurants
SELECT restaurant_id,
    name,
    address,
    city,
    state,
    zip_code,
    phone
FROM Restaurants
ORDER BY name;

-- 2. Generate filter options
SELECT DISTINCT(city)
FROM Restaurants
ORDER BY city;
SELECT DISTINCT(type_name)
FROM RestaurantTypes
ORDER BY type_name;

-- 3. List restaurants from city :city
SELECT restaurant_id,
    name,
    address,
    city,
    state,
    zip_code,
    phone
FROM Restaurants
WHERE city = 'Phoenix';

-- 4. List restaurants of type :type_name
SELECT Restaurants.*
FROM Restaurants
INNER JOIN RestaurantTypesAssignments 
  ON Restaurants.restaurant_id = RestaurantTypesAssignments.restaurant_id
INNER JOIN RestaurantTypes 
  ON RestaurantTypesAssignments.type_id = RestaurantTypes.type_id
WHERE RestaurantTypes.type_name = 'augue';