
from database import create_connection
from model.order import Order
from model.voucher import Voucher
from service.cart_product_item_DAO import list_cart_product_item_by_cart_id
from service.payment_DAO import payment_by_id
from sqlalchemy.orm import Session

def all_vouchers(db:Session):
    return db.query(Voucher).all()
    
def voucher_by_id(voucher_id, db:Session):
    return db.query(Voucher).filter(Voucher.id == voucher_id).first()
    
        