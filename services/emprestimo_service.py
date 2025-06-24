# services/emprestimo_service.py
# VERSÃO FINAL REVISADA

from sqlalchemy.orm import Session, joinedload
from datetime import date
from typing import Optional, List

# CORREÇÃO: Importando do pacote 'models'
from models import Emprestimo, Aluno, Exemplar, EmprestimoExemplar

class EmprestimoService:
    """
    Classe de serviço para gerenciar as operações CRUD da entidade Emprestimo.
    """
    # ADIÇÃO: Construtor para um design consistente.
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def criar_emprestimo(self, mat_aluno: int, data_prevista: date) -> Optional[Emprestimo]:
        """Cria um novo empréstimo, associado a um aluno."""
        try:
            # CORREÇÃO: mat_aluno agora é um int.
            db_emprestimo = Emprestimo(
                mat_aluno=mat_aluno,
                data_emp=date.today(),
                data_prev=data_prevista
            )
            self.db_session.add(db_emprestimo)
            self.db_session.commit()
            self.db_session.refresh(db_emprestimo)
            return db_emprestimo
        except Exception as e:
            print(f"Erro ao criar empréstimo: {e}")
            self.db_session.rollback()
            return None

    def listar_emprestimos(self, skip: int = 0, limit: int = 100) -> List[Emprestimo]:
        """Lista todos os empréstimos, carregando dados do aluno e dos exemplares."""
        return self.db_session.query(Emprestimo).options(
            # Carrega o objeto Aluno relacionado
            joinedload(Emprestimo.aluno),
            # CORREÇÃO CRÍTICA: Carrega a associação E o exemplar final em uma só query
            joinedload(Emprestimo.exemplares_associados).joinedload(EmprestimoExemplar.exemplar)
        ).offset(skip).limit(limit).all()

    def buscar_emprestimo_por_id(self, emprestimo_id: int) -> Optional[Emprestimo]:
        """Busca um empréstimo pelo seu ID (chave primária)."""
        return self.db_session.query(Emprestimo).filter(Emprestimo.codEmp == emprestimo_id).first()

    def atualizar_emprestimo(self, emprestimo_id: int, data_prev: Optional[date] = None, data_dev: Optional[date] = None) -> Optional[Emprestimo]:
        """Atualiza os dados de um empréstimo existente."""
        db_emprestimo = self.buscar_emprestimo_por_id(emprestimo_id)
        if not db_emprestimo:
            return None
        
        try:
            if data_prev is not None:
                db_emprestimo.data_prev = data_prev
            if data_dev is not None:
                db_emprestimo.data_dev = data_dev
                # Lógica para calcular o atraso
                if db_emprestimo.data_prev and data_dev > db_emprestimo.data_prev:
                    db_emprestimo.atraso = (data_dev - db_emprestimo.data_prev).days
                else:
                    db_emprestimo.atraso = 0

            self.db_session.commit()
            self.db_session.refresh(db_emprestimo)
            return db_emprestimo
        except Exception as e:
            print(f"Erro ao atualizar empréstimo: {e}")
            self.db_session.rollback()
            return None

    def remover_emprestimo(self, emprestimo_id: int) -> bool:
        """Remove um empréstimo. O cascade="all, delete-orphan" no modelo
           garante que as associações em EmprestimoExemplar também sejam removidas."""
        db_emprestimo = self.buscar_emprestimo_por_id(emprestimo_id)
        if not db_emprestimo:
            return False
            
        try:
            self.db_session.delete(db_emprestimo)
            self.db_session.commit()
            return True
        except Exception as e:
            print(f"Erro ao remover empréstimo: {e}")
            self.db_session.rollback()
            return False