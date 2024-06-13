
from database import create_connection
from model.cart import Cart
from model.cart_product_item import CartProductItem
from service.cart_product_item_DAO import list_cart_product_item_by_cart_id
import datetime
from sqlalchemy.orm import Session


def all_cart(db:Session):
    results = db.query(Cart).all()
    list_cart = []
    for row in results:
        cart_by_id = list_cart_product_item_by_cart_id(row.id,db)
        totalCart = 0
        for item in cart_by_id:
            totalCart += item["price"] * item["quantity"]
        new_cart = vars(row)
        new_cart.update({"totalCart":totalCart})
        list_cart.append(new_cart)
    return list_cart
    
def my_cart(id,db:Session):
    cart = db.query(Cart).filter(Cart.customerId == id).all()
    if not cart:
        cart = Cart(customerId=id,createdAt=datetime.datetime.now())
        db.add(cart)
        db.commit()
        db.refresh(cart)
        cart = db.query(Cart).filter(Cart.customerId == id).all()

    cart_by_id = list_cart_product_item_by_cart_id(cart[-1].id,db)
    return cart_by_id
    
def add_item_to_cart(id,product_item_id,db:Session):
    cart = db.query(Cart).filter(Cart.customerId == id).all()
    cart_id = cart[-1].id
    product = db.query(CartProductItem).filter(CartProductItem.cartId == cart_id, CartProductItem.productItemId == product_item_id).first()
    if product is None:
        product = CartProductItem(cartId=cart_id, productItemId=product_item_id, quantity=1)
        db.add(product)
        db.commit()
        db.refresh(product)
    else:
        product.quantity += 1
        db.commit()


def reduce_item_to_cart(id,product_item_id,db:Session):
    cart = db.query(Cart).filter(Cart.customerId == id).all()
    cart_id = cart[-1].id
    product = db.query(CartProductItem).filter(CartProductItem.cartId == cart_id, CartProductItem.productItemId == product_item_id).first()
    if product is not None:
        product.quantity -= 1
        db.commit()
        if product.quantity == 0:
            db.delete(product)
            db.commit()

def remove_item_to_card(id,product_item_id,db:Session):
    cart = db.query(Cart).filter(Cart.customerId == id).all()
    cart_id = cart[-1].id
    product = db.query(CartProductItem).filter(CartProductItem.cartId == cart_id, CartProductItem.productItemId == product_item_id).first()
    if product is not None:
        db.delete(product)
        db.commit()


