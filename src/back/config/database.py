import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("A variável de ambiente DATABASE_URL não foi encontrada no arquivo .env")

# O engine é o ecossistema que sabe como se comunicar com o Postgres
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    """
    Importa todos os modelos para garantir que o SQLModel os conheça 
    antes de rodar o create_all.
    """
    from models.order_item import OrderItem
    from models.product import Product
    from models.order import Order
    
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Garante o abrir e fechar de sessões com o banco de dados de forma segura.
    Será usado como 'Dependency Injection' nas rotas.
    """
    with Session(engine) as session:
        yield session