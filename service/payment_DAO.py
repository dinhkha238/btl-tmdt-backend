

from database import create_connection
from model.order import Order
from model.payment import Payment
from service.cart_product_item_DAO import list_cart_product_item_by_cart_id
from sqlalchemy.orm import Session


def all_payments(db:Session):
    # conn = create_connection()
    # with conn.cursor() as cursor:
    #     sql = "SELECT * FROM `payment`"
    #     cursor.execute(sql)
    #     results = cursor.fetchall()
    #     list_payment = []
    #     for row in results:
    #         payment = Payment(id=row[0], name=row[1], currency=row[2], cardNum=row[3], type=row[4], discriminator=row[5])
    #         list_payment.append(payment)
    #     return list_payment
    return db.query(Payment).all()
        
def payment_by_id(payment_id, db:Session):
    return db.query(Payment).filter(Payment.id == payment_id).first()




    # conn = create_connection()
    # with conn.cursor() as cursor:
    #     sql = "SELECT * FROM `payment` WHERE `id` = %s"
    #     cursor.execute(sql, (payment_id,))
    #     result = cursor.fetchone()
    #     payment = Payment(id=result[0], name=result[1], currency=result[2], cardNum=result[3], type=result[4], discriminator=result[5])
    #     return payment