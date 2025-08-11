# ⛏️🤖 Minerador

Este diretório contém todo o código-fonte necessário para minerar dados de repositórios e pull requests usando a API GraphQL do GitHub.
Para executar este projeto, é necessário configurar alguns pré-requisitos:

## 📋 Pré-requisitos

* ### Infraestrutura

Este projeto foi desenvolvido na infraestrutura da AWS, utilizando principalmente os serviços ECS, ECR, DynamoDB e S3.
Portanto, certifique-se de executar o projeto de infraestrutura antes de prosseguir. Ele está localizado no diretório `./scripts/iac/aws`.

* ### SDK do Python

O código-fonte foi escrito utilizando a linguagem de programação Python. Recomendamos a utilizar a versão `3.12.7` do interpretador para a execução.
Caso ainda não tenha esta versão instalada, consulte
[esta documentação](https://www.python.org/downloads/release/python-3127/).

* ### Tokens Granulares do GitHub

Para utilizar a API GraphQL do GitHub, é necessário um token granular válido. 
O GitHub possuí um tutorial sobre como gerá-lo [aqui](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).
Após gerar o token, insira-o no arquivo `.env` localizado na raiz do diretório, na variável de ambiente `GITHUB_API_TOKEN`.
Nesse momento, a chave deverá estar no seguinte formato:

```dotenv
GITHUB_API_TOKEN=github_pat_11AFAG63Q0qL6...
```

Não se preocupe com o conteúdo já existente no arquivo `.env`.
Esse arquivo armazena o token do GitHub utilizado durante a execução da mineração original. Ele está em formato de hash
porque foi criptografado utilizando o [SOPS](https://github.com/getsops/sops).
Caso seja necessário, também é possível criptografar o token gerado. Certifique-se de editar o arquivo `.sops.yaml` com o ID da nova chave PGP antes de
executar qualquer comando do SOPS.

## ⚙️ Execução do Projeto

### Instalação de Dependências

Antes de executar o projeto, é necessário instalar todos os pacotes de dependências necessários.
Um arquivo `requirements.txt` foi disponibilizado na raiz do diretório contendo todos esses pacotes.
Para instalar todas as dependências, execute o seguinte comando na raiz do diretório:

```bash
pip3 install -r requirements.txt
```

### Execução do Minerador

Com todas as configurações prontas, é possível iniciar o programa minerador.
Para isso, execute os seguintes comandos na raiz do diretório:

```bash
cd src/
```

```bash
python3 run.py
```

Caso seja necessário executar este projeto em um ambiente conteinerizado, um `Dockerfile` foi disponibilizado na raiz do diretório.
Para construí-lo e executar o contêiner da aplicação, execute os seguintes comandos na raiz do diretório:

```bash
docker build . -t miner:latest
```

```bash
docker run miner:latest
```

> [!WARNING]
> Certifique-se de que o ambiente Docker esteja em execução antes de rodar o último comando.
> Você pode ver como configurar o Docker [aqui](https://docs.docker.com/engine/install/).
