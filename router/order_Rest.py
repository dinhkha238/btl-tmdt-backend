
from fastapi import APIRouter, Body, Depends

from dbconnect import SessionLocal
from model.order import OrderBase
from security.security import validate_token
from service.order_DAO import accept_order, add_order, all_orders, cancel_order, my_orders, order_by_id, reviewed_order



router = APIRouter()

# Dependency để lấy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get-all-orders", tags=["Order"])
async def get_all_orders(month_year:str="",db = Depends(get_db)):
    order = all_orders(month_year,db)
    return order

@router.get("/get-order-by-id/{order_id}", tags=["Order"])
async def get_order_by_id(order_id: int,db = Depends(get_db)):
    order = order_by_id(order_id,db)
    return order

@router.get("/get-my-order", tags=["Order"],dependencies=[Depends(validate_token)])
async def get_my_order(id:str = Depends(validate_token),db = Depends(get_db)):
    orders = my_orders(id,db)
    return orders

@router.post("/create-order", tags=["Order"],dependencies=[Depends(validate_token)])
async def post_create_order(body:OrderBase = Body(...),id:str = Depends(validate_token),db = Depends(get_db)):
    body = body.dict()
    add_order(id,body,db)
    return True

@router.put("/cancel-order/{order_id}", tags=["Order"])
async def put_cancel_order(order_id:int,db = Depends(get_db)):
    cancel_order(order_id,db)
    return True

@router.put("/reviewed-order/{order_id}", tags=["Order"])
async def put_reviewed_order(order_id:int,db = Depends(get_db)):
    reviewed_order(order_id,db)
    return True

@router.put("/accept-order/{order_id}", tags=["Order"])
async def put_accept_order(order_id:int,db = Depends(get_db)):
    accept_order(order_id,db)
    return True