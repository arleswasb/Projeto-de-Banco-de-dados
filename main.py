# main.py
# VERSÃO FINAL E COMPLETA

"""
Script principal para demonstração e teste manual das funcionalidades do sistema de biblioteca.
"""
from datetime import date, timedelta

# Importa a fábrica de sessões do db.py
from db import SessionLocal

# Importa todas as classes de serviço do pacote 'services'
from services import (
    AlunoService,
    LivroService,
    ExemplarService,
    EmprestimoService,
    EmprestimoExemplarService
)

def run_demonstration():
    """
    Executa um fluxo de trabalho completo para demonstrar as operações do sistema.
    """
    print("--- INICIANDO DEMONSTRAÇÃO DO SISTEMA DE BIBLIOTECA ---")
    
    # Cria uma sessão única para toda a demonstração
    db_session = SessionLocal()
    
    try:
        # --- 1. Instanciando os serviços com a sessão ---
        print("\n[PASSO 1] Instanciando todos os serviços...")
        aluno_service = AlunoService(db_session)
        livro_service = LivroService(db_session)
        exemplar_service = ExemplarService(db_session)
        emprestimo_service = EmprestimoService(db_session)
        ee_service = EmprestimoExemplarService(db_session)
        print("Serviços instanciados com sucesso.")

        # --- 2. Criando entidades base ---
        print("\n[PASSO 2] Criando um novo livro e um novo aluno...")
        
        livro = livro_service.criar_livro(
            titulo="Arquitetura Limpa: O Guia do Artesão para Estrutura e Design de Software",
            autor="Robert C. Martin"
        )
        if not livro:
            print("-> Falha ao criar livro. Abortando.")
            return
        print(f"-> Livro criado: {livro.titulo} (ID: {livro.cod_livro})")

        aluno = aluno_service.criar_aluno(
            nome="Joana D'arc",
            matricula=202502,
            email="joana.dark@email.com",
            curso="Ciência da Computação"
        )
        if not aluno:
            print("-> Falha ao criar aluno. Abortando.")
            return
        print(f"-> Aluno criado: {aluno.nome} (Matrícula: {aluno.matricula})")

        # --- 3. Criando exemplares para o livro ---
        print(f"\n[PASSO 3] Criando dois exemplares para o livro '{livro.titulo}'...")
        exemplar1 = exemplar_service.criar_exemplar(tombo=2001, cod_livro=livro.cod_livro)
        exemplar2 = exemplar_service.criar_exemplar(tombo=2002, cod_livro=livro.cod_livro)
        if not (exemplar1 and exemplar2):
            print("-> Falha ao criar exemplares. Abortando.")
            return
        print(f"-> Exemplares criados: Tombo {exemplar1.tombo} e {exemplar2.tombo}")

        # --- 4. Criando um empréstimo ---
        print(f"\n[PASSO 4] Criando um empréstimo para o aluno '{aluno.nome}'...")
        data_prevista = date.today() + timedelta(days=15)
        emprestimo = emprestimo_service.criar_emprestimo(
            mat_aluno=aluno.matricula,
            data_prevista=data_prevista
        )
        if not emprestimo:
            print("-> Falha ao criar empréstimo. Abortando.")
            return
        print(f"-> Empréstimo criado: ID {emprestimo.codEmp}, com devolução prevista para {emprestimo.data_prev}")

        # --- 5. Associando os exemplares ao empréstimo ---
        print(f"\n[PASSO 5] Associando os exemplares ao empréstimo ID {emprestimo.codEmp}...")
        ee_service.adicionar_exemplar_a_emprestimo(emprestimo.codEmp, exemplar1.tombo)
        ee_service.adicionar_exemplar_a_emprestimo(emprestimo.codEmp, exemplar2.tombo)
        
        # Verificando a associação através do serviço
        exemplares_no_emprestimo = ee_service.listar_exemplares_de_emprestimo(emprestimo.codEmp)
        print(f"-> O empréstimo {emprestimo.codEmp} agora possui {len(exemplares_no_emprestimo)} exemplares.")
        for ex in exemplares_no_emprestimo:
            print(f"   - Exemplar Tombo: {ex.tombo}, Título: '{ex.livro.titulo}'")
        
        # --- 6. Removendo uma associação ---
        print(f"\n[PASSO 6] Removendo o exemplar {exemplar1.tombo} do empréstimo...")
        sucesso = ee_service.remover_exemplar_de_emprestimo(emprestimo.codEmp, exemplar1.tombo)
        if sucesso:
            print("-> Associação removida com sucesso.")
        
        exemplares_restantes = ee_service.listar_exemplares_de_emprestimo(emprestimo.codEmp)
        print(f"-> O empréstimo {emprestimo.codEmp} agora possui {len(exemplares_restantes)} exemplar(es).")

    except Exception as e:
        print(f"\nOcorreu um erro inesperado durante as operações: {e}")
        # Em caso de erro, garante o rollback para não deixar o banco em estado inconsistente
        db_session.rollback()
    finally:
        # Garante que a sessão seja fechada ao final, independentemente de erros
        print("\n--- DEMONSTRAÇÃO FINALIZADA. Fechando sessão. ---")
        db_session.close()

if __name__ == "__main__":
    run_demonstration()