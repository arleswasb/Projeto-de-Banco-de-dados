# main.py
# VERSÃO FINAL COM LISTAGEM DE EXEMPLARES POR LIVRO

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
        # DEMONSTRAÇÃO DO CICLO DE VIDA: ALUNO
        # =================================================================
        print("\n\n--- CICLO DE VIDA: ALUNO ---")
        print("\n[ALUNO - CREATE] Criando um novo aluno...")
        aluno = aluno_service.criar_aluno(nome="Ana Pereira", matricula=101, email="ana.p@email.com", curso="Letras")
        print(f"-> CRIADO: {aluno}")
        
        print(f"\n[ALUNO - READ] Buscando aluno pela matrícula {aluno.matricula}...")
        aluno_encontrado = aluno_service.buscar_aluno_por_id(aluno.matricula)
        print(f"-> ENCONTRADO: {aluno_encontrado}")
        
        print(f"\n[ALUNO - UPDATE] Atualizando o curso do aluno...")
        aluno_atualizado = aluno_service.atualizar_aluno(matricula=aluno.matricula, curso="Letras - Inglês")
        print(f"-> ATUALIZADO: Curso agora é '{aluno_atualizado.curso}'")
        
        print(f"\n[ALUNO - DELETE] Removendo o aluno...")
        aluno_service.remover_aluno(aluno.matricula)
        aluno_apos_remocao = aluno_service.buscar_aluno_por_id(aluno.matricula)
        print(f"-> REMOVIDO: Tentando buscar novamente -> {aluno_apos_remocao}")
        assert aluno_apos_remocao is None

        # =================================================================
        # DEMONSTRAÇÃO DO CICLO DE VIDA: LIVRO
        # =================================================================
        print("\n\n--- CICLO DE VIDA: LIVRO ---")
        
        print("\n[LIVRO - CREATE] Criando um novo livro...")
        livro = livro_service.criar_livro(titulo="O Guia do Mochileiro das Galáxias", autor="Douglas Adams")
        print(f"-> CRIADO: {livro}")
        
        print(f"\n[LIVRO - READ] Buscando livro pelo código {livro.cod_livro}...")
        livro_encontrado = livro_service.buscar_livro_por_id(livro.cod_livro)
        print(f"-> ENCONTRADO: {livro_encontrado}")

        print(f"\n[LIVRO - UPDATE] Atualizando o ano do livro...")
        livro_atualizado = livro_service.atualizar_livro(cod_livro=livro.cod_livro, ano=1979)
        print(f"-> ATUALIZADO: Ano agora é '{livro_atualizado.ano}'")

        print("\n[LIVRO - READ] Listando todos os livros...")
        todos_livros = livro_service.listar_livros()
        print(f"-> LIVROS ATUAIS: {todos_livros}")

        # =================================================================
        # DEMONSTRAÇÃO DO FLUXO DE TRABALHO: EMPRÉSTIMO
        # =================================================================
        print("\n\n--- FLUXO DE TRABALHO: EMPRÉSTIMO COM EXEMPLARES ---")

        # 1. ARRANGE: Criar entidades para o fluxo
        print("\n[FLUXO - ARRANGE] Criando um novo aluno e exemplares para o livro existente...")
        aluno_para_emprestimo = aluno_service.criar_aluno(nome="Beto Silva", matricula=102, email="beto.s@email.com", curso="Física")
        exemplar1 = exemplar_service.criar_exemplar(tombo=3001, cod_livro=livro.cod_livro)
        exemplar2 = exemplar_service.criar_exemplar(tombo=3002, cod_livro=livro.cod_livro)
        print(f"-> Aluno '{aluno_para_emprestimo.nome}' e exemplares {exemplar1.tombo}, {exemplar2.tombo} criados.")

        # --- NOVA DEMONSTRAÇÃO: LISTAR EXEMPLARES DE UM LIVRO ---
        print(f"\n[LIVRO/EXEMPLAR - READ] Listando todos os exemplares do livro '{livro.titulo}'...")
        # Buscamos o livro novamente para garantir que o SQLAlchemy carregue a lista de exemplares
        livro_com_exemplares = livro_service.buscar_livro_por_id(livro.cod_livro)
        # Acessamos o relacionamento .exemplares que foi configurado no models/livro.py
        lista_de_exemplares = livro_com_exemplares.exemplares
        print(f"-> O livro ID {livro.cod_livro} possui {len(lista_de_exemplares)} exemplar(es):")
        for ex in lista_de_exemplares:
            print(f"   - Tombo: {ex.tombo}")
        assert len(lista_de_exemplares) == 2
        # --- FIM DA NOVA DEMONSTRAÇÃO ---

        # 2. ACT: Criar o empréstimo e associar os exemplares
        print("\n[FLUXO - ACT] Criando empréstimo e associando exemplares...")
        data_prevista = date.today() + timedelta(days=10)
        emprestimo = emprestimo_service.criar_emprestimo(mat_aluno=aluno_para_emprestimo.matricula, data_prevista=data_prevista)
        ee_service.adicionar_exemplar_a_emprestimo(emprestimo.codEmp, exemplar1.tombo)
        ee_service.adicionar_exemplar_a_emprestimo(emprestimo.codEmp, exemplar2.tombo)
        print(f"-> Empréstimo ID {emprestimo.codEmp} criado e exemplares associados.")

        # 3. ASSERT: Verificar o resultado
        print("\n[FLUXO - ASSERT] Verificando exemplares no empréstimo...")
        exemplares_no_emprestimo = ee_service.listar_exemplares_de_emprestimo(emprestimo.codEmp)
        print(f"-> O empréstimo {emprestimo.codEmp} possui {len(exemplares_no_emprestimo)} exemplares.")
        assert len(exemplares_no_emprestimo) == 2
        
        # 4. CLEANUP: Remover as entidades em ordem
        print("\n[FLUXO - DELETE] Removendo entidades do fluxo...")
        emprestimo_service.remover_emprestimo(emprestimo.codEmp)
        print("-> Empréstimo e associações removidos.")
        exemplar_service.remover_exemplar(exemplar1.tombo)
        exemplar_service.remover_exemplar(exemplar2.tombo)
        print("-> Exemplares removidos.")
        aluno_service.remover_aluno(aluno_para_emprestimo.matricula)
        print("-> Aluno do fluxo removido.")
        livro_service.remover_livro(livro.cod_livro)
        print("-> Livro removido.")
        
    except Exception as e:
        print(f"\nOcorreu um erro inesperado durante as operações: {e}")
        db_session.rollback()
    finally:
        print("\n--- DEMONSTRAÇÃO FINALIZADA. Fechando sessão. ---")
        db_session.close()

if __name__ == "__main__":
    run_full_demonstration()