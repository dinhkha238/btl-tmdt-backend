
from database import create_connection
from model.feedback import Feedback
from service.user_DAO import info_customer
import datetime
from sqlalchemy.orm import Session


def feedback_by_id_product(product_id: int, db:Session):
    # conn = create_connection()
    # with conn.cursor() as cursor:
    #     sql = "SELECT * FROM feedback WHERE productId = %s"
    #     cursor.execute(sql, (product_id,))
    #     results = cursor.fetchall()
    #     list_feedback = []
    #     for result in results:
    #         customer = info_customer(result[1])
    #         feedback = Feedback(id=result[0], customerId=result[1], productId=result[2], description=result[3], rating=result[4], createdAt=result[6], customer=customer.fullname)
    #         list_feedback.append(feedback)
    #     return list_feedback
    results = db.query(Feedback).filter(Feedback.productId == product_id).all()
    list_feedback = []
    for result in results:
        customer = info_customer(result.customerId, db)
        new_feedback = vars(result)
        new_feedback.update({"customer":customer.fullname})
        list_feedback.append(new_feedback)
    return list_feedback

def add_feedback(feedback,id,db:Session):
    # conn = create_connection()
    # with conn.cursor() as cursor:
    #     sql = "INSERT INTO feedback (customerId, productId, description, rating,createdAt) VALUES (%s, %s, %s, %s,%s)"
    #     cursor.execute(sql, (id, feedback.productId, feedback.description, feedback.rating, datetime.datetime.now()))
    #     conn.commit()

    # dùng db:Session orm
    feedback.customerId = id
    feedback.createdAt = datetime.datetime.now()
    new_feedback = Feedback(**feedback.dict())
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback

