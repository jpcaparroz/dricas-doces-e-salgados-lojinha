from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import event
from sqlalchemy.orm import Mapper


def _now() -> datetime:
    return datetime.now(timezone.utc)


class TimestampMixin(SQLModel):
    """
    Adiciona created_at e updated_at em qualquer modelo que herdar esta classe.
    - created_at: preenchido uma vez na criação, nunca mais alterado.
    - updated_at: atualizado automaticamente via SQLAlchemy event antes de cada UPDATE.
    """
    created_at: datetime = Field(default_factory=_now, nullable=False)
    updated_at: Optional[datetime] = Field(default=None, nullable=True)


def register_updated_at_listener(model_class):
    """
    Registra o evento SQLAlchemy que atualiza updated_at antes de cada flush.
    Chame essa função no final de cada arquivo de modelo.
    """
    @event.listens_for(model_class, "before_update")
    def set_updated_at(mapper: Mapper, connection, target):
        target.updated_at = _now()
