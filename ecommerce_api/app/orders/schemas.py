from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderItemOut(BaseModel):
    """
    Schema representing an individual item within an order.

    Fields:
        product_id (int): ID of the product ordered.
        quantity (int): Number of units purchased.
        price_at_purchase (float): Price per unit at the time of purchase.
    """
    product_id: int
    quantity: int
    price_at_purchase: float

    model_config = {"from_attributes": True}


class OrderOut(BaseModel):
    """
    Schema representing an order, including its items and metadata.

    Fields:
        id (int): Unique ID of the order.
        total_amount (float): Total cost of the order.
        status (str): Current status of the order (e.g., paid, cancelled).
        created_at (datetime): Timestamp of when the order was placed.
        items (List[OrderItemOut]): List of products in the order.
    """
    id: int
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemOut]

    model_config = {"from_attributes": True}
