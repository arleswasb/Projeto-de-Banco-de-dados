# trabalho3/services/exemplar_service.py
"""Módulo para configuração de conexão com o banco de dados."""
import os
import sys
from sqlalchemy.orm import Session
from ..models.exemplar import Exemplar
from ..models.livro import Livro # Importe se precisar acessar dados do livro
from typing import Optional, List

class ExemplarService:
    def __init__(self, db: Session):
        self.db = db

    def get_exemplar_by_tombo(self, tombo: int):
        return self.db.query(Exemplar).filter(Exemplar.tombo == tombo).first()

    def get_all_exemplares(self, skip: int = 0, limit: int = 100):
        from sqlalchemy.orm import joinedload
        return self.db.query(Exemplar).options(
            joinedload(Exemplar.livro) # Carrega os dados do livro relacionado
        ).offset(skip).limit(limit).all()

    def create_exemplar(self, tombo: int, cod_livro: int):
        db_exemplar = Exemplar(tombo=tombo, cod_livro=cod_livro)
        self.db.add(db_exemplar)
        self.db.commit()
        self.db.refresh(db_exemplar)
        return db_exemplar

    # Adicione métodos para update e delete de exemplares
    def delete_exemplar(self, tombo: int):
        db_exemplar = self.get_exemplar_by_tombo(tombo)
        if db_exemplar:
            self.db.delete(db_exemplar)
            self.db.commit()
            return True
        return False
    
    def update_exemplar(self, tombo_existente: int, new_cod_livro: int = None) -> Optional[Exemplar]:
        """Atualiza as informações de um exemplar existente pelo tombo."""
        db_exemplar = self.get_exemplar_by_tombo(tombo_existente)
        if db_exemplar:
            if new_cod_livro is not None:
                # Opcional: Você pode querer verificar se o new_cod_livro realmente existe na tabela Livro
                # antes de atribuir, para evitar erros de FK.
                db_exemplar.cod_livro = new_cod_livro
            self.db.commit()
            self.db.refresh(db_exemplar)
            return db_exemplar
        return None