
from database import create_connection
from model.order import Order
from model.voucher import Voucher
from service.cart_product_item_DAO import list_cart_product_item_by_cart_id


def all_vouchers():
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM `voucher`"
        cursor.execute(sql)
        results = cursor.fetchall()
        list_voucher = []
        for row in results:
            voucher = Voucher(id=row[0], name=row[1], expireDate=row[2], quantity=row[3], value=row[4], percentage=row[5], discriminator=row[6])
            list_voucher.append(voucher)
        return list_voucher
    
def voucher_by_id(voucher_id):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM `voucher` WHERE `id` = %s"
        cursor.execute(sql, (voucher_id,))
        result = cursor.fetchone()
        voucher = Voucher(id=result[0], name=result[1], expireDate=result[2], quantity=result[3], value=result[4], percentage=result[5], discriminator=result[6])
        return voucher
    
        