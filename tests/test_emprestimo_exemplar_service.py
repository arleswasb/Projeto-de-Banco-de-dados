# tests/test_emprestimo_exemplar_service.py
# VERSÃO FINAL REVISADA

from datetime import date # <-- CORREÇÃO: Import necessário
# CORREÇÃO: Importando do pacote 'services'
from services import (
    AlunoService,
    LivroService,
    ExemplarService,
    EmprestimoService,
    EmprestimoExemplarService
)

def test_workflow_emprestimo_completo(db_session):
    """
    Testa o fluxo completo: criar entidades, associar exemplar a empréstimo,
    listar e depois remover a associação.
    """
    # --- 1. Arrange (Preparar) ---
    # CORREÇÃO: Instanciar todos os serviços com a db_session do teste
    aluno_service = AlunoService(db_session)
    livro_service = LivroService(db_session)
    exemplar_service = ExemplarService(db_session)
    emprestimo_service = EmprestimoService(db_session)
    ee_service = EmprestimoExemplarService(db_session)

    # Criar todas as entidades pré-requisito
    # CORREÇÃO: Usando int para matrícula e removendo db_session da chamada
    aluno = aluno_service.criar_aluno(nome="Aluno Workflow", matricula=111, email="wf@teste.com", curso="Curso WF")
    livro = livro_service.criar_livro(titulo="Livro Workflow", autor="Autor WF")
    exemplar = exemplar_service.criar_exemplar(tombo=999111, cod_livro=livro.cod_livro)
    emprestimo = emprestimo_service.criar_emprestimo(mat_aluno=aluno.matricula, data_prevista=date.today())
    
    # --- 2. Act (Adicionar) ---
    # CORREÇÃO: Não é mais necessário passar a sessão para o método
    associacao = ee_service.adicionar_exemplar_a_emprestimo(
        cod_emprestimo=emprestimo.codEmp,
        tombo_exemplar=exemplar.tombo
    )

    # --- 3. Assert (Verificar Adição) ---
    assert associacao is not None
    assert associacao.cod_Emp == emprestimo.codEmp
    assert associacao.Tombo == exemplar.tombo

    # --- 4. Act (Listar) ---
    exemplares_no_emprestimo = ee_service.listar_exemplares_de_emprestimo(
        cod_emprestimo=emprestimo.codEmp
    )

    # --- 5. Assert (Verificar Listagem) ---
    assert len(exemplares_no_emprestimo) == 1
    assert exemplares_no_emprestimo[0].tombo == exemplar.tombo

    # --- 6. Act (Remover) ---
    removido_com_sucesso = ee_service.remover_exemplar_de_emprestimo(
        cod_emprestimo=emprestimo.codEmp,
        tombo_exemplar=exemplar.tombo
    )

    # --- 7. Assert (Verificar Remoção) ---
    assert removido_com_sucesso is True
    exemplares_apos_remocao = ee_service.listar_exemplares_de_emprestimo(
        cod_emprestimo=emprestimo.codEmp
    )
    assert len(exemplares_apos_remocao) == 0