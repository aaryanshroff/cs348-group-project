from datetime import datetime
from typing import TypedDict

class Restaurant(TypedDict):
    restaurant_id: int
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    phone: str
    created_at: datetime