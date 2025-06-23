# tests/test_livro_service.py

# Não precisamos das fixtures aqui, o pytest as pega do conftest.py

# Importe apenas o que é necessário para os testes do Livro
from models.livro import Livro
from services.livro_service import LivroService


# --- Testes para LivroService ---

def test_criar_livro(db_session): # A fixture 'db_session' é injetada automaticamente pelo pytest
    """
    Testa a função de criar um livro.
    """
    # 1. Preparação
    livro_service = LivroService()
    
    # 2. Execução
    livro_criado = livro_service.criar_livro(
        db=db_session,
        titulo="O Sol é para Todos",
        autor="Harper Lee",
        editora="J. B. Lippincott & Co.",
        ano=1960
    )
    
    # 3. Verificação
    assert livro_criado is not None
    assert livro_criado.titulo == "O Sol é para Todos"
    assert livro_criado.autor == "Harper Lee"
    assert livro_criado.cod_livro is not None

def test_buscar_livro_por_id(db_session):
    """
    Testa a busca de um livro pelo seu código.
    """
    # 1. Preparação
    livro_service = LivroService()
    # Note que os parâmetros para criar o livro agora estão explícitos
    livro_criado = livro_service.criar_livro(
        db=db_session, 
        titulo="1984", 
        autor="George Orwell"
    )

    # 2. Execução
    livro_encontrado = livro_service.buscar_livro_por_id(
        db=db_session, 
        cod_livro=livro_criado.cod_livro
    )

    # 3. Verificação
    assert livro_encontrado is not None
    assert livro_encontrado.cod_livro == livro_criado.cod_livro
    assert livro_encontrado.titulo == "1984"