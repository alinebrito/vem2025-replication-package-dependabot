import pandas as pd
import os

df_prs = pd.read_csv('../../dataset/raw/prs.csv', header=0)
df_repos = pd.read_csv('../../dataset/raw/repositories.csv', header=0)

# IDs únicos de repositórios presentes no dataset de PRs
unique_repo_ids = df_prs['RepositoryId'].unique()

# Cálculo de repositórios com pelo menos 1 PR do Dependabot
repos_com_dependabot = df_prs[df_prs['Author'] == 'dependabot']['RepositoryId'].nunique()

# Dados gerais de PRs
total_prs = len(df_prs)
total_repos = len(unique_repo_ids)
total_dependabot_prs = (df_prs['Author'] == 'dependabot').sum()

# Métricas médias por repositório
media_prs_por_repo = total_prs / total_repos
media_dependabot_por_repo = total_dependabot_prs / total_repos
proporcao_dependabot = total_dependabot_prs / total_prs

# Número de repositórios por linguagem principal
repos_por_linguagem = df_prs.groupby('PrimaryLanguage')['RepositoryId'].nunique().sort_values(ascending=False).to_dict()

print("========== Dados de Repositórios ==========")
print(f"Nº total de repositórios minerados: {total_repos}")
print(f"Nº de repositórios com pelo menos 1 PR do Dependabot: {repos_com_dependabot}")

print("\n========== Dados de Pull Requests ==========")
print(f"Nº total de PRs mineradas: {total_prs}")
print(f"Nº de PRs do Dependabot encontradas: {total_dependabot_prs}")
print(f"Média de PRs por repositório: {media_prs_por_repo:.2f}")
print(f"Média de PRs do Dependabot por repositório: {media_dependabot_por_repo:.2f}")
print(f"Proporção de PRs do Dependabot em relação ao total: {proporcao_dependabot * 100:.2f}%")

print("\n========== Repositórios por Linguagem Principal ==========")
for linguagem, count in repos_por_linguagem.items():
    print(f"{linguagem}: {count} repositório(s)")

# Exportar dados
stats_data = {
    'total_repositories': [total_repos],
    'repositories_with_dependabot_pr': [repos_com_dependabot],
    'total_prs': [total_prs],
    'total_dependabot_prs': [total_dependabot_prs],
    'mean_prs_per_repository': [media_prs_por_repo],
    'mean_dependabot_prs_per_repository': [media_dependabot_por_repo],
    'dependabot_prs_ratio': [proporcao_dependabot],
}

for linguagem, count in repos_por_linguagem.items():
    stats_data[f'repositories_{linguagem}'] = [count]

stats_df = pd.DataFrame(stats_data)

stats_df.to_csv('../../dataset/processed/stats.csv', index=False)