
from database import create_connection
from model.shipment import Shipment
from sqlalchemy.orm import Session

def all_shipments(db:Session):
    return db.query(Shipment).all()

def shipment_by_id(shipment_id,db:Session):
    return db.query(Shipment).filter(Shipment.id == shipment_id).first()