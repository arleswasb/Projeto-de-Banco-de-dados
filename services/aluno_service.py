# services/aluno_service.py
# VERSÃO FINAL REVISADA

"""Módulo de serviço para operações CRUD na entidade Aluno."""

from sqlalchemy.orm import Session
from models import Aluno  
from typing import Optional, List

class AlunoService:
    """
    Classe de serviço para gerenciar as operações CRUD da entidade Aluno.
    """

    # Ele armazena a sessão (db) dentro do objeto de serviço.
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def criar_aluno(self, db: Session, nome: str, matricula: int, email: str, curso: str) -> Optional[Aluno]:
        """Cria um novo aluno no banco de dados."""
        try:

            db_aluno = Aluno(nome=nome, matricula=matricula, email=email, curso=curso)
            db.add(db_aluno)
            db.commit()
            db.refresh(db_aluno)
            return db_aluno
        except Exception as e:
            print(f"Erro ao criar aluno: {e}")
            db.rollback()
            return None

    def listar_alunos(self, db: Session, skip: int = 0, limit: int = 100) -> List[Aluno]:
        """Lista todos os alunos com paginação."""
        return db.query(Aluno).offset(skip).limit(limit).all()

    def buscar_aluno_por_id(self, db: Session, matricula: int) -> Optional[Aluno]:
        """Busca um aluno pela sua matrícula (chave primária)."""
        # CORREÇÃO: matricula agora é um int.
        return db.query(Aluno).filter(Aluno.matricula == matricula).first()

    def atualizar_aluno(self, db: Session, matricula: int, nome: Optional[str] = None, email: Optional[str] = None, curso: Optional[str] = None) -> Optional[Aluno]:
        """Atualiza os dados de um aluno existente."""
        # CORREÇÃO: matricula agora é um int.
        db_aluno = self.buscar_aluno_por_id(db, matricula)
        if not db_aluno:
            return None
        
        try:
            if nome is not None:
                db_aluno.nome = nome
            if email is not None:
                db_aluno.email = email
            if curso is not None:
                db_aluno.curso = curso
            
            db.commit()
            db.refresh(db_aluno)
            return db_aluno
        except Exception as e:
            print(f"Erro ao atualizar aluno: {e}")
            db.rollback()
            return None

    def remover_aluno(self, db: Session, matricula: int) -> bool:
        """Remove um aluno do banco de dados."""
        # CORREÇÃO: matricula agora é um int.
        db_aluno = self.buscar_aluno_por_id(db, matricula)
        if not db_aluno:
            return False
            
        try:
            db.delete(db_aluno)
            db.commit()
            return True
        except Exception as e:
            print(f"Erro ao remover aluno: {e}")
            db.rollback()
            return False

    # --- Métodos de busca adicionais (não obrigatórios, mas úteis) ---

    def buscar_aluno_por_email(self, db: Session, email: str) -> Optional[Aluno]:
        """Busca um aluno pelo email."""
        return db.query(Aluno).filter(Aluno.email == email).first()