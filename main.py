# main.py
# VERSÃO FINAL REVISADA

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

def run_crud_operations():
    """
    Executa um conjunto de operações CRUD para demonstrar o uso dos serviços.
    """
    db = SessionLocal()

    # CORREÇÃO: Instancia todos os serviços passando a sessão do banco de dados
    aluno_service = AlunoService(db)
    livro_service = LivroService(db)
    exemplar_service = ExemplarService(db)
    emprestimo_service = EmprestimoService(db)
    ee_service = EmprestimoExemplarService(db)

    try:
        print("--- INICIANDO DEMONSTRAÇÃO DE CRUD ---")

        # 1. CRIAR entidades
        print("\n[CREATE] Criando novas entidades...")
        
        # Criar Aluno
        # CORREÇÃO: Matrícula como int e sem passar 'db' no método
        aluno_criado = aluno_service.criar_aluno(
            nome="Carlos Santana",
            matricula=2025001,
            email="carlos.santana@email.com",
            curso="Engenharia de Computação"
        )
        if not aluno_criado:
            print("Não foi possível criar o aluno. Abortando.")
            return
        print(f"-> Aluno criado: {aluno_criado}")

        # Criar Livro
        livro_criado = livro_service.criar_livro(
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
            tombo=112233,
            cod_livro=livro_criado.cod_livro
        )
        if not exemplar_criado:
            print("Não foi possível criar o exemplar. Abortando.")
            return
        print(f"-> Exemplar criado: {exemplar_criado}")
        
        # 2. LISTAR entidades
        print("\n[READ] Listando entidades...")
        todos_alunos = aluno_service.listar_alunos(limit=5)
        print(f"-> Listando {len(todos_alunos)} alunos: {todos_alunos}")
        
        todos_livros = livro_service.listar_livros(limit=5)
        print(f"-> Listando {len(todos_livros)} livros: {todos_livros}")

        # 3. ATUALIZAR uma entidade
        print("\n[UPDATE] Atualizando o email do aluno...")
        aluno_atualizado = aluno_service.atualizar_aluno(
            matricula=aluno_criado.matricula,
            email="carlos.novo.email@email.com"
        )
        print(f"-> Aluno atualizado: {aluno_atualizado}")

        # 4. CRIAR um empréstimo completo
        print("\n[WORKFLOW] Criando um empréstimo completo...")
        emprestimo_criado = emprestimo_service.criar_emprestimo(
            mat_aluno=aluno_criado.matricula,
            data_prevista=date.today() + timedelta(days=15)
        )
        if not emprestimo_criado:
            print("Não foi possível criar o empréstimo. Abortando.")
            return
        print(f"-> Registro de Empréstimo criado: {emprestimo_criado}")

        associacao = ee_service.adicionar_exemplar_a_emprestimo(
            cod_emprestimo=emprestimo_criado.codEmp,
            tombo_exemplar=exemplar_criado.tombo
        )
        print(f"-> Associação criada: {associacao}")
        
        # 5. LER um empréstimo e seus dados relacionados
        print("\n[READ] Buscando empréstimo por ID e mostrando dados relacionados...")
        emprestimo_completo = emprestimo_service.buscar_emprestimo_por_id(emprestimo_criado.codEmp)
        if emprestimo_completo:
            print(f"-> Empréstimo ID: {emprestimo_completo.codEmp}")
            print(f"-> Aluno: {emprestimo_completo.aluno.nome}")
            # CORREÇÃO: Usando o nome correto do relacionamento ('exemplares_associados')
            # e extraindo o objeto 'exemplar' de cada associação.
            exemplares_emprestados = [assoc.exemplar for assoc in emprestimo_completo.exemplares_associados]
            print(f"-> Exemplares emprestados (Tombos): {[ex.tombo for ex in exemplares_emprestados]}")

        # 6. REMOVER entidades (comentado por padrão para não limpar o DB a cada execução)
        print("\n[DELETE] Seção de remoção comentada. Descomente no código para executar.")
        # ...

    except Exception as e:
        print(f"Ocorreu um erro inesperado durante as operações: {e}")
    finally:
        print("\n--- FIM DA DEMONSTRAÇÃO ---")
        db.close()

if __name__ == "__main__":
    run_crud_operations()