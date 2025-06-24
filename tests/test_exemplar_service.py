# tests/test_exemplar_service.py
# VERSÃO FINAL REVISADA

# Importa os serviços e modelos necessários
from services import ExemplarService, LivroService
from models import Exemplar, Livro

def test_criar_exemplar_com_sucesso(db_session):
    """
    Testa a criação de um novo exemplar.
    """
    # --- 1. Arrange (Preparar) ---
    # CORREÇÃO: Instanciar os serviços com a db_session do teste
    livro_service = LivroService(db_session)
    exemplar_service = ExemplarService(db_session)

    # Criar um livro pré-requisito
    livro_criado = livro_service.criar_livro(
        titulo="Livro para Exemplar",
        autor="Autor do Exemplar"
    )
    assert livro_criado is not None, "Falha ao criar o livro pré-requisito."

    # --- 2. Act (Agir) ---
    # CORREÇÃO: Não é mais necessário passar a sessão na chamada do método
    exemplar_criado = exemplar_service.criar_exemplar(
        tombo=555666,
        cod_livro=livro_criado.cod_livro
    )

    # --- 3. Assert (Verificar) ---
    assert exemplar_criado is not None
    assert exemplar_criado.tombo == 555666
    assert exemplar_criado.cod_livro == livro_criado.cod_livro
    # Um bom assert adicional é verificar se o objeto Livro está acessível
    assert exemplar_criado.livro.titulo == "Livro para Exemplar"

def test_buscar_exemplar_por_id_existente(db_session):
    """
    Testa a busca de um exemplar pelo tombo.
    """
    # --- 1. Arrange (Preparar) ---
    livro_service = LivroService(db_session)
    exemplar_service = ExemplarService(db_session)

    livro_criado = livro_service.criar_livro(titulo="Livro Busca", autor="Autor Busca")
    # A criação do exemplar de teste pode ser feita diretamente aqui
    exemplar_criado = exemplar_service.criar_exemplar(tombo=777888, cod_livro=livro_criado.cod_livro)
    assert exemplar_criado is not None, "Falha ao criar o exemplar pré-requisito."

    # --- 2. Act (Agir) ---
    exemplar_encontrado = exemplar_service.buscar_exemplar_por_id(tombo=777888)

    # --- 3. Assert (Verificar) ---
    assert exemplar_encontrado is not None
    assert exemplar_encontrado.tombo == 777888
    # O seu assert do relacionamento já estava perfeito
    assert exemplar_encontrado.livro.titulo == "Livro Busca"