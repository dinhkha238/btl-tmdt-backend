
from database import create_connection
from model.shipment import Shipment

def all_shipments():
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM `shipment`"
        cursor.execute(sql)
        results = cursor.fetchall()
        list_shipment = []
        for row in results:
            shipment = Shipment(id=row[0], fees=row[1], address=row[2], name=row[3], type=row[4], note=row[5])
            list_shipment.append(shipment)
        return list_shipment

def shipment_by_id(shipment_id):
    conn = create_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM `shipment` WHERE `id` = %s"
        cursor.execute(sql, (shipment_id,))
        result = cursor.fetchone()
        shipment = Shipment(id=result[0], fees=result[1], address=result[2], name=result[3], type=result[4], note=result[5])
        return shipment