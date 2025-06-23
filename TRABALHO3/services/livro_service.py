# trabalho3/services/livro_service.py
"""Módulo de serviço para operações CRUD na entidade Livro."""

from sqlalchemy.orm import Session
from typing import Optional, List

from ..models.livro import Livro

class LivroService:
    """
    Classe de serviço para gerenciar as operações CRUD da entidade Livro.
    """

    def criar_livro(self, db: Session, titulo: str, autor: str, editora: Optional[str] = None, ano: Optional[int] = None) -> Optional[Livro]:
        """Cria um novo livro no banco de dados."""
        try:
            db_livro = Livro(titulo=titulo, autor=autor, editora=editora, ano=ano)
            db.add(db_livro)
            db.commit()
            db.refresh(db_livro)
            return db_livro
        except Exception as e:
            print(f"Erro ao criar livro: {e}")
            db.rollback()
            return None

    def listar_livros(self, db: Session, skip: int = 0, limit: int = 100) -> List[Livro]:
        """Lista todos os livros com paginação."""
        return db.query(Livro).offset(skip).limit(limit).all()

    def buscar_livro_por_id(self, db: Session, cod_livro: int) -> Optional[Livro]:
        """Busca um livro pelo seu código (chave primária)."""
        return db.query(Livro).filter(Livro.cod_livro == cod_livro).first()

    def atualizar_livro(self, db: Session, cod_livro: int, titulo: Optional[str] = None, autor: Optional[str] = None, editora: Optional[str] = None, ano: Optional[int] = None) -> Optional[Livro]:
        """Atualiza os dados de um livro existente."""
        db_livro = self.buscar_livro_por_id(db, cod_livro)
        if not db_livro:
            return None
        
        try:
            if titulo is not None:
                db_livro.titulo = titulo
            if autor is not None:
                db_livro.autor = autor
            if editora is not None:
                db_livro.editora = editora
            if ano is not None:
                db_livro.ano = ano
            
            db.commit()
            db.refresh(db_livro)
            return db_livro
        except Exception as e:
            print(f"Erro ao atualizar livro: {e}")
            db.rollback()
            return None

    def remover_livro(self, db: Session, cod_livro: int) -> bool:
        """
        Remove um livro do banco de dados.
        Nota: Isso pode falhar se existirem exemplares associados a este livro,
        a menos que a remoção em cascata (ON DELETE CASCADE) esteja configurada no banco.
        """
        db_livro = self.buscar_livro_por_id(db, cod_livro)
        if not db_livro:
            return False
            
        try:
            db.delete(db_livro)
            db.commit()
            return True
        except Exception as e:
            print(f"Erro ao remover livro: {e}")
            db.rollback()
            return False