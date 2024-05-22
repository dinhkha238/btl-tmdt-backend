
from typing import List, Optional
from pydantic import BaseModel

from model.cart_product_item import CartProductItem
from model.payment import Payment
from model.shipment import Shipment
from model.voucher import Voucher

class OrderBase(BaseModel):
    employeeId: Optional[int] = None
    paymentId: int
    shipmentId: int
    voucherId: Optional[int] = None
    cartId: Optional[int] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    totalOrder: Optional[float] = None
    payStatus: Optional[int] = None
    shipAdress: Optional[str] = None
    phone: Optional[str] = None

class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True

class OrderDetail(Order):
    payment: Payment
    shipment: Shipment
    voucher: Voucher
    cart: List[CartProductItem]

    class Config:
        orm_mode = True