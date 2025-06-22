# trabalho3/models/aluno.py
from typing import List, Optional
from sqlalchemy import BigInteger, String, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import Base # <--- MUITO IMPORTANTE: Mude para a sua Base

class Aluno(Base):
    __tablename__ = 'aluno' # Nome exato da tabela no seu DB
    __table_args__ = (
        PrimaryKeyConstraint('matricula', name='aluno_pkey'), # Nome da PK no DB
    )

    matricula: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    nome: Mapped[Optional[str]] = mapped_column(String(255))
    curso: Mapped[Optional[str]] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255))

    # Relacionamento: um aluno pode ter muitos empréstimos
    # 'Emprestimo' deve ser o nome da CLASSE do seu modelo de Emprestimo
    emprestimo: Mapped[List['Emprestimo']] = relationship('Emprestimo', back_populates='aluno')

    def __repr__(self):
        return f"<Aluno(matricula={self.matricula}, nome='{self.nome}', email='{self.email}')>"