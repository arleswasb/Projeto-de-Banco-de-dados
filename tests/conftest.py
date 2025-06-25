# tests/conftest.py
# VERSÃO FINAL REVISADA

import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from db import Base, engine # Base ainda é necessária para o engine conhecer os modelos

# Carrega as variáveis de ambiente do arquivo .env (se ele existir)
load_dotenv()

# Configuração da conexão com o banco de dados
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

# --- ADIÇÃO DA FIXTURE QUE CRIA AS TABELAS ---
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Cria todas as tabelas no banco de dados de teste antes dos testes rodarem.
    """
    # Usando a Base importada, cria todas as tabelas (aluno, livro, etc.)
    Base.metadata.create_all(bind=test_engine)
    
    # 'yield' passa o controle para os testes rodarem
    yield
    
    #Apaga as tabelas no final da sessão de testes
    Base.metadata.drop_all(bind=test_engine)

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