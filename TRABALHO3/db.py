# trabalho3/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a URL do banco de dados das variáveis de ambiente.
# Ex: postgresql://usuario:senha@host:porta/nome_do_banco
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("A variável de ambiente DATABASE_URL não está definida. Crie um arquivo .env na raiz do projeto.")

# Cria o motor (engine) do SQLAlchemy para se conectar ao banco de dados
Engine = create_engine(DATABASE_URL)

# Cria uma sessão local do banco de dados, que será usada para interagir com o DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

# Base declarativa para seus modelos ORM
Base = declarative_base()

def get_db():
    """
    Função geradora para fornecer uma sessão de banco de dados.
    Usada como uma dependência para garantir que a sessão seja fechada corretamente.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Como você já tem o banco de dados criado, Base.metadata.create_all(bind=Engine)
# não é estritamente necessário para criar tabelas, mas pode ser útil para o SQLAlchemy
# "conhecer" o esquema se você não usar migrações.
# Para migrações controladas, use Alembic (ver passo 7).