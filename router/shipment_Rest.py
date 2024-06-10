
from fastapi import APIRouter, Depends
from dbconnect import SessionLocal
from service.shipment_DAO import all_shipments

router = APIRouter()

# Dependency để lấy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get-all-shipments", tags=["Shipment"])
async def get_all_shipments(db = Depends(get_db)):
    shipment = all_shipments(db)
    return shipment