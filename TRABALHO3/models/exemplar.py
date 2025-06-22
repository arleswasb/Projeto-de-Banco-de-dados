# trabalho3/models/exemplar.py
from typing import List, Optional
from sqlalchemy import BigInteger, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import Base # <--- MUITO IMPORTANTE: Mude para a sua Base

class Exemplar(Base):
    __tablename__ = 'exemplar' # Nome exato da tabela no seu DB
    __table_args__ = (
        ForeignKeyConstraint(['cod_livro'], ['livro.cod_livro'], name='exemplar_cod_livro_fkey'),
        PrimaryKeyConstraint('tombo', name='exemplar_pkey')
    )

    tombo: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    cod_livro: Mapped[Optional[int]] = mapped_column(BigInteger) # Coluna que é FK

    # Relacionamento: um exemplar pertence a um livro
    # 'Livro' deve ser o nome da CLASSE do seu modelo de Livro
    livro: Mapped[Optional['Livro']] = relationship('Livro', back_populates='exemplar')
    # Relacionamento muitos-para-muitos com Emprestimo através de Emp_exemplar
    emprestimo: Mapped[List['Emprestimo']] = relationship('Emprestimo', secondary='Emp_exemplar', back_populates='exemplar')

    def __repr__(self):
        return f"<Exemplar(tombo={self.tombo}, cod_livro={self.cod_livro})>"