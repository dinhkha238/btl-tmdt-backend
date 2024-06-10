
from fastapi import APIRouter, Depends
from dbconnect import SessionLocal
from service.voucher_DAO import all_vouchers

router = APIRouter()

# Dependency để lấy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get-all-vouchers", tags=["Voucher"])
async def get_all_vouchers(db = Depends(get_db)):
    voucher = all_vouchers(db)
    return voucher