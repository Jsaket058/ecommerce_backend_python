from typing import Optional
from pydantic import BaseModel

class ProductCreate(BaseModel):
    """
    Schema for creating a new product.

    Fields:
        name (str): Name of the product.
        description (str): Description of the product.
        price (float): Price of the product.
        stock (int): Available stock quantity.
        category (str): Product category label.
        image_url (str): URL to the product image.
    """
    name: str
    description: str
    price: float
    stock: int
    category: str
    image_url: str
    


class ProductUpdate(BaseModel):
    """
    Schema for updating an existing product.
    All fields are optional to allow partial updates.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None
    image_url: Optional[str] = None


class ProductOut(ProductCreate):
    """
    Schema for returning product data in API responses.

    Inherits:
        All fields from ProductCreate.

    Adds:
        id (int): Unique product identifier.
    """
    id: int

    model_config = {
        "from_attributes": True
    }
