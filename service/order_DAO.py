
from database import create_connection
from model.order import Order, OrderDetail
from service.cart_product_item_DAO import list_cart_product_item_by_cart_id
from service.payment_DAO import payment_by_id
from service.shipment_DAO import shipment_by_id
from service.voucher_DAO import voucher_by_id


def all_orders(month_year):
    conn = create_connection()
    sql=""
    with conn.cursor() as cursor:
        if month_year != "all":
            sql = "SELECT * FROM `order` WHERE DATE_FORMAT(STR_TO_DATE(createdAt, '%\d/%m/%Y %H:%\i:%\s'), '%Y-%m') = %s"
            cursor.execute(sql, (month_year,))  
        else:
            sql = "SELECT * FROM `order`"
            cursor.execute(sql)
        results = cursor.fetchall()
        list_orders = []
        for row in results:
            cart = list_cart_product_item_by_cart_id(row[5])
            voucher = voucher_by_id(row[4])
            shipment = shipment_by_id(row[3])
            totalOrder = 0
            for item in cart:
                totalOrder += item.price * item.quantity
            totalOrder = totalOrder - voucher.value + shipment.fees
            order = Order(id=row[0], employeeId=row[1], paymentId=row[2], shipmentId=row[3], voucherId=row[4], cartId=row[5], createdAt=row[6], updatedAt=row[7],totalOrder=totalOrder, payStatus=row[8])
            list_orders.append(order)
        return list_orders
    
def order_by_id(order_id):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM `order` WHERE `id` = %s"
        cursor.execute(sql, (order_id,))
        result = cursor.fetchone()
        cart = list_cart_product_item_by_cart_id(result[5])
        voucher = voucher_by_id(result[4])
        shipment = shipment_by_id(result[3])
        payment = payment_by_id(result[2])
        totalOrder = 0
        for item in cart:
            totalOrder += item.price * item.quantity
        totalOrder = totalOrder - voucher.value + shipment.fees
        order = OrderDetail(id=result[0], employeeId=result[1], paymentId=result[2], shipmentId=result[3], voucherId=result[4], cartId=result[5], createdAt=result[6], updatedAt=result[7],payStatus=result[8],totalOrder=totalOrder, payment=payment, shipment=shipment, voucher=voucher, cart=cart, shipAdress=result[9], phone=result[10])
        return order
        
def my_orders(id):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM `cart` WHERE `customerId` = %s"
        cursor.execute(sql, (id,))
        result_carts = cursor.fetchall()
        list_orders = []
        for row in result_carts:
            sql = "SELECT * FROM `order` WHERE `cartId` = %s"
            cursor.execute(sql, (row[0],))
            result = cursor.fetchone()
            if result:
                cart = list_cart_product_item_by_cart_id(result[5])
                voucher = voucher_by_id(result[4])
                shipment = shipment_by_id(result[3])
                payment = payment_by_id(result[2])
                totalOrder = 0
                for item in cart:
                    totalOrder += item.price * item.quantity
                totalOrder = totalOrder - voucher.value + shipment.fees
                order = OrderDetail(id=result[0], employeeId=result[1], paymentId=result[2], shipmentId=result[3], voucherId=result[4], cartId=result[5], createdAt=result[6], updatedAt=result[7],payStatus=result[8],totalOrder=totalOrder, payment=payment, shipment=shipment, voucher=voucher, cart=cart, shipAdress=result[9], phone=result[10])
                list_orders.append(order)
        return list_orders
    
def add_order(id, body):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM cart WHERE customerId = %s"
        cursor.execute(sql, (id,))
        results = cursor.fetchall()
        cart_id = results[-1][0]
        sql = "INSERT INTO `order` (paymentId, shipmentId, voucherId, cartId,createdAt, payStatus, shipAdress, phone) VALUES (%s, %s, %s, %s, %s,%s,%s,%s)"
        cursor.execute(sql, (body["paymentId"], body["shipmentId"], body["voucherId"], cart_id,body["createdAt"], 0, body["shipAdress"], body["phone"]))
        sql = "INSERT INTO `cart` (customerId, createdAt) VALUES (%s, %s)"
        cursor.execute(sql, (id, body["createdAt"]))
        product_in_cart = list_cart_product_item_by_cart_id(cart_id)
        for item in product_in_cart:
            # giảm số lượng sản phẩm trong bảng product_item where productId = item.productItemId
            sql = "UPDATE product_item SET inStock = inStock - %s WHERE productId = %s"
            cursor.execute(sql, (item.quantity, item.productItemId))
        conn.commit()

def cancel_order(id):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "UPDATE `order` SET payStatus = -1 WHERE id = %s"
        cursor.execute(sql, (id,))
        conn.commit()

def reviewed_order(id):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "UPDATE `order` SET payStatus = 2 WHERE id = %s"
        cursor.execute(sql, (id,))
        conn.commit()

def accept_order(id):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "UPDATE `order` SET payStatus = 1 WHERE id = %s"
        cursor.execute(sql, (id,))
        conn.commit()