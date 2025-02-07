SELECT *
FROM restaurants_fts
WHERE restaurants_fts MATCH :search;