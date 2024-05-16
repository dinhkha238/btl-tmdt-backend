
from fastapi import APIRouter
from service.shipment_DAO import all_shipments

router = APIRouter()

@router.get("/get-all-shipments", tags=["Shipment"])
async def get_all_shipments():
    shipment = all_shipments()
    return shipment