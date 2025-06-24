# tests/test_aluno_service.py
# VERSÃO FINAL REVISADA

# CORREÇÃO: Importando do pacote 'services' para manter a consistência
from services import AlunoService
from models import Aluno # Importar o modelo pode ser útil para asserts

# --- Testes para AlunoService ---

def test_criar_aluno_com_sucesso(db_session):
    """Testa a criação de um aluno com dados válidos."""
    # Arrange (Preparar)
    # CORREÇÃO: O serviço é instanciado com a sessão do teste
    aluno_service = AlunoService(db_session)
    # CORREÇÃO: Usando um número inteiro para a matrícula
    matricula_teste = 12345

    # Act (Agir)
    aluno_criado = aluno_service.criar_aluno(
        nome="Aluno Teste Válido",
        matricula=matricula_teste,
        email="valido@teste.com",
        curso="Engenharia de Testes"
    )
    
    # Assert (Verificar)
    assert aluno_criado is not None
    assert isinstance(aluno_criado, Aluno)
    assert aluno_criado.matricula == matricula_teste
    assert aluno_criado.nome == "Aluno Teste Válido"

def test_buscar_aluno_por_id_existente(db_session):
    """Testa a busca de um aluno que existe no banco de dados."""
    # Arrange (Preparar)
    aluno_service = AlunoService(db_session)
    # CORREÇÃO: Usando um número inteiro para a matrícula
    matricula_teste = 78901
    aluno_criado = aluno_service.criar_aluno(
        nome="Aluno para Busca", 
        matricula=matricula_teste, 
        email="busca@email.com", 
        curso="Sistemas de Teste"
    )
    
    # Act (Agir)
    aluno_encontrado = aluno_service.buscar_aluno_por_id(matricula=matricula_teste)

    # Assert (Verificar)
    assert aluno_encontrado is not None
    assert aluno_encontrado.matricula == aluno_criado.matricula
    assert aluno_encontrado.nome == aluno_criado.nome

def test_buscar_aluno_por_id_inexistente(db_session):
    """Testa a busca por um aluno que não existe, esperando None como resultado."""
    # Arrange (Preparar)
    aluno_service = AlunoService(db_session)
    matricula_inexistente = 99999

    # Act (Agir)
    aluno_encontrado = aluno_service.buscar_aluno_por_id(matricula=matricula_inexistente)

    # Assert (Verificar)
    assert aluno_encontrado is None