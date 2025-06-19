import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.products import models, schemas
from app.auth.dependencies import get_current_admin_user
from app.core.database import get_db

router = APIRouter(prefix="/admin/products", tags=["Admin - Products"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=schemas.ProductOut)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_admin_user)
):
    """
    Creates a new product in the catalog. Admin only.

    Args:
        product (ProductCreate): Product data to create.
        db (Session): Database session.
        user: Current admin user (injected by dependency).

    Returns:
        ProductOut: The newly created product.
    """
    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    logger.info(f"Admin {user.email} created product '{new_product.name}' (ID: {new_product.id})")
    return new_product


@router.get("/", response_model=list[schemas.ProductOut])
def list_products(
    db: Session = Depends(get_db),
    user=Depends(get_current_admin_user)
):
    """
    Lists all products for administrative purposes.

    Args:
        db (Session): Database session.
        user: Current admin user.

    Returns:
        List[ProductOut]: All available products.
    """
    logger.info(f"Admin {user.email} requested product list.")
    return db.query(models.Product).all()


@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_admin_user)
):
    """
    Retrieves a specific product by ID. Admin only.

    Args:
        product_id (int): ID of the product.
        db (Session): Database session.
        user: Current admin user.

    Returns:
        ProductOut: The requested product data.

    Raises:
        HTTPException: If the product does not exist.
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        logger.warning(f"Admin {user.email} tried to access nonexistent product ID {product_id}.")
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(
    product_id: int,
    updated: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_admin_user)
):
    """
    Updates an existing product by ID. Admin only.

    Args:
        product_id (int): ID of the product to update.
        updated (ProductUpdate): New data to apply.
        db (Session): Database session.
        user: Current admin user.

    Returns:
        ProductOut: The updated product.

    Raises:
        HTTPException: If the product does not exist.
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        logger.warning(f"Admin {user.email} tried to update nonexistent product ID {product_id}.")
        raise HTTPException(status_code=404, detail="Product not found")

    for field, value in updated.model_dump(exclude_unset=True).items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    logger.info(f"Admin {user.email} updated product ID {product_id}.")
    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_admin_user)
):
    """
    Deletes a product from the catalog by ID. Admin only.

    Args:
        product_id (int): ID of the product to delete.
        db (Session): Database session.
        user: Current admin user.

    Returns:
        dict: Confirmation message.

    Raises:
        HTTPException: If the product does not exist.
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        logger.warning(f"Admin {user.email} tried to delete nonexistent product ID {product_id}.")
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    logger.info(f"Admin {user.email} deleted product ID {product_id}.")
    return {"message": "Product deleted successfully"}
