# models/emprestimo.py
# VERSÃO FINAL REVISADA

"""Modelo ORM para a tabela Emprestimo."""

from sqlalchemy import BigInteger, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date  # Importando 'date' diretamente para clareza
from typing import List, Optional

from db import Base

# Importando as classes para os type hints dos relacionamentos
if TYPE_CHECKING:
    from .aluno import Aluno
    from .emprestimo_exemplar import EmprestimoExemplar

class Emprestimo(Base):
    __tablename__ = 'emprestimo'

    codEmp: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    
    # Chave estrangeira para Aluno. Definida diretamente na coluna.
    # Um empréstimo DEVE pertencer a um aluno, portanto nullable=False.
    mat_aluno: Mapped[int] = mapped_column(BigInteger, ForeignKey('aluno.matricula'), nullable=False)

    # Um empréstimo DEVE ter uma data, portanto nullable=False.
    data_emp: Mapped[date] = mapped_column(Date, nullable=False)
    
    # Data de devolução pode ser nula até a devolução ocorrer.
    data_dev: Mapped[Optional[date]] = mapped_column(Date)
    
    # Data prevista geralmente é obrigatória.
    data_prev: Mapped[date] = mapped_column(Date, nullable=False)

    atraso: Mapped[Optional[int]] = mapped_column(BigInteger)


    # --- RELACIONAMENTOS CORRIGIDOS ---

    # Relacionamento Muitos-para-Um com Aluno.
    # O nome 'emprestimos' deve corresponder ao back_populates na classe Aluno.
    aluno: Mapped["Aluno"] = relationship(back_populates='emprestimos')

    # Relacionamento Um-para-Muitos com a CLASSE de associação EmprestimoExemplar.
    exemplares_associados: Mapped[List["EmprestimoExemplar"]] = relationship(
        back_populates="emprestimo",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Emprestimo(codEmp={self.codEmp}, mat_aluno={self.mat_aluno}, data_emp={self.data_emp})>"