from pathlib import Path

import db
from flask import Flask, request
from flask_cors import CORS
from models.restaurant import Restaurant, RestaurantType

app = Flask(__name__)
db.init_app(app)


# Enables CORS for all domains on all routes
# Read more: https://github.com/corydolphin/flask-cors?tab=readme-ov-file#simple-usage
CORS(app)


@app.get("/api/hello")
def hello():
    return {"message": "Hello from Flask"}


@app.get("/api/restaurants")
def get_restaurants():
    try:
        # SQLite FTS5 is not case-sensitive
        search_term = request.args.get("q", "").strip()

        types_param = request.args.get("types")
        type_ids = types_param.split(",") if types_param is not None else []

        results = _list_restaurants(search_term, type_ids)

        return {"data": results}, 200
    except Exception as e:
        print(f"{type(e).__name__}({e})")
        return {"error": str(e)}, 500


def _list_restaurants(
    search_term: str = "", type_ids: list[int] = []
) -> list[Restaurant]:
    sql_file = Path("queries") / "list_restaurants.sql"
    params = []

    # TODO: Fix FTS
    # if search_term:
    #     sql_file = Path("queries") / "search_restaurants.sql"
    #     params = (search_term,)

    if len(type_ids) > 0:
        params.append(type_ids)

    return db.query_db_from_file(sql_file, args=params)


@app.get("/api/types")
def get_types():
    try:
        results = _list_types()
        return {"data": results}, 200
    except Exception as e:
        print(f"{type(e).__name__}({e})")
        return {"error": str(e)}, 500


def _list_types() -> list[RestaurantType]:
    sql_file = Path("queries") / "list_types.sql"

    return db.query_db_from_file(sql_file)


if __name__ == "__main__":
    app.run(debug=True)
