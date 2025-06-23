# tests/test_emprestimo_service.py
from datetime import date, timedelta
from services.emprestimo_service import EmprestimoService
from services.aluno_service import AlunoService # Necessário para criar o aluno pré-requisito

def test_criar_emprestimo(db_session):
    """
    Testa a criação de um novo registro de empréstimo.
    """
    # 1. Preparação: Criar um aluno primeiro
    aluno_service = AlunoService()
    aluno_criado = aluno_service.criar_aluno(
        db=db_session,
        nome="Aluno para Empréstimo",
        matricula="emp123",
        email="emprestimo@teste.com",
        curso="Engenharia"
    )
    assert aluno_criado is not None

    # 2. Execução: Criar o empréstimo associado ao aluno
    emprestimo_service = EmprestimoService()
    data_prevista = date.today() + timedelta(days=20)
    emprestimo_criado = emprestimo_service.criar_emprestimo(
        db=db_session,
        mat_aluno=aluno_criado.matricula,
        data_prevista=data_prevista
    )

    # 3. Verificação
    assert emprestimo_criado is not None
    assert emprestimo_criado.mat_aluno == aluno_criado.matricula
    assert emprestimo_criado.data_emp == date.today()
    assert emprestimo_criado.data_prev == data_prevista