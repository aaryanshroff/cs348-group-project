from pathlib import Path

import db
from flask import Flask, request
from flask_cors import CORS
from models.restaurant import Restaurant

app = Flask(__name__)
db.init_app(app)


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
        # SQLite FTS5 is not case-sensitive
        search_term = request.args.get('q', '').strip() or None
        results = _list_restaurants(search_term)
        return {
            'data': results
        }, 200
    except Exception as e:
        print(f"{type(e).__name__}({e})")
        return {
            'error': str(e)
        }, 500

def _list_restaurants(search_term: str | None = None) -> list[Restaurant]:
    sql_file = Path("queries") / "list_restaurants.sql"
    params = ()

    # TODO: Fix FTS
    # if search_term:
    #     sql_file = Path("queries") / "search_restaurants.sql"
    #     params = (search_term,)
        
    query = sql_file.read_text(encoding="utf-8")
    rows = db.query_db(query, args=params)
    return [dict(row) for row in rows]

if __name__ == '__main__':
    app.run(debug=True)