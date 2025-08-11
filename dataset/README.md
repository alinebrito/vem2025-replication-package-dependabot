# Datasets

Este diretório é responsável por armazenar os _datasets_ produzidos e categorizados a partir da mineração e processamento dos dados obtidos.
Os _datasets_ são compostos por arquivos no formato CSV, que contêm informações sobre os repositórios e seus _pull requests_ no GitHub, incluindo detalhes com: Título, descrição, linguagem de programação, número de estrelas, entre outros.

---

* `/raw`: Diretório contendo os _datasets_ brutos, que são o resultado da mineração de dados realizada por meio da API GraphQL do GitHub.
* `/processed`: Diretório contendo os _datasets_ processados, que são o resultado do processamento dos dados obtidos através da execução dos _notebooks_ Jupyter,
disponíveis no diretório `./notebooks`.
