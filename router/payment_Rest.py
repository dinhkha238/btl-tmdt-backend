
from fastapi import APIRouter

from service.order_DAO import all_orders
from service.payment_DAO import all_payments



router = APIRouter()

@router.get("/get-all-payments", tags=["Payment"])
async def get_all_payments():
    payment = all_payments()
    return payment