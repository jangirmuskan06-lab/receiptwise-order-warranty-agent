

import sqlite3
from datetime import date, datetime, timedelta

from langchain_core.tools import tool


# These policy values match data/policy.txt
RETURN_POLICY_DAYS = {
    "clothing": 30,
    "electronics": 14,
}

WARRANTY_DAYS = 365


@tool
def calculate_return_warranty_window(
    item_name: str,
    category: str,
    purchase_date: str,
    window_type: str = "return",
) -> dict:
    """
    Computes the return or warranty window using purchase date + policy days.
    Clothing returns use 30 policy days, electronics returns use 14 policy days,
    and warranties use 365 policy days. Windows with fewer than 7 days left
    are flagged as expiring soon.
    """
    try:
        purchased_on = datetime.strptime(purchase_date, "%Y-%m-%d").date()
    except ValueError:
        return {
            "success": False,
            "error": "Purchase date must use YYYY-MM-DD format."
        }

    category_key = category.strip().lower()
    selected_window = window_type.strip().lower()

    if selected_window == "warranty":
        policy_days = WARRANTY_DAYS
    elif selected_window == "return":
        policy_days = RETURN_POLICY_DAYS.get(category_key)
        if policy_days is None:
            return {
                "success": False,
                "item": item_name,
                "error": f"No return policy exists for category: {category}."
            }
    else:
        return {
            "success": False,
            "item": item_name,
            "error": "Window type must be return or warranty."
        }

    deadline = purchased_on + timedelta(days=policy_days)
    days_remaining = (deadline - date.today()).days

    return {
        "success": True,
        "item": item_name,
        "category": category,
        "window_type": selected_window,
        "purchase_date": purchase_date,
        "policy_days": policy_days,
        "deadline": deadline.isoformat(),
        "days_remaining": days_remaining,
        "expiring_soon": 0 <= days_remaining < 7,
        "expired": days_remaining < 0,
    }


@tool
def lookup_order_status(order_id: str) -> dict:
    """
    Looks up an order's status from the mock order database using its order ID.
    Returns a clear not-found response rather than inventing an order status.
    """
    try:
        connection = sqlite3.connect("data/orders.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT order_id, customer_name, status, tracking_number, estimated_delivery
            FROM orders
            WHERE order_id = ?
        """, (order_id.strip(),))

        row = cursor.fetchone()
        connection.close()

        if row is None:
            return {
                "found": False,
                "message": f"No order found for ID {order_id}."
            }

        return {
            "found": True,
            "order_id": row[0],
            "customer_name": row[1],
            "status": row[2],
            "tracking_number": row[3],
            "estimated_delivery": row[4],
        }

    except sqlite3.Error as error:
        return {
            "found": False,
            "message": f"Order lookup could not be completed: {error}"
        }