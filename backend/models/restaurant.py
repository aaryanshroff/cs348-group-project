from dataclasses import dataclass
from datetime import datetime

@dataclass
class Restaurant:
    restaurant_id: int
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    phone: str
    created_at: datetime


MOCK_RESTAURANTS = [
    Restaurant(
        restaurant_id=1,
        name="Pizza Palace",
        address="123 Main St",
        city="New York",
        state="NY",
        zip_code="10001",
        phone="212-555-1234",
        created_at=datetime(2025, 1, 28)
    ),
    Restaurant(
        restaurant_id=2,
        name="Taco Tower",
        address="456 Oak Ave",
        city="Los Angeles",
        state="CA",
        zip_code="90001",
        phone="213-555-5678",
        created_at=datetime(2025, 1, 28)
    ),
]