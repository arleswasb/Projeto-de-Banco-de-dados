# trabalho3/models/exemplar.py
"""Modelo ORM para a tabela Exemplar."""

from typing import List, Optional
from sqlalchemy import BigInteger, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base

class Exemplar(Base):
    __tablename__ = 'exemplar'
    __table_args__ = (
        ForeignKeyConstraint(['cod_livro'], ['livro.cod_livro'], name='exemplar_cod_livro_fkey'),
        PrimaryKeyConstraint('tombo', name='exemplar_pkey')
    )

    tombo: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    cod_livro: Mapped[Optional[int]] = mapped_column(BigInteger)

    # --- RELACIONAMENTOS COM NOMENCLATURA MELHORADA ---

    # Relacionamento Muitos-para-Um com Livro.
    # Um exemplar pertence a um livro.
    livro: Mapped[Optional['Livro']] = relationship('Livro', back_populates='exemplares')

    # Relacionamento Muitos-para-Muitos com Emprestimo.
    # Um exemplar pode estar em vários empréstimos ao longo do tempo.
    emprestimos: Mapped[List['Emprestimo']] = relationship(
        'Emprestimo',
        secondary='Emp_exemplar', # Mantido conforme seu BD existente
        back_populates='exemplares'
    )

    def __repr__(self):
        return f"<Exemplar(tombo={self.tombo}, cod_livro={self.cod_livro})>"