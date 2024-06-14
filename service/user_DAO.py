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
    
def create_user(fullname, username, password, contact, address,gender,birth, db:Session):
    user = User(fullname=fullname, username=username, password=password, contact=contact, address=address, gender=gender, birth=birth)
    db.add(user)
    db.commit()
    user = existing_customer(username, db)
    customer = Customer(userId=user.id)
    db.add(customer)
    db.commit()
    return user

def update_user(id, body, db:Session):
    user = db.query(User).filter(User.id == id).first()
    if user:
        user.fullname = body['fullname']
        user.address = body['address']
        user.contact = body['contact']
        user.password = body['password']
        # dùng db.commit() để lưu thay đổi vào database
        db.commit()
        return user
    return None

def delete_user(id, db:Session):
    user = db.query(User).filter(User.id == id).first()
    if user:
        db.delete(user)
        db.commit()
        return
    return None


            