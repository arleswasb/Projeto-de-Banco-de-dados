# tests/conftest.py
# VERSÃO FINAL REVISADA

import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from db import Base # Base ainda é necessária para o engine conhecer os modelos

# Carrega as variáveis de ambiente do arquivo .env (se ele existir)
load_dotenv()

# Configuração da conexão com o banco de dados de teste
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postarl@localhost:5432/biblioteca?client_encoding=utf8"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        'options': '-c client_encoding=utf8'
    }
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# REMOVIDA a fixture 'setup_and_teardown_database' para cumprir o requisito
# de não usar Base.metadata.create_all().

@pytest.fixture(scope="function")
def db_session():
    """
    Fornece uma sessão de banco de dados isolada para CADA teste.
    A mágica está no transaction.rollback() ao final.
    """
    connection = engine.connect()
    
    # Inicia uma transação
    transaction = connection.begin()
    
    # Cria a sessão vinculada a essa transação
    session = TestingSessionLocal(bind=connection)

    # 'yield' entrega a sessão para o teste que a solicitou
    yield session

    # Ao final do teste, fecha a sessão e desfaz a transação.
    # Isso garante que os dados de um teste não "sujem" o próximo.
    session.close()
    transaction.rollback()
    connection.close()