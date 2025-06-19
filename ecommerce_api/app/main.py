import logging
from fastapi import FastAPI
from app.core.database import Base, engine

from app.auth.routes import router as auth_router
from app.products.routes import router as product_router
from app.products.public_routes import router as public_product_router
from app.cart.routes import router as cart_router
from app.checkout.routes import router as checkout_router
from app.orders.routes import router as orders_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Initialize database schema
Base.metadata.create_all(bind=engine)
logger.info("Database tables created.")

# Include routers
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(public_product_router)
app.include_router(cart_router)
app.include_router(checkout_router)
app.include_router(orders_router)
logger.info("Routers registered.")

@app.get("/")
def read_root():
    """
    Root route to verify the API is running.

    Returns:
        dict: Welcome message.
    """
    logger.info("Root endpoint '/' accessed.")
    return {"message": "E-commerce API is running !!!!!"}
