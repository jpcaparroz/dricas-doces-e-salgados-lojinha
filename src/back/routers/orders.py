from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, SQLModel, Field

from config.database import get_session
from models.order import Order
from models.order_item import OrderItem
from models.product import Product
from models.enums import OrderStatus, PaymentMethod

router = APIRouter(prefix="/orders", tags=["Orders"])


# ─── Schemas ────────────────────────────────────────────────────────────────

class OrderItemInput(SQLModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)


class OrderCreate(SQLModel):
    payment_method: PaymentMethod
    items: List[OrderItemInput] = Field(min_length=1)


class OrderItemRead(SQLModel):
    product_id: int
    quantity: int
    unit_price: float
    created_at: datetime
    updated_at: datetime | None = None


class OrderRead(SQLModel):
    id: int
    total_price: float
    payment_method: PaymentMethod
    status: OrderStatus
    items: List[OrderItemRead] = []
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


# ─── Endpoints ───────────────────────────────────────────────────────────────

@router.get("/", response_model=List[OrderRead])
def list_orders(
    status_filter: Optional[OrderStatus] = None,
    session: Session = Depends(get_session),
):
    """Lista pedidos, com filtro opcional por status."""
    statement = select(Order)
    if status_filter:
        statement = statement.where(Order.status == status_filter)
    orders = session.exec(statement).all()
    return orders


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, session: Session = Depends(get_session)):
    """Busca um pedido pelo ID com seus itens."""
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido com id {order_id} não encontrado."
        )
    return order


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate, session: Session = Depends(get_session)):
    """
    Cria um pedido com seus itens.
    - Valida se todos os produtos existem e estão ativos.
    - Usa o preço atual do banco (não aceita preço do cliente).
    - Calcula o total automaticamente.
    - Tudo em uma única transação atômica.
    """
    # 1. Busca e valida todos os produtos de uma vez (1 query só)
    product_ids = [item.product_id for item in order_data.items]
    products_in_db = session.exec(
        select(Product).where(Product.id.in_(product_ids))
    ).all()

    # Monta dict para acesso rápido: {product_id: product}
    products_map = {p.id: p for p in products_in_db}

    # Verifica produtos inexistentes
    missing = [pid for pid in product_ids if pid not in products_map]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produtos não encontrados: {missing}"
        )

    # Verifica produtos inativos
    inactive = [pid for pid in product_ids if not products_map[pid].is_active]
    if inactive:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Produtos inativos (fora de cardápio): {inactive}"
        )

    # 2. Monta os itens e calcula o total
    order_items = []
    total = 0.0

    for item_input in order_data.items:
        product = products_map[item_input.product_id]
        unit_price = product.price 
        total += unit_price * item_input.quantity

        order_items.append(OrderItem(
            product_id=item_input.product_id,
            quantity=item_input.quantity,
            unit_price=unit_price,
        ))

    # 3. Cria o pedido
    order = Order(
        payment_method=order_data.payment_method,
        total_price=round(total, 2),
        status=OrderStatus.COMPLETED,
    )
    session.add(order)
    session.flush()  # gera o order.id sem commitar ainda

    # 4. Vincula os itens ao pedido
    for item in order_items:
        item.order_id = order.id
        session.add(item)

    session.commit()
    session.refresh(order)

    order = session.exec(
        select(Order).where(Order.id == order.id)
    ).one()
    for item in order.items:
        session.refresh(item)

    return order


@router.patch("/{order_id}/status", response_model=OrderRead)
def update_order_status(
    order_id: int,
    new_status: OrderStatus,
    session: Session = Depends(get_session),
):
    """Atualiza apenas o status de um pedido."""
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido com id {order_id} não encontrado."
        )
    order.status = new_status
    session.add(order)
    session.commit()
    session.refresh(order)
    return order