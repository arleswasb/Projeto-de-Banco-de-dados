# TRABALHO3/main.py

import os
import sys
from datetime import date, timedelta, datetime # Importar datetime também para datetime.now()
from sqlalchemy.exc import IntegrityError
import traceback
import random # Para gerar IDs aleatórios ou sequenciais
import time   # Para usar timestamp como parte do ID

# Adiciona o diretório pai do projeto ao PYTHONPATH para que as importações relativas funcionem
# quando main.py é executado como script ou módulo.
# Isso é especialmente útil se você estiver executando main.py diretamente
# ou se o Python tiver problemas para encontrar o pacote 'trabalho3'.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Importações relativas agora funcionarão
from TRABALHO3.db import Engine, Base, get_db
from TRABALHO3.services.aluno_service import AlunoService
from TRABALHO3.services.livro_service import LivroService
from TRABALHO3.services.exemplar_service import ExemplarService
from TRABALHO3.services.emprestimo_service import EmprestimoService # CORRIGIDO: TRABACHO3 para TRABALHO3

# Importar modelos diretamente para operações de teste ou para type hints
from TRABALHO3.models.aluno import Aluno
from TRABALHO3.models.livro import Livro
from TRABALHO3.models.exemplar import Exemplar
from TRABALHO3.models.emprestimo import Emprestimo


def setup_database():
    """
    Função para garantir que as tabelas existam e sejam mapeadas pelo SQLAlchemy.
    Como você já tem o banco criado, esta função não tentará criar tabelas
    se elas já existirem.
    """
    print("Verificação de tabelas concluída (o ORM mapeou as existentes).")


def run_example_operations():
    """Exemplo de como usar os serviços."""
    db_generator = get_db()
    db = next(db_generator)

    # Definir IDs para teste que *não dependem de execuções anteriores*
    # Usamos timestamp para tentar garantir IDs únicos a cada rodada.
    timestamp_int = int(time.time() * 1000) # milissegundos desde a epoch

    # IDs para o livro e exemplar
    # Comece com um número alto para evitar conflito com IDs existentes no DB
    test_livro_id = 20000 + (timestamp_int % 100000) # Gerar um ID maior e mais aleatório
    test_exemplar_tombo = 50000 + (timestamp_int % 100000)
    test_emprestimo_codEmp = 80000 + (timestamp_int % 100000)

    try:
        aluno_service = AlunoService(db)
        livro_service = LivroService(db)
        exemplar_service = ExemplarService(db)
        emprestimo_service = EmprestimoService(db)

        # --- Operações com Alunos ---
        print("\n--- Operações com Alunos ---")
        try:
            # Tenta criar um aluno. Se a matrícula/email já existir, busca um existente.
            # Podemos usar um timestamp para a matrícula também, se quisermos criar sempre um novo aluno
            novo_aluno_matricula = 30000 + (timestamp_int % 100000) # Gerar matrícula mais única
            novo_aluno_email = f"fernanda.dias.{timestamp_int % 100000}@example.com"
            novo_aluno = aluno_service.create_aluno(nome="Fernanda Dias", matricula=str(novo_aluno_matricula), email=novo_aluno_email)
            print(f"Aluno criado: {novo_aluno}")
        except IntegrityError:
            db.rollback()
            print("Aluno com esta matrícula/email já existe. Buscando um existente.")
            # Se o aluno já existe, buscamos ele pelo email/matricula
            novo_aluno = aluno_service.get_aluno_by_matricula(str(novo_aluno_matricula)) # ou get_aluno_by_email()
            if not novo_aluno:
                print("Não foi possível criar nem encontrar o aluno. Exemplo abortado.")
                return

        todos_alunos = aluno_service.get_all_alunos()
        print("\nTodos os alunos:")
        for aluno in todos_alunos:
            print(aluno)

        # --- Operações com Livros ---
        print("\n--- Operações com Livros ---")
        try:
            # Agora, passamos o test_livro_id gerado
            novo_livro = livro_service.create_livro(titulo=f"Livro de Teste {test_livro_id}", autor="Autor Teste", ano=2024, editora="Editora Teste", cod_livro=test_livro_id)
            print(f"Livro criado: {novo_livro}")
        except IntegrityError:
            db.rollback()
            print("Livro com este cod_livro já existe. Buscando um existente.")
            # Se o livro já existe com esse ID, tentamos buscar ele.
            novo_livro = livro_service.get_livro_by_id(test_livro_id)
            if not novo_livro:
                print("Não foi possível criar nem encontrar o livro. Exemplo abortado.")
                return
        except Exception as e:
            db.rollback()
            print(f"Erro ao criar livro: {e}")
            traceback.print_exc()
            return


        todos_livros = livro_service.get_all_livros()
        print("\nTodos os livros:")
        for livro in todos_livros:
            print(livro)

        # --- Operações com Exemplares ---
        print("\n--- Operações com Exemplares ---")
        if novo_livro:
            try:
                # Agora, passamos o test_exemplar_tombo gerado
                novo_exemplar = exemplar_service.create_exemplar(tombo=test_exemplar_tombo, cod_livro=novo_livro.cod_livro)
                print(f"Exemplar criado: {novo_exemplar}")
            except IntegrityError:
                db.rollback()
                print("Exemplar com este tombo já existe. Buscando um existente.")
                novo_exemplar = exemplar_service.get_exemplar_by_tombo(test_exemplar_tombo)
                if not novo_exemplar:
                    print("Não foi possível criar nem encontrar o exemplar. Exemplo abortado.")
                    return
            except Exception as e:
                db.rollback()
                print(f"Erro ao criar exemplar: {e}")
                traceback.print_exc()
                return
        else:
            print("Nenhum livro disponível para criar exemplar.")
            return

        todos_exemplares = exemplar_service.get_all_exemplares()
        print("\nTodos os Exemplares:")
        for exemplar in todos_exemplares:
            print(exemplar)


        # --- Operações com Empréstimos ---
        print("\n--- Operações com Empréstimos ---")
        if novo_aluno and novo_exemplar:
            try:
                data_prevista = date.today() + timedelta(days=15)
                novo_emprestimo = emprestimo_service.create_emprestimo(
                    aluno=novo_aluno,     # <-- Passe o OBJETO novo_aluno
                    exemplar=novo_exemplar, # <-- Passe o OBJETO novo_exemplar
                    data_devolucao_prevista=data_prevista,
                    codEmp=test_emprestimo_codEmp # <-- PASSE O NOVO ID AQUI
                )
                print(f"Empréstimo criado: {novo_emprestimo}")

                todos_emprestimos = emprestimo_service.get_all_emprestimos()
                print("\nTodos os Empréstimos:")
                for emp in todos_emprestimos:
                    aluno_nome = emp.aluno.nome if emp.aluno else "N/A"
                    # ATENÇÃO AQUI: 'emp.exemplar' é uma LISTA de objetos Exemplar para Many-to-Many
                    # Você geralmente pegaria o primeiro (ou iteraria)
                    exemplar_tombo = emp.exemplar[0].tombo if emp.exemplar else "N/A"
                    print(f"ID: {emp.codEmp}, Aluno: {aluno_nome}, Exemplar (Tombo): {exemplar_tombo}, Data Empréstimo: {emp.data_emp}")
            except IntegrityError as e:
                db.rollback()
                print(f"Empréstimo já existe ou há problema de integridade (aluno/exemplar inválido): {e}")
                traceback.print_exc()
            except Exception as e:
                db.rollback()
                print(f"Erro ao criar/listar empréstimos: {e}")
                traceback.print_exc()
        else:
            print("Não foi possível realizar operações de empréstimo (aluno ou exemplar não disponível).")


    except Exception as e:
        print(f"Ocorreu um erro geral na aplicação: {e}")
        traceback.print_exc()
    finally:
        try:
            db_generator.close()
        except RuntimeError:
            pass # Ignora se o gerador já estiver fechado

if __name__ == "__main__":
    print("Iniciando a aplicação...")
    setup_database()
    run_example_operations()