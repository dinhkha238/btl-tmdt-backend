

from database import create_connection
from model.order import Order
from model.payment import Payment
from service.cart_product_item_DAO import list_cart_product_item_by_cart_id
from sqlalchemy.orm import Session


def all_payments(db:Session):
    return db.query(Payment).all()
        
def payment_by_id(payment_id, db:Session):
    return db.query(Payment).filter(Payment.id == payment_id).first()
