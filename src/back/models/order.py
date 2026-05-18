from typing import Optional, List
from sqlmodel import Field, Relationship
from models.base import TimestampMixin, register_updated_at_listener
from models.enums import OrderStatus, PaymentMethod


class Order(TimestampMixin, table=True):
    __tablename__ = "order"

    id: Optional[int] = Field(default=None, primary_key=True)
    total_price: float = Field(default=0.0, ge=0)
    payment_method: PaymentMethod
    status: OrderStatus = Field(default=OrderStatus.PENDING)

    items: List["OrderItem"] = Relationship(back_populates="order")


register_updated_at_listener(Order)