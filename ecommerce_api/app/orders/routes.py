import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.dependencies import get_current_normal_user
from app.auth.models import User
from app.orders.models import Order
from app.orders.schemas import OrderOut

router = APIRouter(prefix="/orders", tags=["Orders"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[OrderOut])
def get_order_history(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_normal_user)
):
    """
    Retrieves all past orders placed by the authenticated user.

    Args:
        db (Session): Active database session.
        user (User): The currently authenticated user.

    Returns:
        List[OrderOut]: A list of the user's previous orders.
    """
    logger.info(f"User {user.id} is retrieving their order history.")
    orders = db.query(Order).filter(Order.user_id == user.id).all()
    return orders


@router.get("/{order_id}", response_model=OrderOut)
def get_order_details(
    order_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_normal_user)
):
    """
    Retrieves the details of a specific order by its ID.

    Args:
        order_id (int): ID of the order to retrieve.
        db (Session): Active database session.
        user (User): The currently authenticated user.

    Returns:
        OrderOut: Full details of the specified order.

    Raises:
        HTTPException: If the order does not exist or does not belong to the user.
    """
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()

    if not order:
        logger.warning(f"User {user.id} attempted to access nonexistent order {order_id}.")
        raise HTTPException(status_code=404, detail="Order not found")

    logger.info(f"User {user.id} viewed order {order_id}.")
    return order
