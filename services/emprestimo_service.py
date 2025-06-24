# TRABALHO3/services/emprestimo_service.py
"""Módulo de serviço para operações CRUD na entidade Emprestimo."""

from sqlalchemy.orm import Session, joinedload
from datetime import date
from typing import Optional, List

from models.emprestimo import Emprestimo
from models.exemplar import Exemplar # Necessário para o join na busca

class EmprestimoService:
    """
    Classe de serviço para gerenciar as operações CRUD da entidade Emprestimo.
    """

    def criar_emprestimo(self, db: Session, mat_aluno: str, data_prevista: date) -> Optional[Emprestimo]:
        """
        Cria um novo empréstimo, associado a um aluno.
        A associação com exemplares deve ser feita pelo EmprestimoExemplarService.
        """
        try:
            # A data do empréstimo é a data atual. A data de devolução é nula no início.
            db_emprestimo = Emprestimo(
                mat_aluno=mat_aluno,
                data_emp=date.today(),
                data_prev=data_prevista,
                data_dev=None,
                atraso=None
            )
            db.add(db_emprestimo)
            db.commit()
            db.refresh(db_emprestimo)
            return db_emprestimo
        except Exception as e:
            print(f"Erro ao criar empréstimo: {e}")
            db.rollback()
            return None

    def listar_emprestimos(self, db: Session, skip: int = 0, limit: int = 100) -> List[Emprestimo]:
        """Lista todos os empréstimos, carregando dados do aluno e dos exemplares."""
        # O uso de joinedload é uma ótima prática para evitar múltiplas queries (problema N+1)
        return db.query(Emprestimo).options(
            joinedload(Emprestimo.aluno),
            joinedload(Emprestimo.exemplares) # Usando 'exemplares' (plural) que definimos no modelo
        ).offset(skip).limit(limit).all()

    def buscar_emprestimo_por_id(self, db: Session, emprestimo_id: int) -> Optional[Emprestimo]:
        """Busca um empréstimo pelo seu ID (chave primária)."""
        return db.query(Emprestimo).filter(Emprestimo.codEmp == emprestimo_id).first()

    def atualizar_emprestimo(self, db: Session, emprestimo_id: int, data_prev: Optional[date] = None, data_dev: Optional[date] = None) -> Optional[Emprestimo]:
        """Atualiza os dados de um empréstimo existente."""
        db_emprestimo = self.buscar_emprestimo_por_id(db, emprestimo_id)
        if not db_emprestimo:
            return None
        
        try:
            if data_prev is not None:
                db_emprestimo.data_prev = data_prev
            if data_dev is not None:
                db_emprestimo.data_dev = data_dev
                # Aqui você poderia adicionar a lógica para calcular o atraso, se houver
                if data_dev > db_emprestimo.data_prev:
                    db_emprestimo.atraso = (data_dev - db_emprestimo.data_prev).days
                else:
                    db_emprestimo.atraso = 0

            db.commit()
            db.refresh(db_emprestimo)
            return db_emprestimo
        except Exception as e:
            print(f"Erro ao atualizar empréstimo: {e}")
            db.rollback()
            return None

    def remover_emprestimo(self, db: Session, emprestimo_id: int) -> bool:
        """
        Remove um empréstimo do banco de dados.
        Nota: A remoção em cascata das associações em 'Emp_exemplar' deve ser
        configurada no banco de dados (ON DELETE CASCADE) para isso funcionar
        sem violar restrições de chave estrangeira.
        """
        db_emprestimo = self.buscar_emprestimo_por_id(db, emprestimo_id)
        if not db_emprestimo:
            return False
            
        try:
            db.delete(db_emprestimo)
            db.commit()
            return True
        except Exception as e:
            print(f"Erro ao remover empréstimo: {e}")
            db.rollback()
            return False