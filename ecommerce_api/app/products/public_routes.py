import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.products import models, schemas

router = APIRouter(prefix="/products", tags=["Public Products"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[schemas.ProductOut])
def list_products(
    db: Session = Depends(get_db),
    category: str = None,
    min_price: float = None,
    max_price: float = None,
    sort_by: str = Query("id", enum=["id", "price", "name"]),
    page: int = 1,
    page_size: int = 10
):
    """
    Retrieves a paginated list of products with optional filters.

    Args:
        db (Session): Database session.
        category (str, optional): Filter by product category.
        min_price (float, optional): Minimum price filter.
        max_price (float, optional): Maximum price filter.
        sort_by (str): Field to sort by (id, price, name).
        page (int): Page number for pagination.
        page_size (int): Number of items per page.

    Returns:
        List[ProductOut]: Filtered and paginated list of products.
    """
    query = db.query(models.Product)

    if category:
        query = query.filter(models.Product.category == category)
    if min_price:
        query = query.filter(models.Product.price >= min_price)
    if max_price:
        query = query.filter(models.Product.price <= max_price)

    if sort_by == "price":
        query = query.order_by(models.Product.price)
    elif sort_by == "name":
        query = query.order_by(models.Product.name)
    else:
        query = query.order_by(models.Product.id)

    total = query.count()  # Total matching products
    offset = (page - 1) * page_size

    if offset >= total and total > 0:
        raise HTTPException(status_code=404, detail="Page out of range")
    
    logger.info(f"Listing products - category: {category}, page: {page}, size: {page_size}")
    return query.offset(offset).limit(page_size).all()


@router.get("/search", response_model=List[schemas.ProductOut])
def search_products(keyword: str, db: Session = Depends(get_db)):
    """
    Searches for products by keyword in the product name.

    Args:
        keyword (str): Search keyword.
        db (Session): Database session.

    Returns:
        List[ProductOut]: List of matching products.
    """
    logger.info(f"Product search initiated with keyword: {keyword}")
    return db.query(models.Product).filter(models.Product.name.ilike(f"%{keyword}%")).all()


@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product_detail(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieves details for a specific product by ID.

    Args:
        product_id (int): ID of the product to retrieve.
        db (Session): Database session.

    Returns:
        ProductOut: Product detail.

    Raises:
        HTTPException: If the product is not found.
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        logger.warning(f"Product ID {product_id} not found.")
        raise HTTPException(status_code=404, detail="Product not found")

    logger.info(f"Fetched details for product ID {product_id}")
    return product
