from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base


class Product(Base):
    """
    SQLAlchemy model for the 'products' table.

    Attributes:
        id (int): Primary key of the product.
        name (str): Product name (required).
        description (str): Description of the product.
        price (float): Price of the product.
        stock (int): Inventory count.
        category (str): Product category or type.
        image_url (str): URL to the product's image.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    category = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
