from fastapi import APIRouter

from service.product_item_DAO import product_item_by_id, product_items, statistic_product_item


router = APIRouter()

@router.get("/get-product-items", tags=["Product-Item"])
async def get_product_items(option: str, filter: str = None, sort: str = None):
    items = product_items(option, filter, sort)
    return items

@router.get("/get-product-item/{id}", tags=["Product-Item"])
async def get_product_item(id: int):
    item = product_item_by_id(id)
    return item

@router.get("/statistic-product-item", tags=["Product-Item"])
async def get_statistic_product_item():
    list_product_item = statistic_product_item()
    return list_product_item
