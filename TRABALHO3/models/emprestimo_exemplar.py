# trabalho3/models/emprestimo_exemplar.py
"""Modelo ORM para a tabela associativa EmprestimoExemplar."""

from sqlalchemy import BigInteger, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from ..db import Base

class EmprestimoExemplar(Base):
    """
    Classe que mapeia a tabela associativa 'Emp_exemplar'.
    Esta tabela representa o relacionamento Muitos-para-Muitos
    entre as tabelas 'emprestimo' e 'exemplar'.
    """
    __tablename__ = 'Emp_exemplar'  # Nome da tabela conforme seu banco de dados

    # Mapeamento das colunas da tabela associativa.
    # Os nomes 'cod_Emp' e 'Tombo' são mantidos para corresponder ao seu schema.
    cod_Emp: Mapped[int] = mapped_column(BigInteger)
    Tombo: Mapped[int] = mapped_column(BigInteger)

    # Definição das chaves primárias e estrangeiras
    __table_args__ = (
        ForeignKeyConstraint(['cod_Emp'], ['emprestimo.codEmp'], name='cod_emp'),
        ForeignKeyConstraint(['Tombo'], ['exemplar.tombo'], name='tombo'),
        PrimaryKeyConstraint('cod_Emp', 'Tombo', name='Emp_exemplar_pkey')
    )

    def __repr__(self):
        return f"<EmprestimoExemplar(cod_Emp={self.cod_Emp}, Tombo={self.Tombo})>"