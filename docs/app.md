## Documentação: `app.py`

**Propósito:**

Este script é o **ponto de entrada principal** e o **orquestrador** da aplicação de dashboard Streamlit. Ele é responsável por definir a interface do usuário (UI), gerenciar o fluxo da aplicação, interagir com os módulos de dados e visualização, e apresentar os resultados ao usuário.

**Funcionalidades Principais:**

1.  **Classe `DashboardApp`:** Encapsula toda a lógica e o estado da aplicação para uma melhor organização (OOP).
2.  **Configuração da Página (`_setup_page`):** Define configurações iniciais do Streamlit, como título da página, ícone e layout (`wide`).
3.  **Estilização Customizada (`_apply_custom_css`):** Aplica CSS para estilizar componentes específicos, como os cartões de métricas (KPIs), adicionando sombras e ajustando a aparência.
4.  **Carregamento de Dados (`_load_initial_data`):** Chama a função `load_data` do módulo `data_handler.py` para carregar e pré-processar os dados do arquivo CSV. Armazena o DataFrame resultante. Lida com erros caso o carregamento falhe.
5.  **Renderização da Barra Lateral (`_render_sidebar`):** Cria a barra lateral interativa contendo:
    *   Um logo (opcional).
    *   Controles de filtro (seleção múltipla de organizações, slider de intervalo de anos, slider para "Top N").
    *   Informações contextuais e créditos.
    *   Retorna os valores selecionados nos filtros pelo usuário.
6.  **Filtragem de Dados:** Aplica os filtros selecionados pelo usuário (obtidos da barra lateral) ao DataFrame completo, utilizando a função `filter_data` do `data_handler.py`.
7.  **Renderização de KPIs (`_render_kpis`):** Exibe métricas chave (Volume Total, Organizações na Análise, Linguagens Identificadas) no topo da página, buscando os dados agregados do `data_handler.py` e utilizando `st.metric`.
8.  **Organização em Abas (`st.tabs`):** Estrutura o conteúdo principal do dashboard em abas lógicas: "Visão Geral", "Análise Temporal", "Organizações", "Dados Brutos" e "Sobre".
9.  **Renderização das Abas (`_render_tab_*`):** Métodos dedicados para renderizar o conteúdo de cada aba:
    *   Chamando funções de agregação do `data_handler.py` para obter os dados específicos daquela visualização.
    *   Chamando as funções de plotagem correspondentes do `visualizations.py` para gerar as figuras Plotly.
    *   Exibindo as figuras Plotly usando `st.plotly_chart`.
    *   Na aba "Organizações", implementa lógica para exibir detalhes por organização (usando sub-abas ou colunas).
    *   Na aba "Dados Brutos", exibe o DataFrame filtrado e um botão de download.
10. **Fluxo Principal (`run`):** Orquestra a chamada de todos os métodos na sequência correta, desde a configuração inicial até a renderização final do conteúdo, gerenciando o estado e as condições de exibição (ex: mostrar aviso se nenhum dado for filtrado).

**Como Executar:**

Este é o script que deve ser executado com o Streamlit:
```bash
streamlit run app.py
```

**Dependências:**

*   `streamlit`
*   `pandas`
*   `data_handler.py` (módulo local)
*   `visualizations.py` (módulo local)

