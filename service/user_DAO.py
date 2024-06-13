# from database import Database
from database import create_connection
from model.customer import Customer
from model.user import User
from sqlalchemy.orm import Session

def all_users(db:Session):
    return db.query(User).all()
    
def check_customer(username, password, db:Session):
    user = db.query(User).filter(User.username == username, User.password == password).first()
    if user:
        customer = db.query(Customer).filter(Customer.userId == user.id).first()
        if customer:
            return customer
    return None

    

def existing_customer(username, db:Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    return user

def info_customer(id, db:Session):
    customer = db.query(Customer).filter(Customer.id == id).first()
    if customer:
        user = db.query(User).filter(User.id == customer.userId).first()
        return user
    return None
    
def create_user(fullname, username, password, contact, address, db:Session):
    user = User(fullname=fullname, username=username, password=password, contact=contact, address=address)
    db.add(user)
    db.commit
    user = existing_customer(username, db)
    customer = Customer(userId=user.id)
    db.add(customer)
    db.commit()
    return user

        