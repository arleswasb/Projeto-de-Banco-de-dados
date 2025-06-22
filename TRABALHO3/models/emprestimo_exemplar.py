# trabalho3/models/emprestimo_exemplar.py
"""Módulo para configuração de conexão com o banco de dados."""
import os
import sys
from sqlalchemy import BigInteger, Column, ForeignKeyConstraint, PrimaryKeyConstraint, Table
from ..db import Base # <--- MUITO IMPORTANTE: Mude para a sua Base

# Esta é a tabela de associação para o relacionamento muitos-para-muitos entre Emprestimo e Exemplar
t_Emp_exemplar = Table(
    'Emp_exemplar', Base.metadata, # <--- Use Base.metadata do seu db.py
    Column('cod_Emp', BigInteger, primary_key=True, nullable=False),
    Column('Tombo', BigInteger, primary_key=True, nullable=False),
    ForeignKeyConstraint(['Tombo'], ['exemplar.tombo'], name='tombo'),
    ForeignKeyConstraint(['cod_Emp'], ['emprestimo.codEmp'], name='cod_emp'),
    PrimaryKeyConstraint('cod_Emp', 'Tombo', name='Emp_exemplar_pkey')
)