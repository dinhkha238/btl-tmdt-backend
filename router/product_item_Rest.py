from fastapi import APIRouter, Depends

from dbconnect import SessionLocal
from service.product_item_DAO import monthly_revenue, product_item_by_id, product_items, statistic_product_item


router = APIRouter()

# Dependency để lấy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get-product-items", tags=["Product-Item"])
async def get_product_items(option: str, filter: str = None, sort: str = None, db = Depends(get_db)):
    items = product_items(option, filter, sort, db)
    return items

@router.get("/get-product-item/{id}", tags=["Product-Item"])
async def get_product_item(id: int, db = Depends(get_db)):
    item = product_item_by_id(id, db)
    return item

@router.get("/statistic-product-item", tags=["Product-Item"])
async def get_statistic_product_item(yy_mm:str = "", db = Depends(get_db)):
    list_product_item = statistic_product_item(db,yy_mm)
    return list_product_item

@router.get("/month-revenue", tags=["Product-Item"])
async def get_monthly_revenue(year:int = "", db = Depends(get_db)):
    list_monthly_revenue = monthly_revenue(db,year)
    return list_monthly_revenue
