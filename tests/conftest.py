# tests/conftest.py
# VERSÃO FINAL CORRIGIDA E CONSISTENTE

import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from db import Base # Apenas a Base é necessária do db.py

# Carrega as variáveis de ambiente
load_dotenv()

# Configuração da conexão com o banco de dados de teste
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postarl@localhost:5432/biblioteca_db_teste"
)

# ---- DEFINIÇÃO CORRETA DO ENGINE DE TESTE ----
# Criamos um engine específico para os testes.
engine_de_teste = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_de_teste)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Cria todas as tabelas no banco de dados de teste ANTES de qualquer teste rodar.
    """
    # CORREÇÃO: Usando a variável 'engine_de_teste' que foi definida acima.
    Base.metadata.create_all(bind=engine_de_teste)
    yield
    # Opcional: Base.metadata.drop_all(bind=engine_de_teste)

@pytest.fixture(scope="function")
def db_session():
    """
    Fornece uma sessão de banco de dados isolada para CADA teste.
    """
    # CORREÇÃO: Usando o 'engine_de_teste' para a conexão.
    connection = engine_de_teste.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()