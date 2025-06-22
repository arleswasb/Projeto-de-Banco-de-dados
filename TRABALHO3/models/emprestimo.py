# TRABALHO3/models/emprestimo.py
"""Módulo para configuração de conexão com o banco de dados."""
import os
import sys

# Certifique-se de que todas as importações do SQLAlchemy estão aqui:
from sqlalchemy import Column, Integer, DateTime, ForeignKey, BigInteger, Date, PrimaryKeyConstraint, ForeignKeyConstraint # <-- ADICIONE ForeignKeyConstraint AQUI
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime # Para datetime.date e datetime.now()
from typing import List, Optional # Se estiver usando Optional ou List

from ..db import Base

class Emprestimo(Base):
    __tablename__ = 'emprestimo'
    __table_args__ = (
        # ForeignKeyConstraint agora estará definido
        ForeignKeyConstraint(['mat_aluno'], ['aluno.matricula'], name='mat_aluno'),
        PrimaryKeyConstraint('codEmp', name='emprestimo_pkey')
    )

    codEmp: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    data_emp: Mapped[datetime.date] = mapped_column(Date)
    data_dev: Mapped[Optional[datetime.date]] = mapped_column(Date)
    data_prev: Mapped[Optional[datetime.date]] = mapped_column(Date)
    atraso: Mapped[Optional[int]] = mapped_column(BigInteger)
    mat_aluno: Mapped[Optional[int]] = mapped_column(BigInteger)

    aluno: Mapped[Optional['Aluno']] = relationship('Aluno', back_populates='emprestimo')
    exemplar: Mapped[List['Exemplar']] = relationship('Exemplar', secondary='Emp_exemplar', back_populates='emprestimo')

    def __repr__(self):
        return f"<Emprestimo(codEmp={self.codEmp}, mat_aluno={self.mat_aluno}, data_emp={self.data_emp})>"