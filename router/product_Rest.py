from fastapi import APIRouter

from service.product_DAO import all_product

router = APIRouter()

@router.get("/get-all-product", tags=["Product"])
async def get_products():
    product = all_product()
    return product