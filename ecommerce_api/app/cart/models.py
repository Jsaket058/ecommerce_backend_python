from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base

class CartItem(Base):
    """
    SQLAlchemy model for representing a single item in a user's shopping cart.

    Attributes:
        id (int): Primary key.
        user_id (int): Foreign key to the user who owns the cart.
        product_id (int): Foreign key to the product added to the cart.
        quantity (int): Quantity of the product in the cart.
    """
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
