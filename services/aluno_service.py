# services/aluno_service.py
# VERSÃO FINAL E CORRETA

from sqlalchemy.orm import Session
from models import Aluno
from typing import Optional, List

class AlunoService:
    """
    Classe de serviço para gerenciar as operações CRUD da entidade Aluno.
    """
    # Este construtor armazena a sessão para ser usada por todos os métodos.
    def __init__(self, db_session: Session):
        self.db_session = db_session

    # Os métodos agora usam 'self.db_session' e não recebem mais 'db' como argumento.
    def criar_aluno(self, nome: str, matricula: int, email: str, curso: str) -> Optional[Aluno]:
        try:
            db_aluno = Aluno(nome=nome, matricula=matricula, email=email, curso=curso)
            self.db_session.add(db_aluno)
            self.db_session.commit()
            self.db_session.refresh(db_aluno)
            return db_aluno
        except Exception as e:
            print(f"Erro ao criar aluno: {e}")
            self.db_session.rollback()
            return None

    def listar_alunos(self, skip: int = 0, limit: int = 100) -> List[Aluno]:
        return self.db_session.query(Aluno).offset(skip).limit(limit).all()

    def buscar_aluno_por_id(self, matricula: int) -> Optional[Aluno]:
        return self.db_session.query(Aluno).filter(Aluno.matricula == matricula).first()

    def atualizar_aluno(self, matricula: int, nome: Optional[str] = None, email: Optional[str] = None, curso: Optional[str] = None) -> Optional[Aluno]:
        db_aluno = self.buscar_aluno_por_id(matricula)
        if not db_aluno:
            return None
        
        try:
            if nome is not None:
                db_aluno.nome = nome
            if email is not None:
                db_aluno.email = email
            if curso is not None:
                db_aluno.curso = curso
            
            self.db_session.commit()
            self.db_session.refresh(db_aluno)
            return db_aluno
        except Exception as e:
            print(f"Erro ao atualizar aluno: {e}")
            self.db_session.rollback()
            return None

    def remover_aluno(self, matricula: int) -> bool:
        db_aluno = self.buscar_aluno_por_id(matricula)
        if not db_aluno:
            return False
            
        try:
            self.db_session.delete(db_aluno)
            self.db_session.commit()
            return True
        except Exception as e:
            print(f"Erro ao remover aluno: {e}")
            self.db_session.rollback()
            return False

    def buscar_aluno_por_email(self, email: str) -> Optional[Aluno]:
        return self.db_session.query(Aluno).filter(Aluno.email == email).first()