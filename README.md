# GitHub Language Analysis 

Este projeto demonstra um fluxo de trabalho básico de engenharia de dados para coletar, processar, armazenar e visualizar dados sobre o uso de linguagens de programação em repositórios públicos de organizações específicas no GitHub. O objetivo é analisar tendências e comparar o perfil tecnológico dessas organizações com base nos dados da API do GitHub.

![image](./src/assets/pipeline.png)

O projeto é composto por duas partes principais:
1.  Um script de coleta de dados (`src/github_analyzer.py`) que interage com a API do GitHub.
2.  Um dashboard interativo (`src/app.py` e módulos auxiliares) construído com Streamlit para visualizar os dados coletados.

## Funcionalidades

**Coleta de Dados:**
*   Conecta-se à API v3 do GitHub usando um token de acesso pessoal (recomendado, lido de `.env`).
*   Busca repositórios públicos para uma lista configurável de organizações.
*   Filtra repositórios para excluir forks e arquivos arquivados.
*   Extrai dados de linguagens (bytes de código por linguagem) e data de criação para cada repositório.
*   Implementa tratamento básico de limites de taxa (rate limiting) da API, com pausas e retentativas.
*   Salva os dados coletados em um arquivo CSV (`src/data/languages_by_year.csv`).
*   Tenta retomar a coleta a partir de dados existentes no CSV para evitar reprocessamento.

**Dashboard de Visualização (Streamlit App):**
*   Lê os dados processados do arquivo `src/data/languages_by_year.csv`.
*   Apresenta uma interface interativa com filtros para:
    *   Seleção de Organizações.
    *   Intervalo de Anos (baseado na criação do repositório).
    *   Número de "Top N" linguagens a serem exibidas.
*   Exibe Key Performance Indicators (KPIs) resumidos.
*   Organiza as visualizações em abas:
    *   **Visão Geral:** Top linguagens gerais e volume total por organização.
    *   **Análise Temporal:** Evolução do volume total e distribuição das linguagens ao longo do tempo.
    *   **Organizações:** Detalhes específicos por organização (tendência e top linguagens).
    *   **Dados Brutos:** Tabela interativa com os dados filtrados e opção de download.
    *   **Sobre:** Descrição do projeto, metodologia e limitações.
*   Utiliza Plotly para gráficos interativos.
*   Implementa cache (`@st.cache_data`) para otimizar o carregamento de dados.
*   Estrutura modularizada (`src/data_handler.py`, `src/visualizations.py`) para separação de responsabilidades.

## Estrutura do Projeto

```
github-language-analysis/
├── docs/                      # Documentação detalhada dos módulos
│   ├── app.md
│   ├── data_handler.md
│   ├── github_analyzer.md
│   └── visualizations.md
├── src/                       # Código fonte do projeto
│   ├── app.py                 # Script principal da aplicação Streamlit
│   ├── assets/                # Recursos estáticos (imagens, etc.)
│   ├── data/                  # Dados gerados ou utilizados
│   │   └── languages_by_year.csv
│   ├── data_handler.py        # Módulo de manipulação de dados
│   ├── github_analyzer.py     # Script de coleta de dados
│   └── visualizations.py      # Módulo de geração de gráficos
├── .env.example               # Exemplo de como deve ser o arquivo .env
├── .gitignore                 # Especifica arquivos e diretórios a serem ignorados pelo Git
├── requirements.txt           # Dependências Python do projeto
└── README.md                  # Este arquivo
```
## Configuração e Instalação

1.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/esscova/github-language-analysis.git
    cd github-language-analysis
    ```

2.  **Crie e Ative um Ambiente Virtual (Recomendado):**
    ```bash
    python -m venv .venv
    # No Linux/macOS:
    source venv/bin/activate
    # No Windows:
    #.\venv\Scripts\activate
    ```

3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o Token do GitHub:**
    *   Crie um arquivo chamado `.env` na raiz do projeto.
    *   Adicione a seguinte linha ao arquivo `.env`, substituindo `seu_token_aqui` pelo seu Token de Acesso Pessoal do GitHub (com escopo `public_repo`):
        ```dotenv
        GITHUB_TOKEN='seu_token_aqui'
        ```
    *   **Importante:** Certifique-se de que o arquivo `.env` está listado no seu `.gitignore` para evitar o envio acidental do seu token. 

## Contato
[Wellington M Santos](https://www.linkedin.com/in/wellington-moreira-santos/)