# db.py
# VERSÃO FINAL REVISADA

"""Módulo para configuração de conexão com o banco de dados."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env na raiz do projeto
load_dotenv()

# Obtém a URL do banco de dados das variáveis de ambiente.
# Ex: postgresql://usuario:senha@host:porta/nome_do_banco
DATABASE_URL = os.getenv("DATABASE_URL")

# Valida se a variável de ambiente foi carregada corretamente
if not DATABASE_URL:
    raise ValueError("A variável de ambiente DATABASE_URL não está definida. Crie um arquivo .env na raiz do projeto.")

# Cria o motor (engine) do SQLAlchemy para se conectar ao banco de dados
engine = create_engine(DATABASE_URL)

# Cria uma "fábrica" de sessões, que será usada para criar sessões individuais
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria a classe Base da qual todos os seus modelos ORM irão herdar
Base = declarative_base()