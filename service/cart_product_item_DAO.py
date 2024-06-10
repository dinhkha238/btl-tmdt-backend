
from database import create_connection
from model.cart_product_item import CartProductItem
from service.product_item_DAO import product_item_by_id
from sqlalchemy.orm import Session


def list_cart_product_item_by_cart_id(cart_id, db:Session):
    # conn = create_connection()
    # with conn.cursor() as cursor:
    #     sql = "SELECT * FROM cart_product_item WHERE cartId = %s"
    #     cursor.execute(sql, (cart_id,))
    #     results = cursor.fetchall()
    #     list_cart_product_item = []
    #     for row in results:
    #         product = product_item_by_id(row[2], db)
    #         cart_product_item = CartProductItem(id=row[0], cartId=row[1], productItemId=row[2], quantity=row[3],name=product.name,price=product.price,url=product.url,inStock=product.inStock)
    #         list_cart_product_item.append(cart_product_item)
    #     return list_cart_product_item
    results = db.query(CartProductItem).filter(CartProductItem.cartId == cart_id).all()
    list_cart_product_item = []
    for row in results:
        product = product_item_by_id(row.productItemId, db)
        new_cart = vars(row)
        new_cart.update(product)
        list_cart_product_item.append(new_cart)
    return list_cart_product_item
