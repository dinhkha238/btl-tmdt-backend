
from database import create_connection
from model.cart_product_item import CartProductItem
from model.order import Order
from model.product import Product
from model.product_item import ProductItem
from model.statistic_product_item import StatisticProductItemBase
from service.product_DAO import product_by_id
from fuzzywuzzy import fuzz
from sqlalchemy.orm import Session
from sqlalchemy import func,extract


def product_items(option, filter, sort, db:Session):
    if(option == "All"):
        list_product = db.query(ProductItem).all()
    else:
        results = db.query(Product).filter(Product.summary == option).all()
        if not results:
            return []
        list_product = []
        for product in results:
            list_product.append(product.id)
        list_product = db.query(ProductItem).filter(ProductItem.productId.in_(list_product)).all()
    
    list_product_item = []
    for product_item in list_product:
        product = product_by_id(product_item.productId, db)
        new_product_item = vars(product_item)
        new_product_item.update(vars(product))
        list_product_item.append(product_item)

    if filter != None:
        # không phân biệt chữ hoa chữ thường
        filter = filter.lower()
        # Ngưỡng độ tương đồng (tùy chỉnh theo nhu cầu của bạn)
        threshold = 60
        # Lọc các sản phẩm dựa trên độ tương đồng của tên
        list_product_item = [product_item for product_item in list_product_item if fuzz.partial_ratio(filter, product_item.name.lower()) >= threshold]
    if sort != None:
        # if sort = "option2" => sort by name
        if sort == "option2":
            list_product_item = sorted(list_product_item, key=lambda x: x.name)
        elif sort == "option3":
            # sort price from low to high
            list_product_item = sorted(list_product_item, key=lambda x: x.price)
        elif sort == "option4":
            # sort price from high to low
            list_product_item = sorted(list_product_item, key=lambda x: x.price, reverse=True)
    return list_product_item
    
    
def product_item_by_id(id, db:Session):
    result = db.query(ProductItem).filter(ProductItem.id == id).first()
    product = product_by_id(result.productId, db)
    new_product_item = vars(result)
    new_product_item.update(vars(product))
    return new_product_item
    
def statistic_product_item(db:Session, yy_mm):
    if yy_mm == "":
        results = db.query(
    CartProductItem.productItemId,
    func.sum(CartProductItem.quantity).label('totalQuantity'),
    func.sum(CartProductItem.quantity * ProductItem.price).label('totalRevenue')
).join(Order, CartProductItem.cartId == Order.cartId).join(
    ProductItem, CartProductItem.productItemId == ProductItem.id
).filter(
        Order.payStatus > 0
    ).group_by(
        CartProductItem.productItemId
    ).all()
    else:
        results = db.query(
    CartProductItem.productItemId,
    func.sum(CartProductItem.quantity).label('totalQuantity'),
    func.sum(CartProductItem.quantity * ProductItem.price).label('totalRevenue')
).join(Order, CartProductItem.cartId == Order.cartId).join(
    ProductItem, CartProductItem.productItemId == ProductItem.id
).filter(
        Order.payStatus > 0,
        Order.createdAt.startswith(yy_mm)

    ).group_by(
        CartProductItem.productItemId
    ).all()
     

    list_product_item = []
    for row in results:
        pt_by_id = product_item_by_id(row[0], db)
        product_item = StatisticProductItemBase(productItemId = row[0], totalQuantity = row[1], nameProductItem = pt_by_id["name"], totalRevenue = row[2])
        list_product_item.append(product_item)
    return list_product_item

def monthly_revenue(db:Session, year):
    monthly_revenues = [0] * 12  # Tạo mảng rỗng gồm 12 phần tử ban đầu

    for month in range(1, 13):  # Lặp qua từ tháng 1 đến tháng 12
        if(year == ""):
            total_revenue = db.query(
            func.sum(CartProductItem.quantity * ProductItem.price)
        ).join(Order, CartProductItem.cartId == Order.cartId).join(
            ProductItem, CartProductItem.productItemId == ProductItem.id
        ).filter(
            Order.payStatus > 0,
            extract('month', Order.createdAt) == month
        ).first()[0]
        else:
            # Tính tổng doanh thu cho tháng và năm cụ thể
            total_revenue = db.query(
                func.sum(CartProductItem.quantity * ProductItem.price)
            ).join(Order, CartProductItem.cartId == Order.cartId).join(
                ProductItem, CartProductItem.productItemId == ProductItem.id
            ).filter(
                Order.payStatus > 0,
                extract('year', Order.createdAt) == year,
                extract('month', Order.createdAt) == month
            ).scalar() or 0  # scalar() để trả về giá trị hoặc None, nếu là None thì trả về 0

        monthly_revenues[month - 1] = total_revenue  # Lưu tổng doanh thu vào mảng

    return monthly_revenues