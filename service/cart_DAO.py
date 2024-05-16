
from database import create_connection
from model.cart import Cart
from service.cart_product_item_DAO import list_cart_product_item_by_cart_id
import datetime


def all_cart():
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM cart"
        cursor.execute(sql)
        results = cursor.fetchall()
        list_cart = []
        for row in results:
            cart_by_id = list_cart_product_item_by_cart_id(row[0])
            totalCart = 0
            for item in cart_by_id:
                totalCart += item.price * item.quantity
            cart = Cart(id=row[0], customerId=row[1],createdAt=row[4],updatedAt=row[5],totalCart=totalCart)
            list_cart.append(cart)
        return list_cart
    
def my_cart(id):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM cart WHERE customerId = %s"
        cursor.execute(sql, (id,))
        results = cursor.fetchall()
        if not results:
            sql = "INSERT INTO `cart` (customerId, createdAt) VALUES (%s, %s)"
            cursor.execute(sql, (id, datetime.datetime.now()))
            conn.commit()
            sql = "SELECT * FROM cart WHERE customerId = %s"
            cursor.execute(sql, (id,))
            results = cursor.fetchall()
        cart_id = results[-1][0]
        cart_by_id = list_cart_product_item_by_cart_id(cart_id)
        return cart_by_id
    
def add_item_to_cart(id,product_item_id):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM cart WHERE customerId = %s"
        cursor.execute(sql, (id,))
        results = cursor.fetchall()
        cart_id = results[-1][0]
        sql = "SELECT * FROM tmdt.cart_product_item WHERE cartId = %s AND productItemId = %s"
        cursor.execute(sql, (cart_id,product_item_id))
        result = cursor.fetchone()
        if result is None:
            sql = "INSERT INTO tmdt.cart_product_item (cartId, productItemId, quantity) VALUES (%s, %s, %s)"
            cursor.execute(sql, (cart_id,product_item_id,1))
            conn.commit()
        else:
            sql = "UPDATE tmdt.cart_product_item SET quantity = quantity + 1 WHERE cartId = %s AND productItemId = %s"
            cursor.execute(sql, (cart_id,product_item_id))
            conn.commit()

def reduce_item_to_cart(id,product_item_id):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM cart WHERE customerId = %s"
        cursor.execute(sql, (id,))
        results = cursor.fetchall()
        cart_id = results[-1][0]
        sql = "SELECT * FROM tmdt.cart_product_item WHERE cartId = %s AND productItemId = %s"
        cursor.execute(sql, (cart_id,product_item_id))
        result = cursor.fetchone()
        if result is not None:
            sql = "UPDATE tmdt.cart_product_item SET quantity = quantity - 1 WHERE cartId = %s AND productItemId = %s"
            cursor.execute(sql, (cart_id,product_item_id))
            conn.commit()

def remove_item_to_card(id,product_item_id):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM cart WHERE customerId = %s"
        cursor.execute(sql, (id,))
        results = cursor.fetchall()
        cart_id = results[-1][0]
        sql = "SELECT * FROM tmdt.cart_product_item WHERE cartId = %s AND productItemId = %s"
        cursor.execute(sql, (cart_id,product_item_id))
        result = cursor.fetchone()
        if result is not None:
            sql = "DELETE FROM tmdt.cart_product_item WHERE cartId = %s AND productItemId = %s"
            cursor.execute(sql, (cart_id,product_item_id))
            conn.commit()


