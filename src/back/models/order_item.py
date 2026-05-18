from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from models.base import TimestampMixin, register_updated_at_listener

if TYPE_CHECKING:
    from models.order import Order
    from models.product import Product


class OrderItem(TimestampMixin, table=True):
    __tablename__ = "order_item"

    order_id: Optional[int] = Field(
        default=None, foreign_key="order.id", primary_key=True
    )
    product_id: Optional[int] = Field(
        default=None, foreign_key="product.id", primary_key=True
    )
    quantity: int = Field(default=1, ge=1)
    unit_price: float = Field(ge=0)

    order: "Order" = Relationship(back_populates="items")
    product: "Product" = Relationship(back_populates="order_items")


register_updated_at_listener(OrderItem)