# tests/test_emprestimo_service.py
# VERSÃO FINAL REVISADA

from datetime import date, timedelta
# CORREÇÃO: Importando do pacote 'services'
from services import EmprestimoService, AlunoService

def test_criar_emprestimo_com_sucesso(db_session):
    """
    Testa a criação de um novo registro de empréstimo para um aluno existente.
    """
    # --- 1. Arrange (Preparar) ---
    # CORREÇÃO: Instanciar os serviços com a db_session do teste
    aluno_service = AlunoService(db_session)
    emprestimo_service = EmprestimoService(db_session)

    # Criar um aluno pré-requisito
    # CORREÇÃO: Usar int para matrícula e não passar a sessão na chamada do método
    aluno_criado = aluno_service.criar_aluno(
        nome="Aluno para Empréstimo",
        matricula=123,
        email="emprestimo@teste.com",
        curso="Engenharia"
    )
    assert aluno_criado is not None, "Falha ao criar o aluno pré-requisito para o teste."

    # --- 2. Act (Agir) ---
    # Criar o empréstimo associado ao aluno
    data_prevista = date.today() + timedelta(days=20)
    emprestimo_criado = emprestimo_service.criar_emprestimo(
        mat_aluno=aluno_criado.matricula,
        data_prevista=data_prevista
    )

    # --- 3. Assert (Verificar) ---
    assert emprestimo_criado is not None
    assert emprestimo_criado.mat_aluno == aluno_criado.matricula
    assert emprestimo_criado.data_emp == date.today()
    assert emprestimo_criado.data_prev == data_prevista
    assert emprestimo_criado.data_dev is None # Verifica se a data de devolução começa nula