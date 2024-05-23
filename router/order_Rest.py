
from fastapi import APIRouter, Body, Depends

from model.order import OrderBase
from security.security import validate_token
from service.order_DAO import accept_order, add_order, all_orders, cancel_order, my_orders, order_by_id, reviewed_order



router = APIRouter()

@router.get("/get-all-orders", tags=["Order"])
async def get_all_orders(month_year:str=""):
    order = all_orders(month_year)
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

@router.put("/cancel-order/{order_id}", tags=["Order"])
async def put_cancel_order(order_id:int):
    cancel_order(order_id)
    return True

@router.put("/reviewed-order/{order_id}", tags=["Order"])
async def put_reviewed_order(order_id:int):
    reviewed_order(order_id)
    return True

@router.put("/accept-order/{order_id}", tags=["Order"])
async def put_accept_order(order_id:int):
    accept_order(order_id)
    return True