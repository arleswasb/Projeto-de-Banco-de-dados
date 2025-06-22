# TRABALHO3/services/livro_service.py
"""Módulo para configuração de conexão com o banco de dados."""
import os
import sys
from sqlalchemy.orm import Session
from ..models.livro import Livro
from typing import Optional, List # Adicione esta linha

class LivroService:
    def __init__(self, db: Session):
        self.db = db

    def create_livro(self, titulo: str, autor: str, ano: int = None, editora: str = None, cod_livro: int = None) -> Livro:
        if cod_livro:
            db_livro = Livro(cod_livro=cod_livro, titulo=titulo, autor=autor, ano=ano, editora=editora)
        else:
            db_livro = Livro(titulo=titulo, autor=autor, ano=ano, editora=editora)

        self.db.add(db_livro)
        self.db.commit()
        self.db.refresh(db_livro)
        return db_livro

    def update_livro(self, cod_livro_existente: int, new_titulo: str = None, new_autor: str = None, new_ano: int = None, new_editora: str = None) -> Optional[Livro]: # Adicionado new_editora
        """Atualiza as informações de um livro existente."""
        db_livro = self.get_livro_by_cod_livro(cod_livro_existente)
        if db_livro:
            if new_titulo is not None:
                db_livro.titulo = new_titulo
            if new_autor is not None:
                db_livro.autor = new_autor
            if new_ano is not None:
                db_livro.ano = new_ano
            if new_editora is not None: # Atualiza editora
                db_livro.editora = new_editora
            self.db.commit()
            self.db.refresh(db_livro)
            return db_livro
        return None

    def get_livro_by_cod_livro(self, cod_livro: int) -> Optional[Livro]: # Adicionado type hint de retorno
        """Busca um livro pelo código do livro."""
        return self.db.query(Livro).filter(Livro.cod_livro == cod_livro).first()

    def get_all_livros(self, skip: int = 0, limit: int = 100) -> List[Livro]: # Adicionado type hints de parâmetros e retorno
        """Retorna todos os livros."""
        return self.db.query(Livro).offset(skip).limit(limit).all()

    def delete_livro(self, cod_livro: int) -> bool: # Mude o parâmetro de livro_id para cod_livro
        """Deleta um livro pelo código do livro (PK)."""
        db_livro = self.get_livro_by_cod_livro(cod_livro) # Use o método correto
        if db_livro:
            self.db.delete(db_livro)
            self.db.commit()
            return True
        return False

    def get_livro_by_titulo(self, titulo: str) -> Optional[Livro]:
        """Busca um livro pelo título."""
        return self.db.query(Livro).filter(Livro.titulo == titulo).first()

    def get_livro_by_autor(self, autor: str) -> Optional[Livro]:
        """Busca um livro pelo autor."""
        return self.db.query(Livro).filter(Livro.autor == autor).first()

    def get_livro_by_ano(self, ano: int) -> Optional[Livro]:
        """Busca um livro pelo ano de publicação."""
        return self.db.query(Livro).filter(Livro.ano == ano).first()