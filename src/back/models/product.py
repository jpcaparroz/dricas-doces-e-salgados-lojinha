from typing import Optional, List
from sqlmodel import Field, Relationship

from models.enums import ProductCategory
from models.base import TimestampMixin, register_updated_at_listener


class Product(TimestampMixin, table=True):
    __tablename__ = "product"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=1, max_length=100)
    price: float = Field(gt=0)
    category: ProductCategory = Field(default=ProductCategory.OTHERS)
    is_active: bool = Field(default=True)

    order_items: List["OrderItem"] = Relationship(back_populates="product")


register_updated_at_listener(Product)