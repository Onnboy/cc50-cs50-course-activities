C$50 Finance

Este projeto é uma aplicação web que simula um mercado de ações, permitindo que os usuários comprem e vendam ações, acompanhem seu histórico de transações e gerenciem seu saldo em conta.

Funcionalidades

Registro e login: Usuários podem criar contas e fazer login.

Consulta de ações: Permite pesquisar preços de ações em tempo real.

Compra e venda de ações: Gerenciamento de ações no portfólio.

Histórico de transações: Exibe um histórico de todas as compras e vendas de ações.

Gerenciamento de saldo: Usuários podem adicionar dinheiro à conta.

Alteração de senha: Permite aos usuários redefinir suas senhas com critérios de segurança.

Tecnologias utilizadas

Flask: Framework web principal.

SQLite: Banco de dados para armazenamento de usuários, transações e portfólio.

Werkzeug: Utilizado para hashing de senhas.

Bootstrap: Para estilização e responsividade.

Estrutura do Projeto:

finance/
│──flask_session          # Guardar usuario após registro
│── static/               # Arquivos CSS, imagens
│── templates/            # Templates HTML
│── app.py                # Código principal da aplicação
│── finance.db            # Banco de dados SQLite
│── helpers.py            # Funções auxiliares
│── requirements.txt      # Dependências do projeto

Como executar

Clone o repositório:

git clone https://github.com/Onnboy/cc50-cs50-course-activities # Já que o diretorio/pasta(FINANCE) já está mesclada 
cd finance

Crie um ambiente virtual e instale as dependências:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Execute a aplicação:

pip install -r requirements.txt # Baixar dependencias

flask run

Acesse http://127.0.0.1:5000/ no navegador.

Critérios de Segurança para Senhas

Mínimo de 8 caracteres.

Pelo menos 1 número.

Pelo menos 1 símbolo especial.

Se uma senha não atender a esses critérios, o usuário receberá uma mensagem de erro ao tentar registrar ou alterar a senha.

Autor

Projeto desenvolvido como parte do curso CS50’s Introduction to Computer Science.

