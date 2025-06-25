# services/__init__.py
# VERSÃO FINAL CORRIGIDA

"""
Este arquivo transforma o diretório 'services' em um pacote Python
e facilita a importação das classes de serviço.
Ex: from services import AlunoService, LivroService, etc.
"""

# Usando imports relativos (com '.') para importar de dentro do mesmo pacote.
from .aluno_service import AlunoService
from .livro_service import LivroService
from .exemplar_service import ExemplarService
from .emprestimo_service import EmprestimoService
from .emprestimo_exemplar_service import EmprestimoExemplarService