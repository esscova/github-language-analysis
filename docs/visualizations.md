## Documentação: `visualizations.py`

**Propósito:**

Este módulo é dedicado exclusivamente à **criação das figuras de visualização** de dados utilizando a biblioteca Plotly Express. Ele recebe DataFrames processados e retorna objetos de figura Plotly prontos para serem exibidos no dashboard. Isso separa a lógica de criação de gráficos da lógica de manipulação de dados e da interface do usuário.

**Funcionalidades Principais:**

1.  **Funções de Plotagem:** Cada função é responsável por gerar um tipo específico de gráfico:
    *   `plot_top_languages_overall`: Cria um gráfico de barras para as linguagens mais usadas no geral.
    *   `plot_org_total_bytes`: Cria um gráfico de barras comparando o volume total por organização.
    *   `plot_bytes_trend`: Cria um gráfico de linha mostrando a tendência do volume total ao longo do tempo.
    *   `plot_language_trends`: Cria um gráfico de área empilhada mostrando a evolução da participação das Top N linguagens ao longo do tempo.
    *   `plot_org_trend`: Cria um gráfico de linha mostrando a tendência de volume para uma única organização.
    *   `plot_org_top_languages`: Cria um gráfico de pizza mostrando as Top N linguagens para uma única organização.
2.  **Uso de Plotly Express:** Utiliza `plotly.express` (importado como `px`) para gerar os gráficos de forma concisa.
3.  **Customização:** Aplica customizações básicas aos gráficos, como títulos, rótulos de eixos (`labels`), paletas de cores (`color_discrete_sequence`), e ajustes de layout (altura, esconder legenda, etc.).
4.  **Entrada e Saída:**
    *   **Input:** Recebe DataFrames do Pandas como argumentos (geralmente agregados pelo `data_handler.py`).
    *   **Output:** Retorna objetos `plotly.graph_objects.Figure` ou `None` se o DataFrame de entrada estiver vazio.

**Interação:**

*   É chamado pelo `app.py` para gerar as visualizações que serão exibidas nas diferentes abas do dashboard.
*   Recebe dados processados do `data_handler.py` (indiretamente, via `app.py`).

**Dependências:**

*   `plotly` (especificamente `plotly.express`)
*   `pandas` (usado para type hints nos argumentos das funções)