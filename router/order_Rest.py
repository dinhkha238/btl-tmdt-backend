
from fastapi import APIRouter, Body, Depends

from model.order import OrderBase
from security.security import validate_token
from service.order_DAO import add_order, all_orders, my_orders, order_by_id



router = APIRouter()

@router.get("/get-all-orders", tags=["Order"])
async def get_all_orders():
    order = all_orders()
    return order

@router.get("/get-order-by-id/{order_id}", tags=["Order"])
async def get_order_by_id(order_id: int):
    order = order_by_id(order_id)
    return order

@router.get("/get-my-order", tags=["Order"],dependencies=[Depends(validate_token)])
async def get_my_order(id:str = Depends(validate_token)):
    orders = my_orders(id)
    return orders

@router.post("/create-order", tags=["Order"],dependencies=[Depends(validate_token)])
async def post_create_order(body:OrderBase = Body(...),id:str = Depends(validate_token)):
    body = body.dict()
    add_order(id,body)
    return True