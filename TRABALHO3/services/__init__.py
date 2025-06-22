# trabalho3/services/__init__.py
from .aluno_service import AlunoService
from .livro_service import LivroService
from .exemplar_service import ExemplarService
from .emprestimo_service import EmprestimoService
# Você não precisa de um serviço específico para emprestimo_exemplar,
# pois as operações serão feitas através dos serviços de Emprestimo ou Exemplar.