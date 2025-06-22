# TRABALHO3/services/emprestimo_service.py
"""Módulo para configuração de conexão com o banco de dados."""
import os
import sys
from sqlalchemy.orm import Session, joinedload # Adicione 'joinedload' aqui
from datetime import date, datetime # Adicione 'datetime' aqui

from ..models.emprestimo import Emprestimo
from ..models.aluno import Aluno # Importe se precisar acessar atributos do aluno no serviço de emprestimo
from ..models.exemplar import Exemplar # Importe se precisar acessar atributos do exemplar

class EmprestimoService:
    def __init__(self, db: Session):
        self.db = db

    def create_emprestimo(self, aluno: Aluno, exemplar: Exemplar, data_devolucao_prevista: date, codEmp: int = None):
        """Cria um novo empréstimo."""
        if codEmp: # Se um codEmp for fornecido, use-o
            db_emprestimo = Emprestimo(
                codEmp=codEmp,
                data_emp=datetime.now(),
                data_prev=data_devolucao_prevista
            )
        else: # Caso contrário, deixe o SQLAlchemy/DB cuidar (se for SERIAL/autoincrement)
            db_emprestimo = Emprestimo(
                data_emp=datetime.now(),
                data_prev=data_devolucao_prevista
            )

        db_emprestimo.aluno = aluno
        db_emprestimo.exemplar.append(exemplar)

        self.db.add(db_emprestimo)
        self.db.commit()
        self.db.refresh(db_emprestimo)
        return db_emprestimo

    # E também o get_all_emprestimos que chamei no main.py
    def get_all_emprestimos(self, skip: int = 0, limit: int = 100):
        """Lista todos os empréstimos, com os dados de Aluno e Exemplar relacionados."""
        # joinedload já estará importado no topo
        return self.db.query(Emprestimo).options(
            joinedload(Emprestimo.aluno),
            joinedload(Emprestimo.exemplar)
        ).offset(skip).limit(limit).all()

    def get_emprestimo_by_id(self, emprestimo_id: int):
        """Busca um empréstimo pelo ID."""
        return self.db.query(Emprestimo).filter(Emprestimo.codEmp == emprestimo_id).first()

    def delete_emprestimo(self, emprestimo_id: int):
        """Deleta um empréstimo pelo ID."""
        db_emprestimo = self.get_emprestimo_by_id(emprestimo_id)
        if db_emprestimo:
            self.db.delete(db_emprestimo)
            self.db.commit()
            return True
        return False

    def update_emprestimo(self, emprestimo_id: int, data_devolucao_prevista: date = None):
        """Atualiza um empréstimo existente."""
        db_emprestimo = self.get_emprestimo_by_id(emprestimo_id)
        if db_emprestimo:
            if data_devolucao_prevista:
                db_emprestimo.data_prev = data_devolucao_prevista
            self.db.commit()
            self.db.refresh(db_emprestimo)
            return db_emprestimo
        return None

    def get_emprestimos_by_aluno(self, mat_aluno: int): # Renomeie o parâmetro para clareza
        """Busca todos os empréstimos de um aluno específico."""
        return self.db.query(Emprestimo).filter(Emprestimo.mat_aluno == mat_aluno).all()

    def get_emprestimos_by_exemplar(self, exemplar_tombo: int): # Renomeie o parâmetro para clareza
        """Busca todos os empréstimos de um exemplar específico."""
        # Se o relacionamento for muitos-para-muitos, a busca é um pouco diferente
        # Você pode filtrar por emprestimos que tenham o exemplar específico na coleção
        # Ou, mais comumente, filtrar por um JOIN na tabela associativa
        return self.db.query(Emprestimo).join(Emprestimo.exemplar).filter(Exemplar.tombo == exemplar_tombo).all()