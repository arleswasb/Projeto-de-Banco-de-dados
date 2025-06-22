# TRABALHO3/services/aluno_service.py
from sqlalchemy.orm import Session
from ..models.aluno import Aluno # <--- MUITO IMPORTANTE: Verifique esta importação!

class AlunoService: 
    def __init__(self, db: Session):
        self.db = db

    def create_aluno(self, nome: str, matricula: str, email: str): # Adicione 'email' aqui se seu modelo Aluno o tem
        """Cria um novo aluno."""
        db_aluno = Aluno(nome=nome, matricula=matricula, email=email) # Inclua email
        self.db.add(db_aluno)
        self.db.commit()
        self.db.refresh(db_aluno)
        return db_aluno
    
    def get_aluno_by_matricula(self, matricula: str):
        """Busca um aluno pelo número de matrícula."""
        return self.db.query(Aluno).filter(Aluno.matricula == matricula).first()
    
    def get_aluno_by_email(self, email: str):
        """Busca um aluno pelo email."""
        return self.db.query(Aluno).filter(Aluno.email == email).first()  
      
    def get_aluno_by_nome(self, nome: str):
        """Busca um aluno pelo nome."""
        return self.db.query(Aluno).filter(Aluno.nome == nome).first()

    def update_aluno(self, matricula_existente: str, new_nome: str = None, new_email: str = None, new_curso: str = None) -> Optional[Aluno]:
        """Atualiza as informações de um aluno existente pela matrícula.""" # <--- ESTA LINHA COMEÇA COM ESPAÇOS/TAB
        db_aluno = self.get_aluno_by_matricula(matricula_existente) # <--- E ESTA TAMBÉM
        if db_aluno: # <--- E ESTA TAMBÉM
            if new_nome is not None:
                db_aluno.nome = new_nome
            if new_email is not None:
                db_aluno.email = new_email
            if new_curso is not None:
                db_aluno.curso = new_curso
            self.db.commit()
            self.db.refresh(db_aluno)
            return db_aluno
        return None
    
    def delete_aluno(self, aluno_id: int):
        """Deleta um aluno pelo ID."""
        db_aluno = self.get_aluno_by_id(aluno_id)
        if db_aluno:
            self.db.delete(db_aluno)
            self.db.commit()
            return True
        return False
    
    def get_all_alunos(self, skip: int = 0, limit: int = 100):
        """Lista todos os alunos."""
        return self.db.query(Aluno).offset(skip).limit(limit).all()
    