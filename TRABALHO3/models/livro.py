# TRABALHO3/models/livro.py
"""Módulo para configuração de conexão com o banco de dados."""
import os
import sys

from typing import List, Optional
from sqlalchemy import BigInteger, String, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import Base # <--- MUITO IMPORTANTE: Mude para a sua Base

class Livro(Base):
    __tablename__ = 'livro'
    __table_args__ = (
        PrimaryKeyConstraint('cod_livro', name='livro_pkey'),
    )

    # ADICIONE autoincrement=True AQUI
    cod_livro: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True) # <-- CORREÇÃO
    titulo: Mapped[Optional[str]] = mapped_column(String(255))
    autor: Mapped[Optional[str]] = mapped_column(String(255))
    editora: Mapped[Optional[str]] = mapped_column(String(255)) # Verifique se esta linha está correta para seu DB
    ano: Mapped[Optional[int]] = mapped_column(BigInteger)

    exemplar: Mapped[List['Exemplar']] = relationship('Exemplar', back_populates='livro')

    def __repr__(self):
        return f"<Livro(cod_livro={self.cod_livro}, titulo='{self.titulo}')>"