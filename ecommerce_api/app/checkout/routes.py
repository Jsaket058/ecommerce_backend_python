import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.dependencies import get_current_normal_user
from app.auth.models import User
from app.cart.models import CartItem
from app.orders.models import Order, OrderItem
from app.products.models import Product
router = APIRouter(prefix="/checkout", tags=["Checkout"])
logger = logging.getLogger(__name__)


@router.post("/")
def checkout(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_normal_user)
):
    """
    Converts user's cart into a completed order and clears the cart.

    Args:
        db (Session): Database session.
        user (User): Authenticated user.

    Returns:
        dict: Success message with new order ID.

    Raises:
        HTTPException: If the cart is empty or any product is not found.
    """
    cart_items = db.query(CartItem).filter(CartItem.user_id == user.id).all()

    if not cart_items:
        logger.warning(f"Checkout failed: Cart is empty for user {user.id}.")
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0
    for item in cart_items:
        total += item.quantity * get_product_price(db, item.product_id)

    new_order = Order(user_id=user.id, total_amount=total)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    logger.info(f"New order {new_order.id} created for user {user.id} with total {total}.")

    for item in cart_items:
        price = get_product_price(db, item.product_id)
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=price
        )
        db.add(order_item)

    db.query(CartItem).filter(CartItem.user_id == user.id).delete()
    db.commit()
    logger.info(f"Cart cleared for user {user.id} after successful checkout.")

    return {"message": "Checkout successful", "order_id": new_order.id}


def get_product_price(db: Session, product_id: int) -> float:
    """
    Retrieves the current price of a product.

    Args:
        db (Session): Database session.
        product_id (int): ID of the product.

    Returns:
        float: Current product price.

    Raises:
        HTTPException: If the product does not exist.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        logger.warning(f"Product {product_id} not found during checkout.")
        raise HTTPException(status_code=404, detail="Product not found")
    return product.price
