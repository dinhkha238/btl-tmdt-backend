
from fastapi import APIRouter, Depends

from security.security import validate_token
from service.cart_DAO import add_item_to_cart, all_cart, my_cart, reduce_item_to_cart, remove_item_to_card
from service.cart_product_item_DAO import list_cart_product_item_by_cart_id


router = APIRouter()

@router.get("/get-all-carts", tags=["Cart"])
async def get_all_cart():
    cart = all_cart()
    return cart

@router.get("/get-cart-by-id/{cart_id}", tags=["Cart"])
async def get_cart_by_id(cart_id: int):
    cart = list_cart_product_item_by_cart_id(cart_id)
    return cart

@router.get("/get-my-cart", tags=["Cart"],dependencies=[Depends(validate_token)])
async def get_my_cart(id:str = Depends(validate_token)):
    carts = my_cart(id)
    return carts

@router.put("/add-item-to-cart/{product_item_id}", tags=["Cart"],dependencies=[Depends(validate_token)])
async def post_add_cart(product_item_id:str,id:str = Depends(validate_token)):
    add_item_to_cart(id,product_item_id)
    return True

@router.put("/reduce-item-to-cart/{product_item_id}", tags=["Cart"],dependencies=[Depends(validate_token)])
async def post_reduce_cart(product_item_id:str,id:str = Depends(validate_token)):
    reduce_item_to_cart(id,product_item_id)
    return True

@router.delete("/remove-item-from-cart/{product_item_id}", tags=["Cart"],dependencies=[Depends(validate_token)])
async def post_remove_cart(product_item_id:str,id:str = Depends(validate_token)):
    remove_item_to_card(id,product_item_id)
    return True
