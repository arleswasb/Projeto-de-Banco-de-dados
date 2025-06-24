# services/exemplar_service.py
# VERSÃO FINAL REVISADA

from sqlalchemy.orm import Session, joinedload
from typing import Optional, List

# CORREÇÃO: Importando do pacote 'models'
from models import Exemplar, Livro

class ExemplarService:
    """
    Classe de serviço para gerenciar as operações CRUD da entidade Exemplar.
    """
    # ADIÇÃO: Construtor para um design consistente.
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def criar_exemplar(self, tombo: int, cod_livro: int) -> Optional[Exemplar]:
        """
        Cria um novo exemplar no banco de dados.
        O 'tombo' é uma PK não incremental, por isso é fornecido manualmente.
        """
        try:
            # MELHORIA: Verificação de existência do livro foi ativada.
            # Isso torna o serviço mais robusto e fornece erros mais claros.
            livro_existe = self.db_session.query(Livro).filter(Livro.cod_livro == cod_livro).first()
            if not livro_existe:
                print(f"Erro: Livro com código {cod_livro} não encontrado. Não é possível criar o exemplar.")
                return None

            db_exemplar = Exemplar(tombo=tombo, cod_livro=cod_livro)
            self.db_session.add(db_exemplar)
            self.db_session.commit()
            self.db_session.refresh(db_exemplar)
            return db_exemplar
        except Exception as e:
            print(f"Erro ao criar exemplar: {e}")
            self.db_session.rollback()
            return None

    def listar_exemplares(self, skip: int = 0, limit: int = 100) -> List[Exemplar]:
        """Lista todos os exemplares, carregando os dados do livro relacionado."""
        # Esta implementação já estava perfeita.
        return self.db_session.query(Exemplar).options(
            joinedload(Exemplar.livro)
        ).offset(skip).limit(limit).all()

    def buscar_exemplar_por_id(self, tombo: int) -> Optional[Exemplar]:
        """Busca um exemplar pelo seu 'tombo' (chave primária)."""
        return self.db_session.query(Exemplar).filter(Exemplar.tombo == tombo).first()

    def atualizar_exemplar(self, tombo: int, cod_livro: Optional[int] = None) -> Optional[Exemplar]:
        """Atualiza os dados de um exemplar existente."""
        db_exemplar = self.buscar_exemplar_por_id(tombo)
        if not db_exemplar:
            return None
        
        try:
            if cod_livro is not None:
                # MELHORIA: Adicionada verificação aqui também.
                livro_existe = self.db_session.query(Livro).filter(Livro.cod_livro == cod_livro).first()
                if not livro_existe:
                    print(f"Erro: Livro com código {cod_livro} não encontrado. Atualização cancelada.")
                    self.db_session.rollback() # Desfaz qualquer mudança pendente
                    return None
                db_exemplar.cod_livro = cod_livro
            
            self.db_session.commit()
            self.db_session.refresh(db_exemplar)
            return db_exemplar
        except Exception as e:
            print(f"Erro ao atualizar exemplar: {e}")
            self.db_session.rollback()
            return None

    def remover_exemplar(self, tombo: int) -> bool:
        """Remove um exemplar do banco de dados."""
        db_exemplar = self.buscar_exemplar_por_id(tombo)
        if not db_exemplar:
            return False
            
        try:
            self.db_session.delete(db_exemplar)
            self.db_session.commit()
            return True
        except Exception as e:
            print(f"Erro ao remover exemplar: {e}")
            self.db_session.rollback()
            return False