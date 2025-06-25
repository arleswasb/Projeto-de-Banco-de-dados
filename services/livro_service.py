# services/livro_service.py
# VERSÃƒO FINAL REVISADA

from sqlalchemy.orm import Session, selectinload
from typing import Optional, List

# CORREÃ‡ÃƒO: Importando do pacote 'models'
from models import Livro

class LivroService:
    """
    Classe de serviÃ§o para gerenciar as operaÃ§Ãµes CRUD da entidade Livro.
    """
    # ADIÃ‡ÃƒO: Construtor para um design consistente.
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def criar_livro(self, titulo: str, autor: str, editora: Optional[str] = None, ano: Optional[int] = None) -> Optional[Livro]:
        """Cria um novo livro no banco de dados."""
        try:
            db_livro = Livro(titulo=titulo, autor=autor, editora=editora, ano=ano)
            self.db_session.add(db_livro)
            self.db_session.commit()
            self.db_session.refresh(db_livro)
            return db_livro
        except Exception as e:
            print(f"Erro ao criar livro: {e}")
            self.db_session.rollback()
            return None

    def listar_livros(self, skip: int = 0, limit: int = 100) -> List[Livro]:
        """Lista todos os livros, carregando os exemplares de forma otimizada."""
        # MELHORIA: Usando selectinload para evitar o problema N+1.
        # Ele carrega todos os exemplares de todos os livros listados em uma segunda query,
        # o que Ã© muito mais eficiente do que uma query por livro.
        return self.db_session.query(Livro).options(
            selectinload(Livro.exemplares)
        ).offset(skip).limit(limit).all()

    def buscar_livro_por_id(self, cod_livro: int) -> Optional[Livro]:
        """Busca um livro pelo seu cÃ³digo (chave primÃ¡ria)."""
        return self.db_session.query(Livro).filter(Livro.cod_livro == cod_livro).first()

    def atualizar_livro(self, cod_livro: int, titulo: Optional[str] = None, autor: Optional[str] = None, editora: Optional[str] = None, ano: Optional[int] = None) -> Optional[Livro]:
        """Atualiza os dados de um livro existente."""
        db_livro = self.buscar_livro_por_id(cod_livro)
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
            
            self.db_session.commit()
            self.db_session.refresh(db_livro)
            return db_livro
        except Exception as e:
            print(f"Erro ao atualizar livro: {e}")
            self.db_session.rollback()
            return None

    def remover_livro(self, cod_livro: int) -> bool:
        """Remove um livro do banco de dados."""
        db_livro = self.buscar_livro_por_id(cod_livro)
        if not db_livro:
            return False
            
        try:
            self.db_session.delete(db_livro)
            self.db_session.commit()
            return True
        except Exception as e:
            print(f"Erro ao remover livro: {e}")
            self.db_session.rollback()
            return False