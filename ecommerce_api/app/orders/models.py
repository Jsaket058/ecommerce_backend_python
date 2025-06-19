from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime , timezone
from app.core.database import Base
import enum


class OrderStatus(str, enum.Enum):
    """
    Enum for defining the status of an order.

    Attributes:
        pending (str): Order has been created but not paid.
        paid (str): Order has been successfully paid.
        cancelled (str): Order has been cancelled before fulfillment.
    """
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"


class Order(Base):
    """
    SQLAlchemy model for the 'orders' table.

    Attributes:
        id (int): Primary key for the order.
        user_id (int): ID of the user who placed the order.
        total_amount (float): Total cost of all items in the order.
        status (OrderStatus): Current status of the order.
        created_at (datetime): Timestamp of order creation.
        items (List[OrderItem]): Relationship to associated order items.
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float)
    status = Column(Enum(OrderStatus), default=OrderStatus.paid)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    """
    SQLAlchemy model for the 'order_items' table.

    Attributes:
        id (int): Primary key for the order item.
        order_id (int): Foreign key linking to the parent order.
        product_id (int): Foreign key linking to the purchased product.
        quantity (int): Number of units purchased.
        price_at_purchase (float): Price of the product at the time of purchase.
        order (Order): Relationship back to the parent order.
    """
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price_at_purchase = Column(Float)

    order = relationship("Order", back_populates="items")
