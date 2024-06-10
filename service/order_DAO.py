
from database import create_connection
from model.cart import Cart
from model.order import Order, OrderDetail
from model.product_item import ProductItem
from service.cart_product_item_DAO import list_cart_product_item_by_cart_id
from service.payment_DAO import payment_by_id
from service.shipment_DAO import shipment_by_id
from service.voucher_DAO import voucher_by_id
from sqlalchemy.orm import Session
from sqlalchemy import func


def all_orders(month_year,db:Session):
    # conn = create_connection()
    # sql=""
    # with conn.cursor() as cursor:
    #     if month_year != "all":
    #         sql = "SELECT * FROM `order` WHERE DATE_FORMAT(STR_TO_DATE(createdAt, '%\d/%m/%Y %H:%\i:%\s'), '%Y-%m') = %s"
    #         cursor.execute(sql, (month_year,))  
    #     else:
    #         sql = "SELECT * FROM `order`"
    #         cursor.execute(sql)
    #     results = cursor.fetchall()
    #     list_orders = []
    #     for row in results:
    #         cart = list_cart_product_item_by_cart_id(row[5])
    #         voucher = voucher_by_id(row[4])
    #         shipment = shipment_by_id(row[3])
    #         totalOrder = 0
    #         for item in cart:
    #             totalOrder += item.price * item.quantity
    #         totalOrder = totalOrder - voucher.value + shipment.fees
    #         order = Order(id=row[0], employeeId=row[1], paymentId=row[2], shipmentId=row[3], voucherId=row[4], cartId=row[5], createdAt=row[6], updatedAt=row[7],totalOrder=totalOrder, payStatus=row[8])
    #         list_orders.append(order)
    #     return list_orders

    if month_year != "all":
        results = db.query(Order).filter(
            func.date_format(Order.createdAt, '%Y-%m') == month_year
        ).all()
    else:
        results = db.query(Order).all()
    list_orders = []
    for row in results:
        cart = list_cart_product_item_by_cart_id(row.cartId, db)
        voucher = voucher_by_id(row.voucherId, db)
        shipment = shipment_by_id(row.shipmentId, db)
        totalOrder = 0
        for item in cart:
            totalOrder += item["price"] * item["quantity"]
        totalOrder = totalOrder - voucher.value + shipment.fees
        order = OrderDetail(
            id=row.id,
            employeeId=row.employeeId,
            paymentId=row.paymentId,
            shipmentId=row.shipmentId,
            voucherId=row.voucherId,
            cartId=row.cartId,
            createdAt=row.createdAt,
            updatedAt=row.updatedAt,
            payStatus=row.payStatus
        )
        new_order = vars(order)
        new_order.update({"totalOrder": totalOrder})
        list_orders.append(new_order)
    return list_orders
    
def order_by_id(order_id,db:Session):
    # conn = create_connection()
    # with conn.cursor() as cursor:
    #     sql = "SELECT * FROM `order` WHERE `id` = %s"
    #     cursor.execute(sql, (order_id,))
    #     result = cursor.fetchone()
    #     cart = list_cart_product_item_by_cart_id(result[5])
    #     voucher = voucher_by_id(result[4])
    #     shipment = shipment_by_id(result[3])
    #     payment = payment_by_id(result[2])
    #     totalOrder = 0
    #     for item in cart:
    #         totalOrder += item.price * item.quantity
    #     totalOrder = totalOrder - voucher.value + shipment.fees
    #     order = OrderDetail(id=result[0], employeeId=result[1], paymentId=result[2], shipmentId=result[3], voucherId=result[4], cartId=result[5], createdAt=result[6], updatedAt=result[7],payStatus=result[8],totalOrder=totalOrder, payment=payment, shipment=shipment, voucher=voucher, cart=cart, shipAdress=result[9], phone=result[10])
    #     return order
    result = db.query(Order).filter_by(id=order_id).first()
    cart = list_cart_product_item_by_cart_id(result.cartId, db)
    voucher = voucher_by_id(result.voucherId, db)
    shipment = shipment_by_id(result.shipmentId, db)
    payment = payment_by_id(result.paymentId, db)
    totalOrder = 0
    for item in cart:
        totalOrder += item["price"] * item["quantity"]
    totalOrder = totalOrder - voucher.value + shipment.fees
    order = OrderDetail(
        id=result.id,
        employeeId=result.employeeId,
        paymentId=result.paymentId,
        shipmentId=result.shipmentId,
        voucherId=result.voucherId,
        cartId=result.cartId,
        createdAt=result.createdAt,
        updatedAt=result.updatedAt,
        payStatus=result.payStatus,
        shipAdress=result.shipAdress,
        phone=result.phone
    )
    new_order = vars(order)
    new_order.update({"payment": payment, "shipment": shipment, "voucher": voucher, "cart": cart, "totalOrder": totalOrder})
    return new_order

def my_orders(id,db:Session):
    # conn = create_connection()
    # with conn.cursor() as cursor:
    #     sql = "SELECT * FROM `cart` WHERE `customerId` = %s"
    #     cursor.execute(sql, (id,))
    #     result_carts = cursor.fetchall()
    #     list_orders = []
    #     for row in result_carts:
    #         sql = "SELECT * FROM `order` WHERE `cartId` = %s"
    #         cursor.execute(sql, (row[0],))
    #         result = cursor.fetchone()
    #         if result:
    #             cart = list_cart_product_item_by_cart_id(result[5])
    #             voucher = voucher_by_id(result[4])
    #             shipment = shipment_by_id(result[3])
    #             payment = payment_by_id(result[2])
    #             totalOrder = 0
    #             for item in cart:
    #                 totalOrder += item.price * item.quantity
    #             totalOrder = totalOrder - voucher.value + shipment.fees
    #             order = OrderDetail(id=result[0], employeeId=result[1], paymentId=result[2], shipmentId=result[3], voucherId=result[4], cartId=result[5], createdAt=result[6], updatedAt=result[7],payStatus=result[8],totalOrder=totalOrder, payment=payment, shipment=shipment, voucher=voucher, cart=cart, shipAdress=result[9], phone=result[10])
    #             list_orders.append(order)
    #     return list_orders

    result_carts = db.query(Cart).filter_by(customerId=id).all()
    list_orders = []
    for row in result_carts:
        result = db.query(Order).filter_by(cartId=row.id).first()
        if result:
            cart = list_cart_product_item_by_cart_id(result.cartId, db)
            voucher = voucher_by_id(result.voucherId, db)
            shipment = shipment_by_id(result.shipmentId, db)
            payment = payment_by_id(result.paymentId, db)
            totalOrder = 0
            for item in cart:
                totalOrder += item["price"] * item["quantity"]
            totalOrder = totalOrder - voucher.value + shipment.fees
            order = OrderDetail(
                id=result.id,
                employeeId=result.employeeId,
                paymentId=result.paymentId,
                shipmentId=result.shipmentId,
                voucherId=result.voucherId,
                cartId=result.cartId,
                createdAt=result.createdAt,
                updatedAt=result.updatedAt,
                payStatus=result.payStatus,
                # totalOrder=totalOrder,
                # payment=payment,
                # shipment=shipment,
                # voucher=voucher,
                # cart=cart,
                shipAdress=result.shipAdress,
                phone=result.phone
            )
            new_order = vars(order)
            new_order.update({"totalOrder": totalOrder, "payment": payment, "shipment": shipment, "voucher": voucher, "cart": cart})
            list_orders.append(new_order)
    return list_orders
    
    
def add_order(id, body,db:Session):
    # conn = create_connection()
    # with conn.cursor() as cursor:
    #     sql = "SELECT * FROM cart WHERE customerId = %s"
    #     cursor.execute(sql, (id,))
    #     results = cursor.fetchall()
    #     cart_id = results[-1][0]
    #     sql = "INSERT INTO `order` (paymentId, shipmentId, voucherId, cartId,createdAt, payStatus, shipAdress, phone) VALUES (%s, %s, %s, %s, %s,%s,%s,%s)"
    #     cursor.execute(sql, (body["paymentId"], body["shipmentId"], body["voucherId"], cart_id,body["createdAt"], 0, body["shipAdress"], body["phone"]))
    #     sql = "INSERT INTO `cart` (customerId, createdAt) VALUES (%s, %s)"
    #     cursor.execute(sql, (id, body["createdAt"]))
    #     product_in_cart = list_cart_product_item_by_cart_id(cart_id)
    #     for item in product_in_cart:
    #         # giảm số lượng sản phẩm trong bảng product_item where productId = item.productItemId
    #         sql = "UPDATE product_item SET inStock = inStock - %s WHERE productId = %s"
    #         cursor.execute(sql, (item.quantity, item.productItemId))
    #     conn.commit()

    #     return cursor.lastrowid

    # new_order = Order(paymentId=body["paymentId"], shipmentId=body["shipmentId"], voucherId=body["voucherId"], cartId=body["cartId"], createdAt=body["createdAt"], payStatus=0, shipAdress=body["shipAdress"], phone=body["phone"])
    # db.add(new_order)
    # db.commit()
    # db.refresh(new_order)
    # return new_order

    try:
        # Tìm cart của customer
        cart = db.query(Cart).filter_by(customerId=id).all()[-1]
        if not cart:
            raise ValueError("Cart not found for customerId: {}".format(id))
        # Tạo mới đơn hàng
        new_order = Order(
            paymentId=body["paymentId"],
            shipmentId=body["shipmentId"],
            voucherId=body["voucherId"],
            cartId=cart.id,
            createdAt=body["createdAt"],
            payStatus=0,
            shipAdress=body["shipAdress"],
            phone=body["phone"]
        )
        db.add(new_order)
        
        # Tạo mới cart cho customer
        new_cart = Cart(
            customerId=id,
            createdAt=body["createdAt"]
        )
        db.add(new_cart)
        
        # Lấy danh sách sản phẩm trong giỏ hàng
        product_in_cart = list_cart_product_item_by_cart_id(cart.id, db)
        
        # Giảm số lượng sản phẩm trong bảng product_item
        for item in product_in_cart:
            print(item)
            db.query(ProductItem).filter_by(productId=item["productItemId"]).update({"inStock": ProductItem.inStock - item["quantity"]})
        
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

def cancel_order(id,db:Session):
    # conn = create_connection()
    # with conn.cursor() as cursor:
    #     sql = "UPDATE `order` SET payStatus = -1 WHERE id = %s"
    #     cursor.execute(sql, (id,))
    #     conn.commit()
    
    # dùng db:Session
    db.query(Order).filter(Order.id == id).update({Order.payStatus: -1})
    db.commit()

def reviewed_order(id,db:Session):
    # conn = create_connection()
    # with conn.cursor() as cursor:
    #     sql = "UPDATE `order` SET payStatus = 2 WHERE id = %s"
    #     cursor.execute(sql, (id,))
    #     conn.commit()

    # dùng db:Session
    db.query(Order).filter(Order.id == id).update({Order.payStatus: 2})
    db.commit()

def accept_order(id,db:Session):
    # conn = create_connection()
    # with conn.cursor() as cursor:
    #     sql = "UPDATE `order` SET payStatus = 1 WHERE id = %s"
    #     cursor.execute(sql, (id,))
    #     conn.commit()

    # dùng db:Session
    db.query(Order).filter(Order.id == id).update({Order.payStatus: 1})
    db.commit()