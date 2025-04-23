
# Documentação do Script: Github_Analyzer.py

**Versão:** 1.0

**Data:** 2025-04-23

**Autor Original:** [Wellington M Santos](https://www.linkedin.com/in/wellington-moreira-santos/)

## 1. Visão Geral

Este script Python coleta dados sobre as linguagens de programação utilizadas nos repositórios públicos de organizações específicas no GitHub. Ele interage com a API v3 do GitHub para buscar repositórios, extrair informações sobre as linguagens (em bytes de código) e agregar esses dados pelo ano de criação de cada repositório.

O objetivo principal é entender quais linguagens são predominantes em diferentes organizações (como Big Techs) ao longo do tempo, com base na data de criação dos seus repositórios públicos.

O script gera:
1.  Um arquivo CSV (`languages_by_year.csv`) contendo os dados brutos coletados.
2.  Gráficos em formato PNG mostrando as linguagens mais usadas por ano (um agregado e um por organização).

## 2. Pré-requisitos

*   **Python:** Versão 3.6 ou superior.
*   **Bibliotecas Python:**
    *   `requests`: Para fazer chamadas HTTP à API do GitHub.
    *   `pandas`: Para manipulação e armazenamento dos dados em formato tabular (DataFrame) e para salvar em CSV.
    *   `matplotlib`: Para a geração dos gráficos.
*   **Token de Acesso Pessoal do GitHub (Opcional, mas Altamente Recomendado):**
    *   A API do GitHub possui limites de taxa mais restritivos para requisições anônimas. Para analisar múltiplas organizações e repositórios, é essencial gerar um [Token de Acesso Pessoal](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) no GitHub (com escopo `public_repo` é suficiente) e configurá-lo como uma variável de ambiente.

## 3. Instalação de Dependências

```bash
pip install requests pandas matplotlib
```

## 4. Configuração

*   **Token do GitHub:** Defina a variável de ambiente `GITHUB_TOKEN` com o seu Token de Acesso Pessoal.
    *   No Linux/macOS: `export GITHUB_TOKEN='seu_token_aqui'`
    *   No Windows (PowerShell): `$env:GITHUB_TOKEN='seu_token_aqui'`
    *   No Windows (CMD): `set GITHUB_TOKEN=seu_token_aqui`
    *   Alternativamente, você pode modificar o script para ler o token de um arquivo de configuração ou de outra forma segura.
*   **Lista de Organizações:** Modifique a lista `organizations` dentro do bloco `if __name__ == "__main__":` no final do script para incluir os nomes de usuário/organização do GitHub que você deseja analisar. Certifique-se de que os nomes estão corretos (ex: `facebook` agora é `meta`).

## 5. Como Usar

1.  Certifique-se de que todos os pré-requisitos e dependências estão instalados.
2.  Configure a variável de ambiente `GITHUB_TOKEN` (recomendado).
3.  Ajuste a lista `organizations` no script, se necessário.
4.  Execute o script a partir do terminal:
    ```bash
    python nome_do_seu_script.py
    ```
5.  O script começará a coletar dados, exibindo logs no console. Ele pode levar um tempo considerável dependendo do número de organizações e repositórios.
6.  Após a conclusão, verifique os arquivos gerados no mesmo diretório:
    *   `languages_by_year.csv`: Contém os dados coletados.
    *   `languages_by_year_all.png`: Gráfico agregado das linguagens mais usadas por ano.
    *   `languages_by_year_<org>.png`: Gráficos individuais para cada organização analisada.

## 6. Estrutura do Código

O script é organizado principalmente em torno da classe `GithubAnalyzer`.

### 6.1. Imports e Configuração Inicial

*   Importa as bibliotecas necessárias (`os`, `time`, `requests`, `logging`, `pandas`, `matplotlib`, `datetime`).
*   Configura o backend do `matplotlib` para `Agg` para evitar problemas em ambientes sem GUI.
*   Configura o `logging` básico para exibir informações e erros durante a execução.

### 6.2. Classe `GithubAnalyzer`

Encapsula toda a lógica de interação com a API do GitHub e processamento dos dados.

*   **`__init__(self, github_token=None)`**:
    *   Inicializa a classe.
    *   Define os headers padrão para as requisições da API.
    *   Adiciona o header `Authorization` se um `github_token` for fornecido. Emite um aviso se nenhum token for passado.
    *   Define a URL base da API do GitHub.

*   **`_make_request(self, url, params=None)`**:
    *   Método auxiliar privado para realizar requisições GET à API do GitHub.
    *   **Tratamento de Erros:** Usa `try...except` para capturar erros de requisição (`requests.exceptions.RequestException`) e `response.raise_for_status()` para erros HTTP (4xx, 5xx).
    *   **Retentativas:** Tenta fazer a requisição até 3 vezes em caso de falha, com um tempo de espera exponencial (`backoff`) entre as tentativas (1s, 2s, 4s).
    *   **Gerenciamento de Rate Limit:** Verifica os headers `X-RateLimit-Remaining` e `X-RateLimit-Reset`. Se o limite restante estiver baixo (abaixo de 50), calcula o tempo necessário para aguardar até a janela de limite ser resetada e pausa a execução (`time.sleep`).
    *   Retorna o corpo da resposta em formato JSON em caso de sucesso, ou `None` após falhas consecutivas.

*   **`get_user_repos(self, username, per_page=100)`**:
    *   Busca todos os repositórios de uma determinada organização (`username`).
    *   **Paginação:** Lida automaticamente com a paginação da API, buscando repositórios em lotes (`per_page`) até que todos sejam recuperados.
    *   **Filtragem:** Inclui apenas repositórios que **não** estão arquivados (`archived: false`) e que **não** são forks (`fork: false`).
    *   **Pausa:** Inclui uma pequena pausa (`time.sleep(0.5)`) entre as requisições de página para evitar limites de taxa secundários.
    *   Retorna uma lista de dicionários, onde cada dicionário representa um repositório filtrado, ou uma lista vazia se nenhum for encontrado ou ocorrer um erro.

*   **`get_repo_languages(self, username, repo_name)`**:
    *   Busca os dados de linguagens para um repositório específico (`username/repo_name`).
    *   A API retorna um dicionário onde as chaves são os nomes das linguagens e os valores são o número de bytes de código detectados para essa linguagem.
    *   Retorna o dicionário de linguagens ou `None` em caso de erro.

*   **`collect_languages_by_year(self, organizations)`**:
    *   Orquestra o processo principal de coleta de dados.
    *   **Resiliência/Retomada:** Tenta carregar dados de um arquivo `languages_by_year.csv` existente para evitar reprocessar organizações já analisadas em execuções anteriores.
    *   Itera sobre a lista de `organizations`.
    *   Para cada organização:
        *   Verifica se já foi processada (lendo do CSV carregado).
        *   Chama `get_user_repos` para obter a lista de repositórios.
        *   Itera sobre cada repositório:
            *   Extrai o ano de criação (`created_at`).
            *   Chama `get_repo_languages` para obter as linguagens.
            *   Se houver dados de linguagem, adiciona uma entrada para cada linguagem à lista `languages_by_year`, contendo `Organization`, `Year`, `Language`, e `Bytes`.
            *   Inclui uma pausa (`time.sleep(0.5)`) entre as requisições de linguagens de repositórios.
    *   Retorna a lista completa `languages_by_year` (combinando dados existentes e novos).

*   **`save_to_csv(self, languages_by_year, filename='languages_by_year.csv')`**:
    *   Converte a lista de dicionários `languages_by_year` em um DataFrame Pandas.
    *   Salva o DataFrame em um arquivo CSV com o nome especificado.

*   **`plot_languages_by_year(self, languages_by_year, top_n=5)`**:
    *   Gera visualizações dos dados coletados usando Matplotlib.
    *   Converte a lista em um DataFrame Pandas.
    *   **Gráfico Agregado:**
        *   Calcula o total de bytes por linguagem em todos os anos e organizações.
        *   Seleciona as `top_n` linguagens com mais bytes.
        *   Cria uma tabela pivotada (anos nas linhas, linguagens nas colunas, bytes como valores).
        *   Gera um gráfico de barras empilhadas mostrando a distribuição das top N linguagens por ano.
        *   Salva o gráfico como `languages_by_year_all.png`.
    *   **Gráficos por Organização:**
        *   Itera sobre cada organização única presente nos dados.
        *   Filtra os dados para a organização atual.
        *   Calcula as `top_n` linguagens para *essa* organização.
        *   Cria uma tabela pivotada e gera um gráfico de barras empilhadas similar ao agregado, mas específico da organização.
        *   Salva o gráfico como `languages_by_year_<org>.png`.
    *   Usa `plt.close()` para liberar memória após salvar cada gráfico.

### 6.3. Bloco de Execução Principal (`if __name__ == "__main__":`)

*   Este bloco é executado quando o script é chamado diretamente.
*   Obtém o `GITHUB_TOKEN` da variável de ambiente.
*   Instancia a classe `GithubAnalyzer`.
*   Define a lista de `organizations` a serem analisadas.
*   Chama `collect_languages_by_year` para iniciar a coleta.
*   Chama `save_to_csv` para persistir os resultados.
*   Chama `plot_languages_by_year` para gerar as visualizações.

## 7. Saída

*   **`languages_by_year.csv`**: Arquivo CSV com as seguintes colunas:
    *   `Organization`: Nome da organização/usuário do GitHub.
    *   `Year`: Ano de criação do repositório.
    *   `Language`: Linguagem de programação detectada.
    *   `Bytes`: Número de bytes de código para essa linguagem nesse repositório.
*   **`languages_by_year_all.png`**: Imagem PNG contendo um gráfico de barras empilhadas das Top 5 linguagens (por total de bytes) agregadas de todas as organizações analisadas, distribuídas por ano de criação do repositório.
*   **`languages_by_year_<org>.png`**: Imagens PNG (uma para cada organização analisada, substituindo `<org>` pelo nome da organização) contendo um gráfico de barras empilhadas das Top 5 linguagens (por total de bytes) para *aquela* organização específica, distribuídas por ano de criação do repositório.

## 8. Pontos de Atenção e Limitações

*   **Limites da API do GitHub:** O uso de um token é crucial. Mesmo com token, existem limites. O script implementa tratamento básico de rate limit, mas execuções muito longas ou em contas com limites baixos podem encontrar problemas.
*   **Nomes de Organização:** A precisão dos nomes das organizações no GitHub é fundamental. Nomes incorretos ou alterados (como `facebook` -> `meta`) resultarão em falhas ou dados ausentes.
*   **Interpretação dos Dados:**
    *   Os "bytes de código" são uma métrica bruta fornecida pela API do GitHub e podem não refletir perfeitamente a importância ou complexidade do uso de uma linguagem.
    *   Agrupar pelo ano de **criação** do repositório é uma simplificação. Não reflete a evolução do uso da linguagem *dentro* do repositório ao longo do tempo.
*   **Escopo dos Dados:** O script analisa apenas repositórios **públicos**, **não arquivados** e que **não são forks**. Repositórios privados ou pertencentes a usuários individuais (não organizações) não são cobertos, a menos que o nome de usuário seja explicitamente adicionado à lista `organizations`.
*   **Tempo de Execução:** A coleta de dados pode ser demorada, especialmente para organizações com muitos repositórios. A funcionalidade de retomada (usando o CSV existente) ajuda a mitigar isso em execuções subsequentes.

---

Esta documentação tem por objetivo fornecer a qualquer pessoa que precise trabalhar com o script uma compreensão clara de seu propósito, funcionamento e como utilizá-lo.