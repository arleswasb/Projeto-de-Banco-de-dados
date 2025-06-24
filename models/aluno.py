# models/aluno.py
# VERSÃO FINAL REVISADA

"""Módulo que define o modelo ORM para a tabela Aluno."""
from typing import List
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base

class Aluno(Base):
    """
    Classe que mapeia a tabela 'aluno' no banco de dados.
    """
    __tablename__ = 'aluno'

    # Colunas da tabela
    # A definição da chave primária diretamente na coluna é mais clara.
    matricula: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    # Corrigido para não aceitar valores nulos, conforme exemplo do roteiro.
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    curso: Mapped[str] = mapped_column(String(255), nullable=False)

    # Corrigido para não ser nulo e ser único.
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    # Relacionamento: um aluno pode ter muitos empréstimos.
    # Esta definição já estava correta.
    # O 'back_populates' conecta este relacionamento ao atributo 'aluno' na classe Emprestimo.
    emprestimos: Mapped[List["Emprestimo"]] = relationship(back_populates='aluno')

    def __repr__(self) -> str:
        return f"<Aluno(matricula={self.matricula}, nome='{self.nome}', email='{self.email}')>"