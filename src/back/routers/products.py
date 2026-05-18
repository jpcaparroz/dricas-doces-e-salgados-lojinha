from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Field, SQLModel, Session, select

from config.database import get_session
from models.product import Product
from models.enums import ProductCategory

router = APIRouter(prefix="/products", tags=["Products"])


# ─── Schemas ────────────────────────────────────────────────────────────────

class ProductBase(SQLModel):
    """Campos compartilhados entre Create e Read."""
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    category: ProductCategory
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    price: Optional[float] = Field(default=None, gt=0)
    category: Optional[ProductCategory] = None
    is_active: Optional[bool] = None


class ProductRead(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None


# ─── Endpoints ───────────────────────────────────────────────────────────────

@router.get("/", response_model=List[ProductRead])
def list_products(session: Session = Depends(get_session)):
    """Retorna todos os produtos ativos para o cardápio."""
    statement = select(Product).where(Product.is_active.is_(True))
    return session.exec(statement).all()


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, session: Session = Depends(get_session)):
    """Busca um produto específico pelo ID."""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com id {product_id} não encontrado."
        )
    return product


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    session: Session = Depends(get_session)
):
    """Cadastra um novo produto no sistema."""
    db_product = Product.model_validate(product_data)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    session: Session = Depends(get_session)
):
    """Atualiza parcialmente um produto (nome, preço, categoria ou status)."""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com id {product_id} não encontrado."
        )

    # Aplica só os campos que foram enviados (exclui None)
    updated_fields = product_data.model_dump(exclude_unset=True)
    product.sqlmodel_update(updated_fields)

    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, session: Session = Depends(get_session)):
    """
    Soft delete: desativa o produto em vez de remover do banco.
    Preserva histórico de pedidos que referenciam este produto.
    """
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com id {product_id} não encontrado."
        )

    product.is_active = False
    session.add(product)
    session.commit()