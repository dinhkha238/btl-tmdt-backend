
from fastapi import APIRouter, Depends

from dbconnect import SessionLocal
from security.security import validate_token
from service.cart_DAO import add_item_to_cart, all_cart, my_cart, reduce_item_to_cart, remove_item_to_card
from service.cart_product_item_DAO import list_cart_product_item_by_cart_id


router = APIRouter()

# Dependency để lấy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get-all-carts", tags=["Cart"])
async def get_all_cart(db = Depends(get_db)):
    cart = all_cart(db)
    return cart

@router.get("/get-cart-by-id/{cart_id}", tags=["Cart"])
async def get_cart_by_id(cart_id: int, db = Depends(get_db)):
    cart = list_cart_product_item_by_cart_id(cart_id, db)
    return cart

@router.get("/get-my-cart", tags=["Cart"],dependencies=[Depends(validate_token)])
async def get_my_cart(id:str = Depends(validate_token),db = Depends(get_db)):
    carts = my_cart(id,db)
    return carts

@router.put("/add-item-to-cart/{product_item_id}", tags=["Cart"],dependencies=[Depends(validate_token)])
async def post_add_cart(product_item_id:str,id:str = Depends(validate_token),db = Depends(get_db)):
    add_item_to_cart(id,product_item_id,db)
    return True

@router.put("/reduce-item-to-cart/{product_item_id}", tags=["Cart"],dependencies=[Depends(validate_token)])
async def post_reduce_cart(product_item_id:str,id:str = Depends(validate_token),db = Depends(get_db)):
    reduce_item_to_cart(id,product_item_id,db)
    return True

@router.delete("/remove-item-from-cart/{product_item_id}", tags=["Cart"],dependencies=[Depends(validate_token)])
async def post_remove_cart(product_item_id:str,id:str = Depends(validate_token),db = Depends(get_db)):
    remove_item_to_card(id,product_item_id,db)
    return True
