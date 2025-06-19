from pydantic import BaseModel, Field


class CartAdd(BaseModel):
    """
    Schema for adding a product to the cart.

    Fields:
        product_id (int): ID of the product to add.
        quantity (int): Quantity of the product to add.
    """
    product_id: int
    quantity: int


class CartOut(BaseModel):
    """
    Schema for representing a cart item in API responses.

    Fields:
        id (int): Unique cart item ID.
        product_id (int): ID of the product in the cart.
        quantity (int): Quantity of the product in the cart.
    """
    id: int
    product_id: int
    quantity: int

    model_config = {
        "from_attributes": True
    }

class CartQuantityUpdate(BaseModel):
    """
    Schema for updating the quantity of an existing cart item.

    Fields:
        quantity (int): New quantity to set for the product.
    """
    quantity: int = Field(..., gt=0, description="New quantity (must be > 0)")

