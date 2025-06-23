# TRABALHO3/services/aluno_service.py
"""Módulo para configuração de conexão com o banco de dados."""
import os
import sys
from sqlalchemy.orm import Session
from ..models.aluno import Aluno
from typing import Optional, List # OK! Optional e List importados

class AlunoService:
    def __init__(self, db: Session):
        self.db = db

    def create_aluno(self, nome: str, matricula: str, email: str, curso: str = None) -> Aluno: # Adicione 'curso' aos parâmetros, pois o modelo tem
        """Cria um novo aluno."""
        # Passe 'curso' aqui também, se ele for NOT NULL no DB ou para preenchê-lo
        db_aluno = Aluno(nome=nome, matricula=matricula, email=email, curso=curso)
        self.db.add(db_aluno)
        self.db.commit()
        self.db.refresh(db_aluno)
        return db_aluno

    def get_aluno_by_matricula(self, matricula: str) -> Optional[Aluno]:
        """Busca um aluno pelo número de matrícula (PK)."""
        return self.db.query(Aluno).filter(Aluno.matricula == matricula).first()

    def get_aluno_by_email(self, email: str) -> Optional[Aluno]:
        """Busca um aluno pelo email."""
        return self.db.query(Aluno).filter(Aluno.email == email).first()

    def get_aluno_by_nome(self, nome: str) -> Optional[Aluno]:
        """Busca um aluno pelo nome."""
        return self.db.query(Aluno).filter(Aluno.nome == nome).first()

    def update_aluno(self, matricula_existente: str, new_nome: str = None, new_email: str = None, new_curso: str = None) -> Optional[Aluno]:
        """Atualiza as informações de um aluno existente pela matrícula."""
        db_aluno = self.get_aluno_by_matricula(matricula_existente) # Busca pela matrícula (CORRETO)
        if db_aluno:
            if new_nome is not None:
                db_aluno.nome = new_nome
            if new_email is not None:
                db_aluno.email = new_email
            if new_curso is not None: # Se 'curso' for um campo atualizável
                db_aluno.curso = new_curso
            # Não atualize a matrícula (PK) a menos que seja estritamente necessário e o DB permita.
            self.db.commit()
            self.db.refresh(db_aluno)
            return db_aluno
        return None

    def delete_aluno(self, matricula: str) -> bool: # Mude o parâmetro de 'aluno_id: int' para 'matricula: str'
        """Deleta um aluno pelo número de matrícula (PK)."""
        db_aluno = self.get_aluno_by_matricula(matricula) # Busca pela matrícula (CORRETO)
        if db_aluno:
            self.db.delete(db_aluno)
            self.db.commit()
            return True
        return False

    def get_all_alunos(self, skip: int = 0, limit: int = 100) -> List[Aluno]:
        """Lista todos os alunos."""
        return self.db.query(Aluno).offset(skip).limit(limit).all()