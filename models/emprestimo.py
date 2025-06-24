# TRABALHO3/models/emprestimo.py
"""Modelo ORM para a tabela Emprestimo."""

# Importações do SQLAlchemy e de tipos Python
from sqlalchemy import Column, BigInteger, Date, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Optional

from db import Base

class Emprestimo(Base):
    __tablename__ = 'emprestimo'
    __table_args__ = (
        ForeignKeyConstraint(['mat_aluno'], ['aluno.matricula'], name='mat_aluno'),
        PrimaryKeyConstraint('codEmp', name='emprestimo_pkey')
    )

    codEmp: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    data_emp: Mapped[datetime.date] = mapped_column(Date)
    data_dev: Mapped[Optional[datetime.date]] = mapped_column(Date)
    data_prev: Mapped[Optional[datetime.date]] = mapped_column(Date)
    atraso: Mapped[Optional[int]] = mapped_column(BigInteger)
    mat_aluno: Mapped[Optional[int]] = mapped_column(BigInteger)

    # --- RELACIONAMENTOS COM NOMENCLATURA MELHORADA ---

    # Relacionamento Muitos-para-Um com Aluno.
    # Um empréstimo pertence a um aluno.
    aluno: Mapped[Optional['Aluno']] = relationship('Aluno', back_populates='emprestimos')

    # Relacionamento Muitos-para-Muitos com Exemplar.
    # Um empréstimo pode ter vários exemplares.
    # O nome do atributo 'exemplares' (plural) reflete que é uma lista.
    exemplares: Mapped[List['Exemplar']] = relationship(
        'Exemplar', 
        secondary='Emp_exemplar',  # Mantido conforme seu BD existente
        back_populates='emprestimos'
    )

    def __repr__(self):
        return f"<Emprestimo(codEmp={self.codEmp}, mat_aluno={self.mat_aluno}, data_emp={self.data_emp})>"