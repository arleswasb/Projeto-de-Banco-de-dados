# tests/conftest.py
import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv # Biblioteca para ler o arquivo .env
from db import Base

# Carrega as variáveis de ambiente do arquivo .env (se ele existir)
load_dotenv()

# --- CONFIGURAÇÃO DA CONEXÃO COM O BANCO DE DADOS ---
# Lê a DATABASE_URL do ambiente. 
# Se não encontrar, usa uma URL padrão para um PostgreSQL local.
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postarl@localhost:5432/biblioteca_db_teste"
)

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_database():
    """Cria e destrói o banco de dados uma vez por sessão de teste."""
    try:
        # Tenta criar as tabelas. Pode já existir se o banco não for limpo.
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}. Presumindo que já existem.")
        
    yield
    
    # Comentar a linha abaixo se você quiser inspecionar o banco de teste após a execução
    # Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Fornece uma sessão de banco de dados isolada para cada teste."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()