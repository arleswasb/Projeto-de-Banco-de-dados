# Projeto-de-Banco-de-dados
projeto de elaboração de banco de dados relacional para disciplina da ufrn

PROJETO DE BANCO DE DADOS - SISTEMA DE BIBLIOTECA
=================================================

Este projeto consiste em uma aplicação em Python que utiliza o ORM SQLAlchemy para interagir com um banco de dados PostgreSQL. A aplicação implementa uma camada de serviços para realizar operações CRUD (Create, Read, Update, Delete) em um modelo de dados de uma biblioteca, incluindo entidades como Aluno, Livro, Exemplar e Empréstimo.


TECNOLOGIAS UTILIZADAS
----------------------

* Linguagem: Python 3.11
* Banco de Dados: PostgreSQL 16
* ORM: SQLAlchemy 2.0
* Gerenciamento de Ambiente: Docker e Docker Compose
* Testes Automatizados: Pytest
* CI/CD: GitHub Actions


ESTRUTURA DO PROJETO
--------------------

O projeto segue uma arquitetura de camadas para separar as responsabilidades, conforme especificado nos requisitos da disciplina:

.
├── .github/workflows/      # Contém o pipeline de CI/CD
├── models/                 # Mapeamentos ORM (SQLAlchemy) das tabelas
├── services/               # Classes com a lógica de negócio (operações CRUD)
├── tests/                  # Testes automatizados com Pytest
├── .env                    # Arquivo de configuração de ambiente (NÃO deve ir para o Git)
├── .gitignore              # Arquivos e pastas ignorados pelo Git
├── db.py                   # Configuração da conexão com o banco de dados
├── docker-compose.yml      # Arquivo para orquestrar o container do banco de dados local
├── main.py                 # Script principal para demonstração manual das operações
└── requirements.txt        # Lista de dependências Python do projeto


PRÉ-REQUISITOS
--------------

Antes de começar, garanta que você tenha os seguintes softwares instalados na sua máquina:

* Git (https://git-scm.com/)
* Python 3.11+ (https://www.python.org/)
* Docker Desktop (https://www.docker.com/products/docker-desktop/) (que inclui o Docker Compose)


CONFIGURAÇÃO E SETUP DO AMBIENTE LOCAL
---------------------------------------

Siga estes passos para configurar o projeto na sua máquina.

1. Clonar o Repositório
   git clone <URL_DO_SEU_REPOSITORIO_AQUI>
   cd Projeto-de-Banco-de-dados

2. Criar o Arquivo de Ambiente (.env)
   Este arquivo guarda as credenciais do banco de dados para o ambiente local. Crie um arquivo chamado .env na raiz do projeto e copie o conteúdo abaixo para ele, substituindo a senha se necessário.

   # .env - Arquivo de configuração para ambiente local

   # Usado pelo docker-compose.yml para criar o container do banco
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=sua_senha_segura
   POSTGRES_DB=biblioteca_db

   # Usado pelo db.py para se conectar ao banco de dados
   DATABASE_URL="postgresql://postgres:sua_senha_segura@localhost:5432/biblioteca_db"

3. Criar e Ativar o Ambiente Virtual
   É uma boa prática isolar as dependências do projeto.

   # Criar o ambiente virtual
   python -m venv .venv

   # Ativar no Windows (PowerShell)
   . .\.venv\Scripts\Activate.ps1

   # Ativar no Linux ou macOS
   source .venv/bin/activate

4. Instalar as Dependências
   Com o ambiente virtual ativo, instale todas as bibliotecas necessárias.

   pip install -r requirements.txt


EXECUTANDO O PROJETO
--------------------

Com o ambiente configurado, você pode rodar a aplicação de duas formas:

1. Demonstração Manual (Conforme o Roteiro do Trabalho)

   Esta opção utiliza o main.py para executar um script que demonstra as operações CRUD.

   Passo 1: Iniciar o Banco de Dados com Docker
   Este comando irá iniciar um container PostgreSQL em segundo plano.

   docker-compose up -d

   *Aguarde alguns segundos para que o serviço do banco de dados esteja completamente pronto.*

   Passo 2: Executar o Script de Demonstração
   Este script irá limpar as tabelas e executar uma série de operações para demonstrar a funcionalidade.

   python main.py

   Passo 3: Parar o Banco de Dados
   Quando terminar, você pode parar o container do PostgreSQL com o comando:

   docker-compose down


2. Executando os Testes Automatizados

   O projeto possui uma suíte de testes completa que valida cada serviço individualmente.

   Passo 1: Iniciar o Banco de Dados
   Assim como na demonstração manual, o banco de dados precisa estar rodando.

   docker-compose up -d

   Passo 2: Rodar os Testes com Pytest
   Com o ambiente virtual ativo, execute:

   pytest --verbose

   *Este comando irá encontrar e executar todos os testes na pasta tests/.*


PIPELINE DE CI/CD (GITHUB ACTIONS)
---------------------------------

Este repositório está configurado com um pipeline de Integração Contínua (CI) usando GitHub Actions. A cada push ou pull request para as branches main e develop, o pipeline é acionado automaticamente para:
1. Executar o Linter (pylint): Para garantir a qualidade e o padrão do código.
2. Executar os Testes Automatizados (pytest): Para garantir que todas as funcionalidades continuam funcionando como esperado. Os testes rodam contra um banco de dados PostgreSQL temporário, criado exclusivamente para o pipeline.

Isso garante a integridade e a qualidade contínua do projeto.
