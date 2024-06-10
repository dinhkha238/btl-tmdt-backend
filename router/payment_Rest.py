
from fastapi import APIRouter, Depends
from dbconnect import SessionLocal
from sqlalchemy.orm import Session
from service.order_DAO import all_orders
from service.payment_DAO import all_payments



router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get-all-payments", tags=["Payment"])
async def get_all_payments(db: Session = Depends(get_db)):
    payment = all_payments(db)
    return payment