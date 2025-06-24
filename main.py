# main.py

from datetime import date, timedelta

# Importa a SessionLocal para criar sessões com o banco
from db import SessionLocal

# Importa todas as classes de serviço
from services.aluno_service import AlunoService
from services.livro_service import LivroService
from services.exemplar_service import ExemplarService
from services.emprestimo_service import EmprestimoService
from services.emprestimo_exemplar_service import EmprestimoExemplarService

def run_crud_operations():
    """
    Executa um conjunto de operações CRUD para demonstrar o uso dos serviços.
    """
    db = SessionLocal()

    # Instancia todos os serviços
    aluno_service = AlunoService()
    livro_service = LivroService()
    exemplar_service = ExemplarService()
    emprestimo_service = EmprestimoService()
    ee_service = EmprestimoExemplarService()

    try:
        print("--- INICIANDO TESTES DE CRUD ---")

        # 1. CRIAR entidades
        print("\n[CREATE] Criando novas entidades...")
        
        # Criar Aluno
        aluno_criado = aluno_service.criar_aluno(
            db,
            nome="Carlos Santana",
            matricula="2025001",
            email="carlos.santana@email.com",
            curso="Engenharia de Computação"
        )
        if not aluno_criado:
            print("Não foi possível criar o aluno. Abortando.")
            return

        print(f"-> Aluno criado: {aluno_criado}")

        # Criar Livro
        livro_criado = livro_service.criar_livro(
            db,
            titulo="O Pássaro e o Trovão",
            autor="Maria Fumaça",
            editora="Ed. Vento Levou",
            ano=2021
        )
        if not livro_criado:
            print("Não foi possível criar o livro. Abortando.")
            return

        print(f"-> Livro criado: {livro_criado}")

        # Criar Exemplar
        exemplar_criado = exemplar_service.criar_exemplar(
            db,
            tombo=112233,
            cod_livro=livro_criado.cod_livro
        )
        if not exemplar_criado:
            print("Não foi possível criar o exemplar. Abortando.")
            return

        print(f"-> Exemplar criado: {exemplar_criado}")
        
        # 2. LISTAR entidades
        print("\n[READ] Listando entidades...")
        
        todos_alunos = aluno_service.listar_alunos(db, limit=5)
        print(f"-> Listando {len(todos_alunos)} alunos: {todos_alunos}")
        
        todos_livros = livro_service.listar_livros(db, limit=5)
        print(f"-> Listando {len(todos_livros)} livros: {todos_livros}")

        # 3. ATUALIZAR uma entidade
        print("\n[UPDATE] Atualizando o email do aluno...")
        
        aluno_atualizado = aluno_service.atualizar_aluno(
            db,
            matricula=aluno_criado.matricula,
            email="carlos.novo.email@email.com"
        )
        print(f"-> Aluno atualizado: {aluno_atualizado}")

        # 4. CRIAR um empréstimo completo (processo de 2 etapas)
        print("\n[WORKFLOW] Criando um empréstimo completo...")

        # Etapa 1: Criar a entidade Empréstimo
        emprestimo_criado = emprestimo_service.criar_emprestimo(
            db,
            mat_aluno=aluno_criado.matricula,
            data_prevista=date.today() + timedelta(days=15)
        )
        if not emprestimo_criado:
            print("Não foi possível criar o empréstimo. Abortando.")
            return
            
        print(f"-> Registro de Empréstimo criado: {emprestimo_criado}")

        # Etapa 2: Associar o exemplar ao empréstimo
        associacao = ee_service.adicionar_exemplar_a_emprestimo(
            db,
            cod_emprestimo=emprestimo_criado.codEmp,
            tombo_exemplar=exemplar_criado.tombo
        )
        print(f"-> Associação criada: {associacao}")
        
        # 5. LER um empréstimo e seus dados relacionados
        print("\n[READ] Buscando empréstimo por ID e mostrando dados relacionados...")
        emprestimo_completo = emprestimo_service.buscar_emprestimo_por_id(db, emprestimo_criado.codEmp)
        if emprestimo_completo:
            print(f"-> Empréstimo ID: {emprestimo_completo.codEmp}")
            print(f"-> Aluno: {emprestimo_completo.aluno.nome}")
            print(f"-> Exemplares emprestados: {[ex.tombo for ex in emprestimo_completo.exemplares]}")


        # 6. REMOVER entidades (ações destrutivas, geralmente comentadas em testes)
        # print("\n[DELETE] Removendo entidades criadas...")
        #
        # Descomente as linhas abaixo para testar a remoção.
        # A ordem é importante para não violar restrições de chave estrangeira.
        #
        # ee_service.remover_exemplar_de_emprestimo(db, emprestimo_criado.codEmp, exemplar_criado.tombo)
        # print("-> Associação removida.")
        # emprestimo_service.remover_emprestimo(db, emprestimo_criado.codEmp)
        # print("-> Empréstimo removido.")
        # exemplar_service.remover_exemplar(db, exemplar_criado.tombo)
        # print("-> Exemplar removido.")
        # aluno_service.remover_aluno(db, aluno_criado.matricula)
        # print("-> Aluno removido.")
        # livro_service.remover_livro(db, livro_criado.cod_livro)
        # print("-> Livro removido.")

    except Exception as e:
        print(f"Ocorreu um erro inesperado durante as operações: {e}")
    finally:
        print("\n--- FIM DOS TESTES ---")
        db.close()

if __name__ == "__main__":
    run_crud_operations()