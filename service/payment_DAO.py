

from database import create_connection
from model.order import Order
from model.payment import Payment
from service.cart_product_item_DAO import list_cart_product_item_by_cart_id


def all_payments():
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM `payment`"
        cursor.execute(sql)
        results = cursor.fetchall()
        list_payment = []
        for row in results:
            payment = Payment(id=row[0], name=row[1], currency=row[2], cardNum=row[3], type=row[4], discriminator=row[5])
            list_payment.append(payment)
        return list_payment
        
def payment_by_id(payment_id):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM `payment` WHERE `id` = %s"
        cursor.execute(sql, (payment_id,))
        result = cursor.fetchone()
        payment = Payment(id=result[0], name=result[1], currency=result[2], cardNum=result[3], type=result[4], discriminator=result[5])
        return payment