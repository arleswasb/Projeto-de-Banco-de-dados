# tests/test_aluno_service.py

# Não precisamos mais das fixtures aqui, elas vêm do conftest.py

from services.aluno_service import AlunoService

# --- Testes para AlunoService ---

def test_criar_aluno(db_session): # A fixture db_session é injetada automaticamente
    """
    Testa a função de criar um aluno no PostgreSQL.
    """
    aluno_service = AlunoService()
    
    aluno_criado = aluno_service.criar_aluno(
        db=db_session,
        nome="Aluno Teste Postgres",
        matricula="pg12345",
        email="pg@teste.com",
        curso="Engenharia de BD"
    )
    
    assert aluno_criado is not None
    assert aluno_criado.nome == "Aluno Teste Postgres"

def test_buscar_aluno_por_id(db_session):
    """
    Testa a busca de um aluno pela matrícula no PostgreSQL.
    """
    aluno_service = AlunoService()
    aluno_criado = aluno_service.criar_aluno(db_session, "Aluno para Busca PG", "pg789", "buscapg@email.com", "Sistemas")
    
    aluno_encontrado = aluno_service.buscar_aluno_por_id(db=db_session, matricula="pg789")

    assert aluno_encontrado is not None
    assert aluno_encontrado.matricula == aluno_criado.matricula