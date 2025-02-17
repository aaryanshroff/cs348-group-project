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
        type_ids = types_param.split(",") if types_param else []

        results = _list_restaurants(search_term, type_ids)

        return {"data": results}, 200
    except Exception as e:
        print(f"{type(e).__name__}({e})")
        return {"error": str(e)}, 500


def _list_restaurants(
    search_term: str = "", type_ids: list[int] = []
) -> list[Restaurant]:
    if len(type_ids) == 0:
        sql_file = Path("queries") / "list_restaurants.sql"
        return db.query_db_from_file(sql_file)

    placeholders = ", ".join(["?"] * len(type_ids))

    sql_file = Path("queries") / "filter_restaurants.sql"
    # NOT SQL injection b/c we only substitute with X number of ?
    # ? substitution is handled by SQLite engine
    query = sql_file.read_text(encoding="utf-8").format(placeholders=placeholders)
    print(query)

    return db.query_db(query, tuple(type_ids))

    # TODO: Fix FTS
    # if search_term:
    #     sql_file = Path("queries") / "search_restaurants.sql"
    #     params = (search_term,)

@app.get("/api/restaurants/add")
def add_restaurant():
    try:
        # SQLite FTS5 is not case-sensitive
        name = request.args.get("name", "").strip()
        address = request.args.get("address", "").strip()
        city = request.args.get("city", "").strip()
        state = request.args.get("state", "").strip()
        zip_code = request.args.get("zip_code", "").strip()
        phone = request.args.get("phone", "").strip()

        results = _add_restaurants(name, address, city, state, zip_code, phone)

        return {"data": results}, 200
    except Exception as e:
        print(f"{type(e).__name__}({e})")
        return {"error": str(e)}, 500

# TODO @dyasin: Implement me
def _add_restaurant(
        name: str = "", address: str = "", city: str = "", state: str = "", zip_code: str = "", phone: str = ""
) -> int:
    if len(type_ids) == 0:
        sql_file = Path("queries") / "list_restaurants.sql"
        return db.query_db_from_file(sql_file)

    placeholders = ", ".join(["?"] * len(type_ids))

    sql_file = Path("queries") / "filter_restaurants.sql"
    # NOT SQL injection b/c we only substitute with X number of ?
    # ? substitution is handled by SQLite engine
    query = sql_file.read_text(encoding="utf-8").format(placeholders=placeholders)
    print(query)

    return db.query_db(query, tuple(type_ids))


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
