-- created_at not shown to users
SELECT restaurant_id,
    name,
    address,
    city,
    state,
    zip_code,
    phone
FROM Restaurants
ORDER BY name;