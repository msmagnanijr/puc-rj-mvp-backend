Este é um projeto Python que usa Flask e PostgreSQL para criar uma API para gerenciar matérias. A API permite criar, atualizar, remover e listar matérias. Além disso, a API inclui documentação interativa gerada pelo Swagger.
A aplicação usa o módulo psycopg2 para se comunicar com o banco de dados.

## Pré-requisitos

Para executar este projeto, você precisa ter o Python 3.7 ou superior instalado, além de uma instância do PostgreSQL em execução.

## Como usar

1. Para instalar as dependências, execute o seguinte comando:

```
pip install -r requirements.txt
```

2. Crie um banco de dados PostgreSQL e Inicie a aplicação:

```
python app.py
```

Agora você pode acessar a documentação da API em http://localhost:5000/apidocs/

## Ponto de Atenção

Esse código é uma configuração básica para acessar um banco de dados PostgreSQL. Ele define os parâmetros de conexão com o banco de dados, incluindo o nome do host, porta, nome do banco de dados, nome de usuário e senha.

No entanto, é importante destacar que a senha do banco de dados deve ser armazenada com segurança, de preferência em um arquivo separado ou variável de ambiente, e não diretamente no código-fonte, como é o caso aqui.

```
self.connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="postgres",
    password="senha"
)
```
