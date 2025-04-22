# ---

import os
import time
import requests
import logging
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime

# --- 

matplotlib.use('Agg')  #! backend Agg para evitar erros de interface gráfica
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ---
class GithubAnalyzer:
    def __init__(self, github_token=None):
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        if github_token:
            self.headers['Authorization'] = f'token {github_token}'
        else:
            logging.warning("Nenhum token do GitHub fornecido. Operando com limites de taxa anônimos.")
        self.base_url = 'https://api.github.com'

    def _make_request(self, url, params=None):
        """Faz uma requisição à API do GitHub com tratamento de erros e limites de taxa."""
        for attempt in range(3):  # até 3 vezes em caso de falha
            try:
                logging.info(f"Fazendo requisição para: {url}")
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()

                # verificar e aguardar se houver limites de taxa
                remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
                reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                
                if remaining < 50:  #! ajustado para 50 para mais margem
                    sleep_time = max(reset_time - time.time(), 0) + 1
                    logging.warning(f"Limite de taxa baixo ({remaining}). Aguardando {sleep_time:.1f}s.")
                    time.sleep(sleep_time)

                logging.info("Requisição bem-sucedida.")
                return response.json()
            except requests.exceptions.RequestException as e:
                logging.error(f"Erro na requisição (tentativa {attempt+1}/3): {e}")
                time.sleep(2 ** attempt)  #! pausa com tempo exponencial .. 2⁰ = 1 seg, 2¹ = 2 seg...
        logging.error("Falha após 3 tentativas.")
        return None

    def get_user_repos(self, username, per_page=100):
        """Obtém todos os repositórios de uma organização, lidando com paginação."""
        repos = []
        page = 1
        while True:
            url = f"{self.base_url}/orgs/{username}/repos"
            params = {'per_page': per_page, 'page': page, 'sort': 'created', 'direction': 'asc'}
            data = self._make_request(url, params)
            if not data:
                break
            # filtrar repositórios não arquivados e não forks
            filtered_repos = [repo for repo in data if not repo.get('archived') and not repo.get('fork')]
            repos.extend(filtered_repos)
            if len(data) < per_page:
                break
            page += 1
            time.sleep(0.5)  # evitar atingir limite de taxa
        return repos

    def get_repo_languages(self, username, repo_name):
        """Obtém as linguagens usadas em um repositório."""
        url = f"{self.base_url}/repos/{username}/{repo_name}/languages"
        return self._make_request(url)

    def collect_languages_by_year(self, organizations):
        """Coletar linguagens de programação por ano para uma lista de organizações."""
        languages_by_year = []
        # carregar dados csv caso exista
        try:
            existing_df = pd.read_csv('languages_by_year.csv')
            languages_by_year = existing_df.to_dict('records')
            logging.info("Carregado dados existentes do CSV.")
        except FileNotFoundError:
            logging.info("Nenhum CSV existente encontrado. Iniciando do zero.")

        for org in organizations:
            if any(d['Organization'] == org for d in languages_by_year): # ja existe?
                logging.info(f"Organização {org} já processada. Pulando.")
                continue
            logging.info(f"Analisando organização: {org}")
            repos = self.get_user_repos(org)
            if not repos:
                logging.warning(f"Nenhum repositório encontrado para {org}")
                continue

            for repo in repos:
                repo_name = repo['name']
                created_at = repo.get('created_at', '')
                if not created_at:
                    continue
                year = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ').year
                
                languages = self.get_repo_languages(org, repo_name)
                if languages:
                    for lang, bytes_count in languages.items():
                        languages_by_year.append({
                            'Organization': org,
                            'Year': year,
                            'Language': lang,
                            'Bytes': bytes_count
                        })
                time.sleep(0.5)  # pausa entre requisições

        return languages_by_year

    def save_to_csv(self, languages_by_year, filename='languages_by_year.csv'):
        """Salva os dados de linguagens por ano em um arquivo CSV."""
        df = pd.DataFrame(languages_by_year)
        df.to_csv(filename, index=False)
        logging.info(f"Dados salvos em {filename}")

    def plot_languages_by_year(self, languages_by_year, top_n=5):
        """Gera gráficos de barras empilhadas: um agregado e um por organização."""
        df = pd.DataFrame(languages_by_year)

        # gráfico agregado (todas as organizações)
        top_languages = df.groupby('Language')['Bytes'].sum().nlargest(top_n).index
        agg_df = df[df['Language'].isin(top_languages)]
        pivot_df = agg_df.pivot_table(index='Year', columns='Language', values='Bytes', aggfunc='sum').fillna(0)
        
        plt.figure(figsize=(12, 8))
        pivot_df.plot(kind='bar', stacked=True, ax=plt.gca())
        plt.title('Linguagens Mais Usadas por Ano (Todas as Organizações)')
        plt.xlabel('Ano')
        plt.ylabel('Bytes de Código')
        plt.legend(title='Linguagem')
        plt.tight_layout()
        plt.savefig('languages_by_year_all.png')
        logging.info("Gráfico salvo em 'languages_by_year_all.png'")
        plt.close()

        # gráficos por organização (um por empresa)
        for org in df['Organization'].unique():
            org_df = df[df['Organization'] == org]
            top_languages = org_df.groupby('Language')['Bytes'].sum().nlargest(top_n).index
            org_df = org_df[org_df['Language'].isin(top_languages)]
            
            pivot_df = org_df.pivot_table(index='Year', columns='Language', values='Bytes', aggfunc='sum').fillna(0)
            
            plt.figure(figsize=(12, 8))
            pivot_df.plot(kind='bar', stacked=True, ax=plt.gca())
            plt.title(f'Linguagens Mais Usadas por Ano - {org}')
            plt.xlabel('Ano')
            plt.ylabel('Bytes de Código')
            plt.legend(title='Linguagem')
            plt.tight_layout()
            plt.savefig(f'languages_by_year_{org}.png')
            logging.info(f"Gráfico salvo em 'languages_by_year_{org}.png'")
            plt.close()

# --- testes
if __name__ == "__main__":
    github_token = os.environ.get('GITHUB_TOKEN')
    analyzer = GithubAnalyzer(github_token)

    # empresas
    organizations = ['microsoft','APPLE','nvidia','facebook','amzn','netflix','google','uber']

    # coletar
    languages_by_year = analyzer.collect_languages_by_year(organizations)

    # persistir
    analyzer.save_to_csv(languages_by_year)

    # visualizar
    analyzer.plot_languages_by_year(languages_by_year, top_n=5)