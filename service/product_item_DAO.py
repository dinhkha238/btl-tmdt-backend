
from database import create_connection
from model.product_item import ProductItem
from model.statistic_product_item import StatisticProductItemBase
from service.product_DAO import product_by_id
from fuzzywuzzy import fuzz

def product_items(option, filter, sort):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = ""
        if(option == "All"):
            sql = "SELECT * FROM product_item"
            cursor.execute(sql)
        else:
            sql = "SELECT * FROM product WHERE summary = %s"
            cursor.execute(sql, (option,))   
            results = cursor.fetchall()
            if not results:
                return []
            list_product = []
            for row in results:
                list_product.append(row[0])
            sql = "SELECT * FROM product_item WHERE productId IN ({})".format(",".join(str(i) for i in list_product))
            cursor.execute(sql)
        results = cursor.fetchall()
        list_product_item = []
        for row in results:
            product = product_by_id(row[2])
            product_item = ProductItem(id=row[0], employeeId=row[1], productId=row[2], price=row[3], addedDate=row[4], inStock=row[5], name=product.name, summary=product.summary, releaseDate=product.releaseDate, provider=product.provider, brand=product.brand, model=product.model, spec=product.spec, version=product.version, roomType=product.roomType, series=product.series, discriminator=product.discriminator, url=product.url)
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
    
def product_item_by_id(id):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM product_item WHERE productId = %s"
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        product = product_by_id(result[2])
        product_item = ProductItem(id=result[0], employeeId=result[1], productId=result[2], price=result[3], addedDate=result[4], inStock=result[5], name=product.name, summary=product.summary, releaseDate=product.releaseDate, provider=product.provider, brand=product.brand, model=product.model, spec=product.spec, version=product.version, roomType=product.roomType, series=product.series, discriminator=product.discriminator, url=product.url)
        return product_item
    
def statistic_product_item():
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT productItemId, SUM(quantity) AS totalQuantity FROM tmdt.cart_product_item cpi INNER JOIN tmdt.order o ON cpi.cartId = o.cartId and payStatus > 0 GROUP BY productItemId"
        cursor.execute(sql)
        results = cursor.fetchall()
        list_product_item = []
        for row in results:
            pt_by_id = product_item_by_id(row[0])
            product_item = StatisticProductItemBase(productItemId = row[0], totalQuantity = row[1], nameProductItem = pt_by_id.name)
            list_product_item.append(product_item)
        return list_product_item