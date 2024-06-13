
from database import create_connection
from model.cart_product_item import CartProductItem
from service.product_item_DAO import product_item_by_id
from sqlalchemy.orm import Session


def list_cart_product_item_by_cart_id(cart_id, db:Session):
    results = db.query(CartProductItem).filter(CartProductItem.cartId == cart_id).all()
    list_cart_product_item = []
    for row in results:
        product = product_item_by_id(row.productItemId, db)
        new_cart = vars(row)
        new_cart.update(product)
        list_cart_product_item.append(new_cart)
    return list_cart_product_item
