# models/emprestimo_exemplar.py

from sqlalchemy import BigInteger, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base
from typing import TYPE_CHECKING

# Para evitar importação circular com type hints
if TYPE_CHECKING:
    from .emprestimo import Emprestimo
    from .exemplar import Exemplar

class EmprestimoExemplar(Base):
    __tablename__ = 'Emp_exemplar'

    cod_Emp: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    Tombo: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(['cod_Emp'], ['emprestimo.codEmp']),
        ForeignKeyConstraint(['Tombo'], ['exemplar.tombo']),
    )
    
    # --- Relacionamentos ORM (essencial para o padrão funcionar) ---
    emprestimo: Mapped["Emprestimo"] = relationship(back_populates="exemplares_associados")
    exemplar: Mapped["Exemplar"] = relationship(back_populates="emprestimos_associados")

    def __repr__(self):
        return f"<EmprestimoExemplar(cod_Emp={self.cod_Emp}, Tombo={self.Tombo})>"