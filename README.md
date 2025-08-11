# Gerenciamento Automatizado de Dependências: Um Estudo em Larga Escala sobre a Adoção do Dependabot

Este repositório contém o pacote de replicação para o _paper_ submetido ao _13th Workshop on Software Visualization, Evolution and Maintenance_, da CBSoft 2025.

## Diretórios

Todos os diretórios do projeto possuem um arquivo `README.md` com informações sobre o conteúdo e a finalidade de cada um deles. 
Abaixo, uma breve descrição dos principais diretórios:

### Diretórios de conjunto de dados

* `./dataset`: Contém os conjuntos de dados utilizados neste estudo, organizados em duas categorias: `raw` (dados brutos) e `processed` (dados processados).

### Diretórios de código-fonte

* `./notebooks`: Contém o _notebook_ Jupyter utilizado para o cálculo de métricas.
* `./scripts`: Diretório que contém o código-fonte utilizado para a mineração e processamento dos dados, bem como utilitários para análise do _dataset_.

## Conjunto de dados

### Arquivos

Este repositório contém um conjunto de dados minerados de _pull requests_ (PRs) e repositórios populares do GitHub. Os arquivos estão organizados nas pastas `dataset/raw` e `dataset/processed`. Abaixo está uma descrição de cada um deles:

#### `dataset/raw`

Os arquivos contidos neste diretório são utilizados para alimentar as entradas de dados dos _notebooks_ [Jupyter](https://jupyter.org/) relacionados ao cálculo das métricas deste estudo.

- **prs.csv**: Este arquivo contém as informações de todas as PRs extraídas, incluindo aquelas criadas por Dependabot e outros contribuintes. Cada linha representa um _pull request_.
- **repositories.csv**: Este arquivo contém todas as informações dos repositórios de onde os PRs utilizados neste estudo foram extraídos. Cada linha corresponde a um repositório e inclui informações relevantes como nome, descrição e identificador único. 
Ademais, o arquivo também apresenta o campo booleano `HasDependabotPRs`, cujo valor é `1` para aqueles repositórios que apresentam pelo menos 1 PR do Dependabot, e `0` para os que não apresentam nenhuma.

#### `dataset/processed`

Os arquivos contidos neste diretório correspondem a dados processados a partir das entradas brutas e incluem saídas do cálculo de métricas e outras informações auxiliares relevantes para a caracterização do _dataset_ e validação de resultados.

- **output/*.csv**: Neste diretório estão contidos os resultados das manipulações de dados realizadas no _notebook_ `./notebooks/metrics_calculation.ipynb`. São utilizados para o cálculo das RQs deste estudo.
- **stats.csv**: Este arquivo oferece informações gerais calculadas sobre o conjunto de dados, conforme descritas na seção seguinte deste documento.
- **unique_repo_ids.csv**: Este arquivo contém apenas os identificadores únicos dos repositórios a partir dos quais as PRs foram extraídas. É útil para identificar e mapear os repositórios sem incluir informações adicionais.
- **dependabot_prs/*.csv**: Neste diretório estão contidos, de forma particionada, apenas as PRs de autoria do Dependabot mineradas para este estudo.

### Descrição do _dataset_

Abaixo se encontram características gerais do _dataset_ utilizado neste experimento, considerando os _pull requests_ e os repositórios minerados. O conjunto original de dados se encontra no diretório `./dataset/raw`.

#### Informações dos repositórios

- Nº total de repositórios minerados: `500`
- Nº de repositórios com pelo menos 1 PR do Dependabot: `232`

#### Informações dos _Pull Requests_

| Métrica | Valor |
| --- | --- |
| Nº total de PRs minerados | `909,879` |
| Nº de PRs do Dependabot encontradas | `40,292` |
| Média de PRs por repositório | `181.76` |
| Média de PRs do Dependabot por repositório | `80.58` |
| Proporção de PRs do Dependabot em relação ao total | `4.43%` |
| Total de PRs aceitos (`MERGED`) | `23,980` |
| Total de PRs rejeitados (`CLOSED`) | `15,512` |
| Total de PRs em aberto (`OPEN`) | `800` |
| Total de PRs analisados (`MERGED`) | `40,292` |
| Porcentagem de PRs aceitos | `59.52%` |
| Porcentagem de PRs rejeitados | `38.50%` |
| Porcentagem de PRs em aberto | `1.99%` |
| Maior taxa de aceitação por projeto | `100.0%` |
| Menor taxa de aceitação por projeto | `0.0%` |
| Mediana da taxa de aceitação por projeto | `58.43%` |
| Projeto com o PR que levou mais tempo para ser aceito | `prettier` — aceito após `12 meses` |
| Projeto com o PR que levou menos tempo para ser aceito | `tldraw` — aceito após `7 segundos` |
| Tempo médio para fechar um PR | `9 dias` |

#### Top 3 linguagens com mais PRs do Dependabot
1. **TypeScript**: `15660` PRs (`38.87%`)
2. **JavaScript**: `6926` PRs (`17.19%`)
3. **Go**: `4780` PRs (`11.86%`)

#### Linguagem com menor número de PRs do Dependabot

- **VueScript**: `5` PRs (`0.01%`)

#### Linguagem principal utilizada nos repositórios

| Linguagem | Nº de repositórios |
| --- | --- |
| Python | `90` |
| JavaScript | `78` |
| TypeScript | `69` |
| Go | `32` |
| Java | `28` |
| Rust | `23` |
| C++ | `15` |
| HTML | `13` |
| Shell | `11` |
| Jupyter Notebook | `10` |
| C | `9` |

> **Total de PRs em linguagens não populares (excluindo 'Desconhecida')**: `4208` PRs (`10.45%`)

## Instruções de replicação

É necessário utilizar um sistema operacional baseado em Linux ou macOS para reproduzir os passos a seguir. Para garantir o funcionamento pleno,
a execução de cada subseção abaixo deve ser iniciada a partir da raiz deste repositório.

### Configurando o ambiente Python

1. Crie um ambiente virtual:

    ```bash
    python3 -m venv .venv
    ```

2. Ative o ambiente virtual:

    ```bash
    source .venv/bin/activate
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

### Obter informações gerais do _dataset_

1. Navegue até o diretório de utilitários:

    ```bash
    cd scripts/utils/
    ```

2. Execute o _script_ utilitário:

    ```bash
    python stats.py
    ```

### Calcular métricas e gerar gráficos

Para executar os _notebooks_ Jupyter, disponíveis no diretório `./notebooks`, siga estes passos:

1. Certifique-se de ter todas as bibliotecas necessárias instaladas, conforme instruído na subseção "Configurando o ambiente Python".

2. No diretório raiz do projeto, execute o comando:

    ```bash
    jupyter notebook
    ```

3. Neste ponto, a interface visual já deve estar a ser visualizada. Navegue até o diretório `./notebooks` e abra o arquivo `metrics_calculation.ipynb` na interface visual do Jupyter.

4. Execute as células no _notebook_ para gerar os resultados.
