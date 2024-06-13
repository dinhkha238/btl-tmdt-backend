
from database import create_connection
from model.product import Product
from sqlalchemy.orm import Session


def all_product(db:Session):
    return db.query(Product).all()
    
def product_by_id(id, db:Session):
    return db.query(Product).filter(Product.id == id).first()