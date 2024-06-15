
from database import create_connection
from model.customer import Customer
from model.feedback import Feedback
from model.user import User
from service.user_DAO import info_customer
import datetime
from sqlalchemy.orm import Session


def feedback_by_id_product(product_id: int, db:Session):
    results = db.query(Feedback).filter(Feedback.productId == product_id).all()
    list_feedback = []
    for result in results:
        customer = db.query(Customer).filter(Customer.id == result.customerId).first()
        if customer:
            user = db.query(User).filter(User.id == customer.userId).first()
            if user:
                new_feedback = vars(result)
                new_feedback.update({"customer":user.fullname})
                list_feedback.append(new_feedback)
    return list_feedback

def add_feedback(feedback,id,db:Session):
    feedback.customerId = id
    feedback.createdAt = datetime.datetime.now()
    new_feedback = Feedback(**feedback.dict())
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback

