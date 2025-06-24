# tests/test_livro_service.py
# VERSÃO FINAL REVISADA

# CORREÇÃO: Importando do pacote 'services' e 'models'
from services import LivroService
from models import Livro

# --- Testes para LivroService ---

def test_criar_livro_com_sucesso(db_session):
    """Testa a criação de um livro com dados válidos."""
    # --- 1. Arrange (Preparar) ---
    # CORREÇÃO: Instanciar o serviço com a db_session do teste
    livro_service = LivroService(db_session)
    
    # --- 2. Act (Agir) ---
    # CORREÇÃO: Não é mais necessário passar a sessão na chamada do método
    livro_criado = livro_service.criar_livro(
        titulo="O Sol é para Todos",
        autor="Harper Lee",
        editora="J. B. Lippincott & Co.",
        ano=1960
    )
    
    # --- 3. Assert (Verificar) ---
    assert livro_criado is not None
    assert isinstance(livro_criado, Livro)
    assert livro_criado.titulo == "O Sol é para Todos"
    assert livro_criado.autor == "Harper Lee"
    assert livro_criado.cod_livro is not None

def test_buscar_livro_por_id_existente(db_session):
    """Testa a busca de um livro pelo seu código."""
    # --- 1. Arrange (Preparar) ---
    livro_service = LivroService(db_session)
    livro_criado_previamente = livro_service.criar_livro(
        titulo="1984", 
        autor="George Orwell"
    )
    assert livro_criado_previamente is not None, "Falha ao criar o livro pré-requisito."

    # --- 2. Act (Agir) ---
    livro_encontrado = livro_service.buscar_livro_por_id(
        cod_livro=livro_criado_previamente.cod_livro
    )

    # --- 3. Assert (Verificar) ---
    assert livro_encontrado is not None
    assert livro_encontrado.cod_livro == livro_criado_previamente.cod_livro
    assert livro_encontrado.titulo == "1984"