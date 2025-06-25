# models/livro.py
# VERSÃO FINAL REVISADA

"""Modelo ORM para a tabela Livro."""

from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base

# Importando a classe para o type hint do relacionamento
if TYPE_CHECKING:
    from .exemplar import Exemplar

class Livro(Base):
    __tablename__ = 'livro'

    cod_livro: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    # Corrigido para não aceitar valores nulos para informações essenciais.
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    autor: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Editora e ano podem ser opcionais, dependendo da sua regra de negócio.
    # Mantidos como Optional por enquanto.
    editora: Mapped[Optional[str]] = mapped_column(String(255))
    ano: Mapped[Optional[int]] = mapped_column(BigInteger)


    # --- RELACIONAMENTO ---
    # Esta definição já estava correta.
    # Um livro pode ter vários exemplares.
    # O 'back_populates' conecta este relacionamento ao atributo 'livro' na classe Exemplar.
    exemplares: Mapped[List["Exemplar"]] = relationship(back_populates='livro')

    def __repr__(self):
        return f"<Livro(cod_livro={self.cod_livro}, titulo='{self.titulo}')>"