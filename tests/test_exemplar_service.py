# tests/test_exemplar_service.py

# Importa os serviços e modelos necessários
from services.exemplar_service import ExemplarService
from services.livro_service import LivroService # Necessário para criar o livro pré-requisito

def test_criar_exemplar(db_session):
    """
    Testa a criação de um novo exemplar.
    """
    # 1. Preparação: Criar um livro primeiro
    livro_service = LivroService()
    livro_criado = livro_service.criar_livro(
        db=db_session,
        titulo="Livro para Exemplar",
        autor="Autor do Exemplar"
    )
    assert livro_criado is not None

    # 2. Execução: Criar o exemplar associado ao livro
    exemplar_service = ExemplarService()
    exemplar_criado = exemplar_service.criar_exemplar(
        db=db_session,
        tombo=555666,
        cod_livro=livro_criado.cod_livro
    )

    # 3. Verificação
    assert exemplar_criado is not None
    assert exemplar_criado.tombo == 555666
    assert exemplar_criado.cod_livro == livro_criado.cod_livro

def test_buscar_exemplar_por_id(db_session):
    """
    Testa a busca de um exemplar pelo tombo.
    """
    # 1. Preparação
    livro_service = LivroService()
    exemplar_service = ExemplarService()
    livro_criado = livro_service.criar_livro(db=db_session, titulo="Livro Busca", autor="Autor Busca")
    exemplar_service.criar_exemplar(db=db_session, tombo=777888, cod_livro=livro_criado.cod_livro)

    # 2. Execução
    exemplar_encontrado = exemplar_service.buscar_exemplar_por_id(db=db_session, tombo=777888)

    # 3. Verificação
    assert exemplar_encontrado is not None
    assert exemplar_encontrado.tombo == 777888
    assert exemplar_encontrado.livro.titulo == "Livro Busca" # Testando o relacionamento