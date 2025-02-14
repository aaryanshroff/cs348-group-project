-- created_at not shown to users
SELECT r.restaurant_id,
    r.name,
    r.address,
    r.city,
    r.state,
    r.zip_code,
    r.phone,
    GROUP_CONCAT(rt.type_name) AS types
FROM Restaurants r
    LEFT JOIN RestaurantTypeAssignments rta ON r.restaurant_id = rta.restaurant_id
    LEFT JOIN RestaurantTypes rt ON rta.type_id = rt.type_id
GROUP BY r.restaurant_id -- In SQLite, you can use any attribute in SELECT if you GROUP BY a primary key
ORDER BY r.name;