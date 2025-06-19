import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.cart import models, schemas
from app.core.database import get_db
from app.auth.dependencies import get_current_normal_user
from app.auth.models import User

router = APIRouter(prefix="/cart", tags=["Cart"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=schemas.CartOut)
def add_to_cart(
    item: schemas.CartAdd,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_normal_user)
):
    """
    Adds a product to the user's cart. If the product already exists, updates the quantity.

    Args:
        item (CartAdd): Product ID and quantity to add.
        db (Session): Database session.
        user (User): Current authenticated user.

    Returns:
        CartOut: Updated or newly added cart item.
    """
    existing = db.query(models.CartItem).filter_by(
        user_id=user.id, product_id=item.product_id
    ).first()

    if existing:
        existing.quantity += item.quantity
        logger.info(f"Updated quantity for product {item.product_id} in user {user.id}'s cart.")
    else:
        existing = models.CartItem(
            user_id=user.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(existing)
        logger.info(f"Added product {item.product_id} to user {user.id}'s cart.")

    db.commit()
    db.refresh(existing)
    return existing


@router.get("/", response_model=list[schemas.CartOut])
def view_cart(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_normal_user)
):
    """
    Retrieves all cart items for the current user.

    Args:
        db (Session): Database session.
        user (User): Current authenticated user.

    Returns:
        list[CartOut]: List of cart items for the user.
    """
    return db.query(models.CartItem).filter_by(user_id=user.id).all()


@router.put("/{product_id}", response_model=schemas.CartOut)
def update_cart_quantity(
    product_id: int,
    item: schemas.CartQuantityUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_normal_user)
):
    """
    Updates the quantity of a specific product in the user's cart.

    Args:
        product_id (int): ID of the product to update.
        item (CartAdd): New quantity to set.
        db (Session): Database session.
        user (User): Current authenticated user.

    Returns:
        CartOut: Updated cart item.

    Raises:
        HTTPException: If the item is not found in the cart.
    """
    cart_item = db.query(models.CartItem).filter_by(
        user_id=user.id, product_id=product_id
    ).first()
    
    if not cart_item:
        logger.warning(f"User {user.id} attempted to update non-existent cart item {product_id}.")
        raise HTTPException(status_code=404, detail="Item not found in cart")

    cart_item.quantity = item.quantity
    db.commit()
    db.refresh(cart_item)
    logger.info(f"Updated quantity for cart item {product_id} for user {user.id}.")
    return cart_item


@router.delete("/{product_id}")
def remove_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_normal_user)
):
    """
    Removes a product from the user's cart.

    Args:
        product_id (int): ID of the product to remove.
        db (Session): Database session.
        user (User): Current authenticated user.

    Returns:
        dict: Confirmation message.

    Raises:
        HTTPException: If the item is not found in the cart.
    """
    cart_item = db.query(models.CartItem).filter_by(
        user_id=user.id, product_id=product_id
    ).first()
    
    if not cart_item:
        logger.warning(f"User {user.id} attempted to delete non-existent cart item {product_id}.")
        raise HTTPException(status_code=404, detail="Item not found in cart")

    db.delete(cart_item)
    db.commit()
    logger.info(f"Removed product {product_id} from user {user.id}'s cart.")
    return {"message": "Item removed from cart"}
