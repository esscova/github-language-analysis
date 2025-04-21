# ---

import os
import time
import requests 
import logging

# --- configs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ---

class GithubAnalyzer:
    def __init__(self, github_token=None):
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        
        if github_token:
            self.headers['Authorization'] = f'token {github_token}'
        else:
            logging.warning("Aviso: Nenhum token do GitHub fornecido. Operando com limites de taxa anônimos.")

        self.base_url = 'https://api.github.com'

    def _make_request(self, url, params=None):
        try:
            logging.info(f"Fazendo requisição para a URL: {url}")
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            logging.info("Requisição bem-sucedida.")
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao fazer a requisição: {e}")
            return None
        
        except requests.exceptions.HTTPError as e:
            logging.error(f"Erro HTTP ao fazer a requisição: {e}")
            return None

        except ValueError as e:
            logging.error(f"Erro ao analisar a resposta JSON: {e}")
            return None

        except Exception as e:
            logging.error(f"Erro desconhecido ao fazer a requisição: {e}")
            return None

    def get_user_info(self, username):
        try:
            logging.info(f"Obtendo informações do usuário: {username}")
            url = f"{self.base_url}/users/{username}"
            logging.info(f"URL da requisição: {url}")
            return self._make_request(url)
        except Exception as e:
            logging.error(f"Erro ao obter informações do usuário: {username}. Erro: {e}")
            return None

    def get_user_repos(self, username):
        try:
            logging.info(f"Obtendo repositórios do usuário: {username}")
            url = f"{self.base_url}/users/{username}/repos"
            logging.info(f"URL da requisição: {url}")
            return self._make_request(url)
        except Exception as e:
            logging.error(f"Erro ao obter repositórios do usuário: {username}. Erro: {e}")
            return None
    
    def get_repo_info(self, username, repo_name):
        try:
            logging.info(f"Obtendo informações do repositório: {repo_name}")
            url = f"{self.base_url}/repos/{username}/{repo_name}"
            logging.info(f"URL da requisição: {url}")
            return self._make_request(url)
        except Exception as e:
            logging.error(f"Erro ao obter informações do repositório: {repo_name}. Erro: {e}")
            return None

    def get_repo_languages(self, username, repo_name):
        try:
            logging.info(f"Obtendo linguagens do repositório: {repo_name}")
            url = f"{self.base_url}/repos/{username}/{repo_name}/languages"
            logging.info(f"URL da requisição: {url}")
            return self._make_request(url)
        except Exception as e:
            logging.error(f"Erro ao obter linguagens do repositório: {repo_name}. Erro: {e}")
            return None
    
    def get_all_repos_languages(self, username):
        try:
            logging.info(f"Obtendo linguagens de todos os repositórios do usuário: {username}")
            url = f"{self.base_url}/users/{username}/repos"
            logging.info(f"URL da requisição: {url}")
            repos = self._make_request(url)
            languages = {}
            for repo in repos:
                repo_name = repo['name']
                languages[repo_name] = self.get_repo_languages(username, repo_name)
                time.sleep(1)
            return languages
        except Exception as e:
            logging.error(f"Erro ao obter linguagens de todos os repositórios do usuário: {username}. Erro: {e}")
            return None

# --- testes

if __name__ == "__main__":
    github_token = os.environ.get('GITHUB_TOKEN') 
    github_analyzer = GithubAnalyzer(github_token) 

    user_info = github_analyzer.get_user_info("esscova")
    user_repos = github_analyzer.get_user_repos("esscova")
    repo_info = github_analyzer.get_repo_info("esscova", "deepFIIs")
    repo_languages = github_analyzer.get_repo_languages("esscova", "deepFIIs")
    all_repos_languages = github_analyzer.get_all_repos_languages("esscova")

    if user_info:
        print("Informações do usuário:")
        print(user_info)

    if user_repos:
        print("Repositórios do usuário:")
        for repo in user_repos:
            print(repo['name'])

    if repo_info:
        print("Informações do repositório:")
        print(repo_info)

    if repo_languages:
        print("Linguagens do repositório:")
        print(repo_languages)

    if all_repos_languages:
        print("Linguagens de todos os repositórios do usuário:")
        print(all_repos_languages)