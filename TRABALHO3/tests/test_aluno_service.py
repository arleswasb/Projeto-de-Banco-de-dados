# trabalho3/tests/test_aluno_service.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from trabalho3.db import Base
from trabalho3.models.aluno import Aluno
from trabalho3.services.aluno_service import AlunoService

# Usar um banco de dados em memória para testes unitários mais rápidos
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"

@pytest.fixture(scope="module")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine) # Cria as tabelas para o teste
    yield engine
    Base.metadata.drop_all(bind=engine) # Limpa as tabelas após o teste

@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = SessionLocal()
    yield session
    session.close()
    transaction.rollback()
    connection.close()

def test_create_aluno(db_session):
    service = AlunoService(db_session)
    aluno = service.create_aluno(nome="Teste Aluno", matricula="99999", email="test@example.com", curso="Engenharia")
    assert aluno.matricula == "99999"
    assert aluno.nome == "Teste Aluno"

    found_aluno = service.get_aluno_by_matricula("99999")
    assert found_aluno is not None
    assert found_aluno.email == "test@example.com"