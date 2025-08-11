# Projeto de Infraestrutura - AWS

Para executar este projeto de infraestrutura, é necessário configurar o ambiente de execução. Para isso,
seguem abaixo guias de: instalação das linhas de comando da AWS e Terraform; um tutorial para configuração das credenciais
da AWS.

## Guias de Instalação

1. [Instalar o AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
2. [Instalar o Terraform CLI](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
3. [Configurar credenciais AWS](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

> [!WARNING]
> É indicado que o usuário já seja contextualizado com os serviços de computação em nuvem da AWS
> e possua experiência com ferramentas de infraestrutura IAC para prosseguir. Tópicos avançados
> sobre redes, configuração de recursos e encriptação de chaves serão abordados abaixo.

## Configuração das Variáveis de Ambiente em Nuvem

O arquivo `terraform.tfvars` contém todos os detalhes da configuração-base para os recursos em nuvem,
como a VPC, _subnets_ e identificadores AMI. Esse arquivo está encriptado com as chaves originais usadas
para a execução do projeto e devem ser substituídas pelas chaves pertencentes ao usuário. Para encontrar
quais variáveis precisam ser definidas, confira o arquivo `variables.tf` na raiz do projeto. Essas variáveis
possuem nomes intuítivos e similares aos recursos em nuvem que precisam ser configurados.

## Execução

Abaixo estão listados passo-a-passo todos os comandos necessários para executar o projeto de infraestrutura.

1. Inicialize o Terraform:

   ```bash
   terraform init
   ```

2. Visualize o plano de execução da infraestrutura:

   ```bash
   terraform plan
   ```
   
3. Aplique as configurações:

   ```bash
   terraform apply
   ```
   
4. **(Opcional)** Caso seja necessário, destrua a infraestrutura:

   ```bash
   terraform destroy
   ```
   
## Observação

Se você deseja encriptar o arquivo `terraform.tfvars` novamente, utilize o [SOPS](https://github.com/getsops/sops), ferramenta utilizada para a encriptação do arquivo inicialmente.
Garanta que o arquivo `.sops.yaml` está apontando para a nova chave PGP. 
