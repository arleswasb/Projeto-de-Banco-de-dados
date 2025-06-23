# TRABALHO3/models/livro.py
"""Modelo ORM para a tabela Livro."""

from typing import List, Optional
from sqlalchemy import BigInteger, String, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base

class Livro(Base):
    __tablename__ = 'livro'
    __table_args__ = (
        PrimaryKeyConstraint('cod_livro', name='livro_pkey'),
    )

    cod_livro: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    titulo: Mapped[Optional[str]] = mapped_column(String(255))
    autor: Mapped[Optional[str]] = mapped_column(String(255))
    editora: Mapped[Optional[str]] = mapped_column(String(255))
    ano: Mapped[Optional[int]] = mapped_column(BigInteger)

    # --- RELACIONAMENTO COM NOMENCLATURA MELHORADA ---

    # Relacionamento Um-para-Muitos com Exemplar.
    # Um livro pode ter vários exemplares. O nome 'exemplares' reflete a lista.
    exemplares: Mapped[List['Exemplar']] = relationship('Exemplar', back_populates='livro')

    def __repr__(self):
        return f"<Livro(cod_livro={self.cod_livro}, titulo='{self.titulo}')>"