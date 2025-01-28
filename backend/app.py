from dataclasses import asdict
from datetime import datetime
from flask import Flask, request
from flask_cors import CORS

from models.restaurant import MOCK_RESTAURANTS, Restaurant

app = Flask(__name__)

# Enables CORS for all domains on all routes
# Read more: https://github.com/corydolphin/flask-cors?tab=readme-ov-file#simple-usage
CORS(app)

@app.get('/api/hello')
def hello():
    return {
        "message": "Hello from Flask"
    }

@app.get('/api/restaurants')
def get_restaurants():
    try:
        # Not guaranteed lower-case, use LOWER() in DB query
        search_term = request.args.get('q', '').strip() or None
        results = _search_restaurants(search_term)
        return {
            'data': [asdict(r) for r in results]
        }, 200
    except Exception as e:
        return {
            'error': str(e)
        }, 500

def _search_restaurants(search_term: str | None = None) -> list[Restaurant]:
    if not search_term:
        return MOCK_RESTAURANTS
    
    search = search_term.lower()
    return [
        r for r in MOCK_RESTAURANTS
        if (search in r.name.lower() or 
            search in r.address.lower() or
            search in r.city.lower() or
            search in r.state.lower())
    ]

# MySQL query for future implementation
SEARCH_QUERY = """
    -- created_at not shown to users
    SELECT restaurant_id, name, address, city, state, zip_code, phone
    FROM restaurants
    WHERE 
        LOWER(name) LIKE CONCAT('%', LOWER(%s), '%') OR
        LOWER(address) LIKE CONCAT('%', LOWER(%s), '%') OR
        LOWER(city) LIKE CONCAT('%', LOWER(%s), '%') OR
        LOWER(state) LIKE CONCAT('%', LOWER(%s), '%')
    ORDER BY name
"""

GET_ALL_QUERY = """
    -- created_at not shown to users
    SELECT restaurant_id, name, address, city, state, zip_code, phone
    FROM restaurants
    ORDER BY name
"""


if __name__ == '__main__':
    app.run(debug=True)