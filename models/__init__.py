print("DEBUG: Entrando em models/__init__.py")

print("DEBUG: Importando Aluno...")
from .aluno import Aluno
print("DEBUG: OK - Aluno importado.")

print("DEBUG: Importando Livro...")
from .livro import Livro
print("DEBUG: OK - Livro importado.")

print("DEBUG: Importando Exemplar...")
from .exemplar import Exemplar
print("DEBUG: OK - Exemplar importado.")

print("DEBUG: Importando Emprestimo...")
from .emprestimo import Emprestimo
print("DEBUG: OK - Emprestimo importado.")

print("DEBUG: Importando EmprestimoExemplar...")
from .emprestimo_exemplar import EmprestimoExemplar
print("DEBUG: OK - EmprestimoExemplar importado.")

print("DEBUG: Saindo de models/__init__.py")