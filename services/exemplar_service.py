# trabalho3/services/exemplar_service.py
"""Módulo de serviço para operações CRUD na entidade Exemplar."""

from sqlalchemy.orm import Session, joinedload
from typing import Optional, List

from models.exemplar import Exemplar

class ExemplarService:
    """
    Classe de serviço para gerenciar as operações CRUD da entidade Exemplar.
    """

    def criar_exemplar(self, db: Session, tombo: int, cod_livro: int) -> Optional[Exemplar]:
        """
        Cria um novo exemplar no banco de dados.
        O 'tombo' é uma PK não incremental, por isso é fornecido manualmente.
        """
        try:
            # Opcional: Verificar se o livro com 'cod_livro' existe antes de criar.
            # livro_existe = db.query(Livro).filter(Livro.cod_livro == cod_livro).first()
            # if not livro_existe:
            #     print(f"Erro: Livro com código {cod_livro} não encontrado.")
            #     return None

            db_exemplar = Exemplar(tombo=tombo, cod_livro=cod_livro)
            db.add(db_exemplar)
            db.commit()
            db.refresh(db_exemplar)
            return db_exemplar
        except Exception as e:
            print(f"Erro ao criar exemplar: {e}")
            db.rollback()
            return None

    def listar_exemplares(self, db: Session, skip: int = 0, limit: int = 100) -> List[Exemplar]:
        """Lista todos os exemplares, carregando os dados do livro relacionado."""
        return db.query(Exemplar).options(
            joinedload(Exemplar.livro)
        ).offset(skip).limit(limit).all()

    def buscar_exemplar_por_id(self, db: Session, tombo: int) -> Optional[Exemplar]:
        """Busca um exemplar pelo seu 'tombo' (chave primária)."""
        return db.query(Exemplar).filter(Exemplar.tombo == tombo).first()

    def atualizar_exemplar(self, db: Session, tombo: int, cod_livro: Optional[int] = None) -> Optional[Exemplar]:
        """Atualiza os dados de um exemplar existente."""
        db_exemplar = self.buscar_exemplar_por_id(db, tombo)
        if not db_exemplar:
            return None
        
        try:
            if cod_livro is not None:
                db_exemplar.cod_livro = cod_livro
            
            db.commit()
            db.refresh(db_exemplar)
            return db_exemplar
        except Exception as e:
            print(f"Erro ao atualizar exemplar: {e}")
            db.rollback()
            return None

    def remover_exemplar(self, db: Session, tombo: int) -> bool:
        """Remove um exemplar do banco de dados."""
        db_exemplar = self.buscar_exemplar_por_id(db, tombo)
        if not db_exemplar:
            return False
            
        try:
            db.delete(db_exemplar)
            db.commit()
            return True
        except Exception as e:
            print(f"Erro ao remover exemplar: {e}")
            db.rollback()
            return False