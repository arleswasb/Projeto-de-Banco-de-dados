# tests/test_emprestimo_exemplar_service.py
from services.aluno_service import AlunoService
from services.livro_service import LivroService
from services.exemplar_service import ExemplarService
from services.emprestimo_service import EmprestimoService
from services.emprestimo_exemplar_service import EmprestimoExemplarService

def test_workflow_emprestimo_completo(db_session):
    """
    Testa o fluxo completo: criar entidades, associar exemplar a empréstimo,
    listar e depois remover a associação.
    """
    # 1. Preparação: Instanciar todos os serviços
    aluno_service = AlunoService()
    livro_service = LivroService()
    exemplar_service = ExemplarService()
    emprestimo_service = EmprestimoService()
    ee_service = EmprestimoExemplarService()

    # Criar todas as entidades pré-requisito
    aluno = aluno_service.criar_aluno(db_session, "Aluno Workflow", "wf1", "wf@teste.com", "Curso WF")
    livro = livro_service.criar_livro(db_session, "Livro Workflow", "Autor WF")
    exemplar = exemplar_service.criar_exemplar(db_session, 999111, livro.cod_livro)
    emprestimo = emprestimo_service.criar_emprestimo(db_session, aluno.matricula, date.today())
    
    # 2. Execução (Adicionar)
    associacao = ee_service.adicionar_exemplar_a_emprestimo(
        db=db_session,
        cod_emprestimo=emprestimo.codEmp,
        tombo_exemplar=exemplar.tombo
    )

    # 3. Verificação (Adicionar)
    assert associacao is not None
    assert associacao.cod_Emp == emprestimo.codEmp
    assert associacao.Tombo == exemplar.tombo

    # 4. Execução (Listar)
    exemplares_no_emprestimo = ee_service.listar_exemplares_de_emprestimo(
        db=db_session, 
        cod_emprestimo=emprestimo.codEmp
    )

    # 5. Verificação (Listar)
    assert len(exemplares_no_emprestimo) == 1
    assert exemplares_no_emprestimo[0].tombo == exemplar.tombo

    # 6. Execução (Remover)
    removido_com_sucesso = ee_service.remover_exemplar_de_emprestimo(
        db=db_session,
        cod_emprestimo=emprestimo.codEmp,
        tombo_exemplar=exemplar.tombo
    )

    # 7. Verificação (Remover)
    assert removido_com_sucesso is True
    exemplares_apos_remocao = ee_service.listar_exemplares_de_emprestimo(
        db=db_session, 
        cod_emprestimo=emprestimo.codEmp
    )
    assert len(exemplares_apos_remocao) == 0