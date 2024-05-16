
from database import create_connection
from model.product import Product


def all_product():
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM product"
        cursor.execute(sql)
        results = cursor.fetchall()
        list_product = []
        for row in results:
            product = Product(id=row[0], employeeId=row[1], name=row[2], summary=row[3], releaseDate=row[4], provider=row[5], brand=row[6], model=row[7], spec=row[8], version=row[9], roomType=row[10], series=row[11], discriminator=row[12], url=row[13])
            list_product.append(product)
        return list_product
    
def product_by_id(id):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM product WHERE id = %s"
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        product = Product(id=result[0], employeeId=result[1], name=result[2], summary=result[3], releaseDate=result[4], provider=result[5], brand=result[6], model=result[7], spec=result[8], version=result[9], roomType=result[10], series=result[11], discriminator=result[12], url=result[13])
        return product