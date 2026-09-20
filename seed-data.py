import sqlite3
from pathlib import Path

Path("data").mkdir(exist_ok=True)

connection = sqlite3.connect("data/orders.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    status TEXT NOT NULL,
    tracking_number TEXT,
    estimated_delivery TEXT
)
""")

orders = [
    (
        "ORD-1001",
        "Pre",
        "Shipped",
        "TRK-987654",
        "2026-09-24"
    ),
    (
        "ORD-1002",
        "Pre",
        "Delivered",
        "TRK-123456",
        "2026-09-18"
    )
]

cursor.executemany("""
INSERT OR REPLACE INTO orders
(order_id, customer_name, status, tracking_number, estimated_delivery)
VALUES (?, ?, ?, ?, ?)
""", orders)

connection.commit()
connection.close()

print("Mock order database created: data/orders.db")
print("Sample orders added: ORD-1001 and ORD-1002")