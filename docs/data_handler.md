## Documentação: `data_handler.py`

**Propósito:**

Este módulo é responsável por toda a **manipulação e preparação dos dados** necessários para o dashboard. Ele isola a lógica de acesso, limpeza, transformação e agregação dos dados do restante da aplicação.

**Funcionalidades Principais:**

1.  **Constantes:** Define constantes importantes como o caminho para o arquivo CSV (`CSV_FILE`) e o dicionário para padronização de nomes de organizações (`PADRONIZACAO_NOMES`).
2.  **Carregamento e Pré-processamento (`load_data`):**
    *   Lê o arquivo CSV especificado.
    *   Aplica a padronização dos nomes das organizações usando o dicionário `PADRONIZACAO_NOMES`.
    *   Converte a coluna 'Year' para tipo numérico, tratando possíveis erros e removendo linhas inválidas.
    *   Utiliza `@st.cache_data` para armazenar em cache o resultado do carregamento, evitando releituras desnecessárias do arquivo e melhorando a performance do dashboard.
    *   Retorna o DataFrame processado ou `None` em caso de erro.
3.  **Filtragem (`filter_data`):**
    *   Recebe o DataFrame completo e os critérios de filtro (organizações e anos selecionados).
    *   Retorna um novo DataFrame contendo apenas as linhas que atendem aos critérios.
    *   Lida com casos onde o DataFrame de entrada é inválido ou nenhuma organização é selecionada.
4.  **Cálculo de Métricas e Agregações:** Fornece um conjunto de funções que recebem um DataFrame (geralmente o filtrado) e realizam agregações específicas usando `pandas`:
    *   `get_kpi_metrics`: Calcula os valores totais para os KPIs (Bytes, Nº de Orgs, Nº de Linguagens).
    *   `get_top_languages_overall`: Identifica as N linguagens mais usadas (por bytes) no geral.
    *   `get_bytes_per_org`: Calcula o total de bytes por organização.
    *   `get_bytes_per_year`: Calcula o total de bytes por ano.
    *   `get_language_trends_over_time`: Agrega bytes por ano e linguagem para as Top N linguagens, preparando os dados para o gráfico de tendências.
    *   `get_org_bytes_per_year`: Calcula bytes por ano para *uma única* organização (usado na aba "Organizações").
    *   `get_top_languages_for_org`: Calcula as Top N linguagens para *uma única* organização (usado na aba "Organizações").

**Interação:**

*   **Input:** Lê dados do arquivo definido em `CSV_FILE`.
*   **Output:** Fornece DataFrames processados e agregados para o `app.py`.

**Dependências:**

*   `pandas`
*   `os` (para verificar a existência do arquivo)
*   `streamlit` (especificamente para o decorador `@st.cache_data`)
