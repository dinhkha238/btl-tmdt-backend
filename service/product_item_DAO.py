
from database import create_connection
from model.cart_product_item import CartProductItem
from model.order import Order
from model.product import Product
from model.product_item import ProductItem, ProductItemBase
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

def add_product(product: ProductItemBase, db:Session):
    product_new = Product(
        name = product.name,
        summary = product.summary,
        provider = product.provider,
        brand = product.brand,
        model = product.model,
        version = product.version,
        roomType = product.roomType,
        series = product.series,
        discriminator = product.discriminator,
        employeeId = 1,
        url = product.url
    )
    db.add(product_new)
    db.commit()

    product_last = db.query(Product).all()[-1]
    product_item = ProductItem(
        productId = product_last.id,
        price = product.price,
        inStock = product.inStock,
        employeeId = 1
    )
    db.add(product_item)
    db.commit()

    return product_item

def update_product(id, product: ProductItemBase, db:Session):
    product_new = db.query(Product).filter(Product.id == id).first()
    product_new.name = product.name
    product_new.summary = product.summary
    product_new.provider = product.provider
    product_new.brand = product.brand
    product_new.model = product.model
    product_new.version = product.version
    product_new.roomType = product.roomType
    product_new.series = product.series
    product_new.discriminator = product.discriminator
    product_new.url = product.url
    db.commit()

    product_item = db.query(ProductItem).filter(ProductItem.productId == id).first()
    product_item.price = product.price
    product_item.inStock = product.inStock
    db.commit()

    return product_item

def delete_product(id, db:Session):
    product_item = db.query(ProductItem).filter(ProductItem.productId == id).first()
    if product_item:
        db.delete(product_item)
        db.commit()
    product = db.query(Product).filter(Product.id == id).first()
    if product:
        db.delete(product)
        db.commit()
    return
    