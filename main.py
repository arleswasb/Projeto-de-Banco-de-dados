# main.py
# VERSÃO DE DEMONSTRAÇÃO COMPLETA E SISTEMÁTICA

from datetime import date, timedelta
from sqlalchemy import text
from db import SessionLocal
from services import (
    AlunoService,
    LivroService,
    ExemplarService,
    EmprestimoService,
    EmprestimoExemplarService
)

def run_full_demonstration():
    """
    Executa uma demonstração sistemática de todas as operações CRUD e fluxos de trabalho.
    """
    print("--- INICIANDO DEMONSTRAÇÃO COMPLETA DO SISTEMA ---")
    
    db_session = SessionLocal()
    
    try:
        # --- PASSO 0: Limpeza do Banco de Dados ---
        print("\n[SETUP] Limpando tabelas para uma nova demonstração...")
        db_session.execute(text('TRUNCATE TABLE aluno, livro, exemplar, emprestimo, "Emp_exemplar" RESTART IDENTITY CASCADE;'))
        db_session.commit()
        print("Tabelas limpas com sucesso.")

        # --- Instanciando os serviços ---
        aluno_service = AlunoService(db_session)
        livro_service = LivroService(db_session)
        exemplar_service = ExemplarService(db_session)
        emprestimo_service = EmprestimoService(db_session)
        ee_service = EmprestimoExemplarService(db_session)
        print("Serviços instanciados.")

        # =================================================================
        # DEMONSTRAÇÃO DO CICLO DE VIDA COMPLETO: ALUNO
        # =================================================================
        print("\n\n--- DEMONSTRAÇÃO DO CICLO DE VIDA: ALUNO ---")
        
        # 1. CREATE
        print("\n[ALUNO - CREATE] Criando um novo aluno...")
        aluno = aluno_service.criar_aluno(nome="Ana Pereira", matricula=101, email="ana.p@email.com", curso="Letras")
        print(f"-> Aluno criado: {aluno}")
        
        # 2. READ (By ID)
        print(f"\n[ALUNO - READ] Buscando aluno pela matrícula {aluno.matricula}...")
        aluno_encontrado = aluno_service.buscar_aluno_por_id(aluno.matricula)
        print(f"-> Aluno encontrado: {aluno_encontrado}")
        assert aluno_encontrado.nome == "Ana Pereira"

        # 3. UPDATE
        print(f"\n[ALUNO - UPDATE] Atualizando o curso do aluno {aluno.nome}...")
        aluno_atualizado = aluno_service.atualizar_aluno(matricula=aluno.matricula, curso="Letras - Inglês")
        print(f"-> Curso atualizado para: '{aluno_atualizado.curso}'")
        assert aluno_atualizado.curso == "Letras - Inglês"

        # 4. READ (List All)
        print("\n[ALUNO - READ] Listando todos os alunos no banco...")
        todos_alunos = aluno_service.listar_alunos()
        print(f"-> Total de alunos encontrados: {len(todos_alunos)}")
        print(todos_alunos)
        assert len(todos_alunos) == 1
        
        # 5. DELETE
        print(f"\n[ALUNO - DELETE] Removendo o aluno {aluno.nome}...")
        sucesso_remocao = aluno_service.remover_aluno(aluno.matricula)
        print(f"-> Remoção bem-sucedida: {sucesso_remocao}")
        aluno_apos_remocao = aluno_service.buscar_aluno_por_id(aluno.matricula)
        print(f"-> Tentando buscar o aluno novamente: {aluno_apos_remocao}")
        assert aluno_apos_remocao is None

        # =================================================================
        # DEMONSTRAÇÃO DO FLUXO DE TRABALHO: EMPRÉSTIMO
        # =================================================================
        print("\n\n--- DEMONSTRAÇÃO DO FLUXO DE TRABALHO: EMPRÉSTIMO ---")

        # 1. CREATE (Entidades pré-requisito)
        print("\n[EMPRÉSTIMO - ARRANGE] Criando livro, exemplar e aluno para o fluxo...")
        livro = livro_service.criar_livro(titulo="O Guia do Mochileiro das Galáxias", autor="Douglas Adams")
        aluno = aluno_service.criar_aluno(nome="Beto Silva", matricula=102, email="beto.s@email.com", curso="Física")
        exemplar = exemplar_service.criar_exemplar(tombo=3001, cod_livro=livro.cod_livro)
        print(f"-> Entidades criadas: Livro '{livro.titulo}', Aluno '{aluno.nome}', Exemplar Tombo {exemplar.tombo}")

        # 2. CREATE (Empréstimo) e Associação
        print("\n[EMPRÉSTIMO - ACT] Criando empréstimo e associando exemplar...")
        data_prevista = date.today() + timedelta(days=10)
        emprestimo = emprestimo_service.criar_emprestimo(mat_aluno=aluno.matricula, data_prevista=data_prevista)
        ee_service.adicionar_exemplar_a_emprestimo(emprestimo.codEmp, exemplar.tombo)
        print(f"-> Empréstimo ID {emprestimo.codEmp} criado e exemplar {exemplar.tombo} associado.")

        # 3. READ (Verificação)
        print("\n[EMPRÉSTIMO - ASSERT] Verificando exemplares no empréstimo...")
        exemplares_no_emprestimo = ee_service.listar_exemplares_de_emprestimo(emprestimo.codEmp)
        print(f"-> O empréstimo {emprestimo.codEmp} possui {len(exemplares_no_emprestimo)} exemplar(es).")
        assert len(exemplares_no_emprestimo) == 1
        assert exemplares_no_emprestimo[0].tombo == exemplar.tombo

    except Exception as e:
        print(f"\nOcorreu um erro inesperado durante as operações: {e}")
        db_session.rollback()
    finally:
        print("\n--- DEMONSTRAÇÃO FINALIZADA. Fechando sessão. ---")
        db_session.close()

if __name__ == "__main__":
    run_full_demonstration()