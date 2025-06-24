# services/emprestimo_exemplar_service.py
# VERSÃO FINAL REVISADA

from sqlalchemy.orm import Session
# CORREÇÃO: Importando do pacote 'models'
from models import Emprestimo, Exemplar, EmprestimoExemplar
from typing import List

class EmprestimoExemplarService:
    """
    Classe de serviço para gerenciar as operações na tabela associativa EmprestimoExemplar.
    Adapta os métodos CRUD para o contexto de uma relação.
    """
    # ADIÇÃO: Construtor para um design consistente com outros serviços.
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def adicionar_exemplar_a_emprestimo(self, cod_emprestimo: int, tombo_exemplar: int) -> EmprestimoExemplar | None:
        """
        Associa um exemplar a um empréstimo. (Operação 'criar' da associação).
        """
        try:
            # Verifica se o empréstimo e o exemplar existem
            emprestimo = self.db_session.query(Emprestimo).filter_by(codEmp=cod_emprestimo).first()
            exemplar = self.db_session.query(Exemplar).filter_by(tombo=tombo_exemplar).first()

            if not emprestimo:
                print(f"Erro: Empréstimo com código {cod_emprestimo} não encontrado.")
                return None
            if not exemplar:
                print(f"Erro: Exemplar com tombo {tombo_exemplar} não encontrado.")
                return None

            nova_associacao = EmprestimoExemplar(cod_Emp=cod_emprestimo, Tombo=tombo_exemplar)
            
            self.db_session.add(nova_associacao)
            self.db_session.commit()
            print(f"Exemplar {tombo_exemplar} adicionado ao Empréstimo {cod_emprestimo} com sucesso.")
            return nova_associacao
        except Exception as e:
            self.db_session.rollback()
            print(f"Erro ao adicionar exemplar ao empréstimo: {e}")
            return None

    def listar_exemplares_de_emprestimo(self, cod_emprestimo: int) -> List[Exemplar]:
        """
        Lista todos os exemplares associados a um determinado empréstimo.
        """
        emprestimo = self.db_session.query(Emprestimo).filter_by(codEmp=cod_emprestimo).first()
        
        if not emprestimo:
            print(f"Erro: Empréstimo com código {cod_emprestimo} não encontrado.")
            return []
        
        # CORREÇÃO: Iterar sobre os objetos de associação para retornar os objetos Exemplar.
        # 1. Acessa a lista de associações (`emprestimo.exemplares_associados`)
        # 2. Para cada objeto 'assoc' na lista, pega o atributo 'assoc.exemplar'
        exemplares = [assoc.exemplar for assoc in emprestimo.exemplares_associados]
        return exemplares

    def remover_exemplar_de_emprestimo(self, cod_emprestimo: int, tombo_exemplar: int) -> bool:
        """
        Remove a associação entre um exemplar e um empréstimo. (Operação 'remover').
        """
        try:
            associacao = self.db_session.query(EmprestimoExemplar).filter_by(
                cod_Emp=cod_emprestimo,
                Tombo=tombo_exemplar
            ).first()

            if not associacao:
                print("Erro: Associação entre o Empréstimo e o Exemplar não encontrada.")
                return False

            self.db_session.delete(associacao)
            self.db_session.commit()
            print(f"Associação do Exemplar {tombo_exemplar} com o Empréstimo {cod_emprestimo} removida com sucesso.")
            return True
        except Exception as e:
            self.db_session.rollback()
            print(f"Erro ao remover exemplar do empréstimo: {e}")
            return False