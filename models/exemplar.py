# models/exemplar.py
# VERSÃO FINAL REVISADA

"""Modelo ORM para a tabela Exemplar."""

from typing import List
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base

# Importando as classes para os type hints dos relacionamentos
if TYPE_CHECKING:
    from .livro import Livro
    from .emprestimo_exemplar import EmprestimoExemplar

class Exemplar(Base):
    __tablename__ = 'exemplar'

    tombo: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    # Um exemplar DEVE pertencer a um livro, portanto nullable=False.
    # A ForeignKey é definida diretamente na coluna.
    cod_livro: Mapped[int] = mapped_column(BigInteger, ForeignKey('livro.cod_livro'), nullable=False)


    # --- RELACIONAMENTOS CORRIGIDOS ---

    # Relacionamento Muitos-para-Um com Livro.
    # O nome 'exemplares' deve corresponder ao back_populates na classe Livro.
    # Removido o 'Optional' pois um exemplar sempre terá um livro associado.
    livro: Mapped["Livro"] = relationship(back_populates='exemplares')

    # Relacionamento Um-para-Muitos com a CLASSE de associação EmprestimoExemplar.
    # Esta é a correção CRÍTICA.
    emprestimos_associados: Mapped[List["EmprestimoExemplar"]] = relationship(
        back_populates="exemplar",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Exemplar(tombo={self.tombo}, cod_livro={self.cod_livro})>"