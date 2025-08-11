# ⚙️ Processador

Este diretório contém todo o código-fonte necessário para gerar e processar o _dump_ de dados.
Para executar este projeto, é necessário configurar alguns pré-requisitos:

## 📋 Pré-requisitos

* ### Infraestrutura

Este projeto foi desenvolvido na infraestrutura da AWS, utilizando principalmente os serviços ECS, ECR, DynamoDB e S3.
Portanto, certifique-se de executar o projeto de infraestrutura antes de prosseguir. Ele está localizado no diretório `./scripts/iac/aws`.

Ademais, também foi utilizado um recurso da provedora de computação em nuvem Google Cloud Platform. Essa configuração é mais
simplista e será abordada abaixo.

* ### SDK do Python

O código-fonte foi escrito utilizando a linguagem de programação Python. Recomendamos a utilizar a versão `3.12.7` do interpretador para a execução.
Caso ainda não tenha esta versão instalada, consulte
[esta documentação](https://www.python.org/downloads/release/python-3127/).

* ### Credenciais da Google Cloud Platform

Utilizamos o serviço do Google Spreadsheets para salvar os resultados das métricas e garantir alta disponibilidade.
Este serviço é fornecido pela [GCP](https://cloud.google.com/?hl=pt-BR) e é necessário configurar suas próprias credenciais.
Siga [este tutorial](https://developers.google.com/workspace/guides/create-credentials) para gerar um arquivo de credenciais `gcp-credentials.json`
e substitua o que está atualmente na raiz do diretório.

Esse arquivo armazena as credenciais utilizadas durante o processamento e _upload_ de métricas no Google Spreadsheets. Ele está em formato de hash
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

### Execução do Processador

Com todas as configurações prontas, é possível iniciar o programa processador.
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
docker build . -t processor:latest
```

```bash
docker run processor:latest
```

> [!WARNING]
> Certifique-se de que o ambiente Docker esteja em execução antes de rodar o último comando.
> Você pode ver como configurar o Docker [aqui](https://docs.docker.com/engine/install/).