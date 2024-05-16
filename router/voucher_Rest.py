
from fastapi import APIRouter
from service.voucher_DAO import all_vouchers

router = APIRouter()

@router.get("/get-all-vouchers", tags=["Voucher"])
async def get_all_vouchers():
    voucher = all_vouchers()
    return voucher