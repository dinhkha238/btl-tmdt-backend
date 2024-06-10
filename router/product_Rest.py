from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dbconnect import SessionLocal
from service.product_DAO import all_product

router = APIRouter()

# Dependency để lấy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get-all-product", tags=["Product"])
async def get_products(db: Session = Depends(get_db)):
    product = all_product(db)
    return product