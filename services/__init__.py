# services/__init__.py

# Usando imports relativos (com '.') para importar de dentro do mesmo pacote.
from .aluno_service import AlunoService
from .livro_service import LivroService
from .exemplar_service import ExemplarService
from .emprestimo_service import EmprestimoService
from .emprestimo_exemplar_service import EmprestimoExemplarService