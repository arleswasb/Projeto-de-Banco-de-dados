# services/emprestimo_exemplar_service.py

# Importa os modelos necessários
from models.emprestimo import Emprestimo
from models.exemplar import Exemplar
from models.emprestimo_exemplar import EmprestimoExemplar

class EmprestimoExemplarService:
    """
    Classe de serviço para gerenciar as operações na tabela associativa EmprestimoExemplar.
    Adapta os métodos CRUD para o contexto de uma relação.
    """

    def adicionar_exemplar_a_emprestimo(self, session, cod_emprestimo: int, tombo_exemplar: int):
        """
        Associa um exemplar a um empréstimo. (Operação 'criar' da associação).
        """
        try:
            # Verifica se o empréstimo e o exemplar existem
            emprestimo = session.query(Emprestimo).filter_by(codEmp=cod_emprestimo).first()
            exemplar = session.query(Exemplar).filter_by(tombo=tombo_exemplar).first()

            if not emprestimo:
                print(f"Erro: Empréstimo com código {cod_emprestimo} não encontrado.")
                return None
            if not exemplar:
                print(f"Erro: Exemplar com tombo {tombo_exemplar} não encontrado.")
                return None

            # Cria a nova associação usando os nomes de coluna corretos ('cod_Emp', 'Tombo')
            nova_associacao = EmprestimoExemplar(
                cod_Emp=cod_emprestimo,
                Tombo=tombo_exemplar
            )
            
            session.add(nova_associacao)
            session.commit()
            print(f"Exemplar {tombo_exemplar} adicionado ao Empréstimo {cod_emprestimo} com sucesso.")
            return nova_associacao
        except Exception as e:
            session.rollback()
            print(f"Erro ao adicionar exemplar ao empréstimo: {e}")
            return None

    def listar_exemplares_de_emprestimo(self, session, cod_emprestimo: int):
        """
        Lista todos os exemplares associados a um determinado empréstimo. (Operação 'listar').
        """
        try:
            # A forma mais elegante, usando o relacionamento que definimos no modelo Emprestimo
            emprestimo = session.query(Emprestimo).filter_by(codEmp=cod_emprestimo).first()
            
            if not emprestimo:
                print(f"Erro: Empréstimo com código {cod_emprestimo} não encontrado.")
                return []
            
            # O SQLAlchemy faz todo o trabalho de JOIN por baixo dos panos
            return emprestimo.exemplares

        except Exception as e:
            print(f"Erro ao listar exemplares do empréstimo: {e}")
            return []

    def remover_exemplar_de_emprestimo(self, session, cod_emprestimo: int, tombo_exemplar: int):
        """
        Remove a associação entre um exemplar e um empréstimo. (Operação 'remover').
        """
        try:
            # Encontra a associação específica usando os nomes de coluna corretos
            associacao = session.query(EmprestimoExemplar).filter_by(
                cod_Emp=cod_emprestimo,
                Tombo=tombo_exemplar
            ).first()

            if not associacao:
                print("Erro: Associação entre o Empréstimo e o Exemplar não encontrada.")
                return False

            session.delete(associacao)
            session.commit()
            print(f"Associação do Exemplar {tombo_exemplar} com o Empréstimo {cod_emprestimo} removida com sucesso.")
            return True
        except Exception as e:
            session.rollback()
            print(f"Erro ao remover exemplar do empréstimo: {e}")
            return False