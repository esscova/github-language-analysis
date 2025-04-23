# --- IMPORTS ---

import streamlit as st
import pandas as pd
import data_handler       # módulo de dados
import visualizations     # módulo de plots

# --- CLASSE PRINCIPAL ---

class DashboardApp:
    """
    Encapsula a lógica e a interface do dashboard Streamlit
    para análise de linguagens do GitHub.
    """
    def __init__(self):
        """Inicializa a aplicação."""
        self.TOP_N_DEFAULT = 10
        self.df_full = None
        self.df_filtered = pd.DataFrame() # inicia vazio

    def _setup_page(self):
        """Configura as definições iniciais da página Streamlit."""
        st.set_page_config(
            page_title="Análise de Linguagens de Programação - GitHub",
            page_icon="📈",
            layout="wide"
        )

    def _apply_custom_css(self):
        """Aplica CSS customizado, direcionando o container do st.metric."""
        st.markdown("""
        <style>
        div[data-testid="stMetric"] {
            background-color: #FFFFFF;        
            border: 1px solid #e6e6e6;        
            padding: 15px 20px 15px 20px;     
            border-radius: 10px;              
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); 
            transition: box-shadow 0.3s ease-in-out; 
            margin-bottom: 15px;              
        }

        div[data-testid="stMetric"]:hover {
             box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15); 
        }

        div[data-testid="stMetric"] div[data-testid="stMetricLabel"] {
            font-size: 0.95em;
            color: #555555;
        }
                    
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            font-size: 1.8em;
            font-weight: bold;
            color: #1E88E5; 
        }
        div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
             font-size: 0.85em;
        }
        </style>
        """, unsafe_allow_html=True)

    def _load_initial_data(self):
        """Carrega os dados iniciais usando o data_handler."""
        self.df_full = data_handler.load_data() 
        if self.df_full is None:
            st.error("❌ Falha no carregamento dos dados iniciais. Verifique o console e a existência do arquivo CSV.")

    def _render_sidebar(self):
        """Renderiza a barra lateral com filtros e informações."""
        st.sidebar.header("Controles e Filtros")

        # filtros default caso os dados não carreguem
        selected_orgs_sb = []
        selected_years_sb = (0, 0)
        top_n_sb = self.TOP_N_DEFAULT

        if self.df_full is not None:
            st.sidebar.subheader("Filtros de Organização")
            all_orgs = sorted(self.df_full['Organization'].unique())
            selected_orgs_sb = st.sidebar.multiselect(
                "Selecione as Organizações:",
                options=all_orgs,
                default=all_orgs
            )

            st.sidebar.subheader("Filtros de Tempo")
            min_year, max_year = int(self.df_full['Year'].min()), int(self.df_full['Year'].max())
            if min_year > max_year: min_year = max_year # força min_year = max_year em cenario de erro ou inconsistencia de dados
            selected_years_sb = st.sidebar.slider(
                "Intervalo de Anos:",
                min_value=min_year,
                max_value=max_year,
                value=(min_year, max_year)
            )

            st.sidebar.subheader("Configurações de Visualização")
            top_n_sb = st.sidebar.slider(
                "Top N Linguagens:",
                min_value=3,
                max_value=20,
                value=self.TOP_N_DEFAULT
            )
        else:
            st.sidebar.error("Dados não carregados. Filtros indisponíveis.")


        # st.sidebar.markdown("---")
        st.sidebar.info("Dashboard interativo para análise de linguagens no GitHub.")
        st.sidebar.caption("Desenvolvido por [Wellington M Santos](https://www.linkedin.com/in/wellington-moreira-santos/).")

        return selected_orgs_sb, selected_years_sb, top_n_sb

    def _render_kpis(self):
        """Renderiza os Key Performance Indicators (KPIs) no topo."""
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        total_bytes, num_orgs_filtered, num_langs = data_handler.get_kpi_metrics(self.df_filtered)

        with kpi_col1:
            st.metric("Volume Total de Código", f"{total_bytes / 1e9:.2f} GB")
        with kpi_col2:
            st.metric("Organizações na Análise", num_orgs_filtered)
        with kpi_col3:
            st.metric("Linguagens Identificadas", num_langs)

    def _render_tab_visao_geral(self, top_n):
        """Renderiza o conteúdo da aba 'Visão Geral'."""
        st.header("Visão Geral de Linguagens")

        # Gráfico: Top N Linguagens Geral
        df_top_langs = data_handler.get_top_languages_overall(self.df_filtered, top_n)
        fig_overall_langs = visualizations.plot_top_languages_overall(df_top_langs, top_n)
        if fig_overall_langs:
            st.plotly_chart(fig_overall_langs, use_container_width=True)
        else:
            st.write("Nenhum dado para o gráfico de Top Linguagens Gerais.")

        # Gráfico: Comparativo de Bytes Totais por Organização
        st.subheader("Volume em Bytes por Organização")
        df_org_bytes = data_handler.get_bytes_per_org(self.df_filtered)
        fig_org_total = visualizations.plot_org_total_bytes(df_org_bytes)
        if fig_org_total:
            st.plotly_chart(fig_org_total, use_container_width=True)
        else:
            st.write("Nenhum dado para o gráfico de Volume por Organização.")

    def _render_tab_analise_temporal(self, top_n):
        """Renderiza o conteúdo da aba 'Análise Temporal'."""
        st.header("Análise Temporal")

        # Gráfico: Evolução do Total de Bytes por Ano
        df_bytes_year = data_handler.get_bytes_per_year(self.df_filtered)
        fig_bytes_trend = visualizations.plot_bytes_trend(df_bytes_year)
        if fig_bytes_trend:
            st.plotly_chart(fig_bytes_trend, use_container_width=True)
        else:
            st.write("Nenhum dado para o gráfico de Volume por Ano.")

        # Gráfico: Evolução das Top N Linguagens por Ano (Área Empilhada)
        st.subheader(f"Distribuição das Linguagens ao Longo do Tempo")
        df_top_langs = data_handler.get_top_languages_overall(self.df_filtered, top_n)
        top_n_lang_names = df_top_langs['Language'].tolist() if not df_top_langs.empty else []
        df_lang_trends = data_handler.get_language_trends_over_time(self.df_filtered, top_n_lang_names)
        fig_lang_trends = visualizations.plot_language_trends(df_lang_trends, top_n, top_n_lang_names)
        if fig_lang_trends:
            st.plotly_chart(fig_lang_trends, use_container_width=True)
        else:
            st.write("Nenhum dado para o gráfico de Evolução das Linguagens.")

    def _render_tab_organizacoes(self, selected_orgs, top_n):
        """Renderiza o conteúdo da aba 'Organizações'."""
        st.header("Análise por Organização")

        if len(selected_orgs) > 3:
            org_tabs = st.tabs(selected_orgs)
            for i, org in enumerate(selected_orgs):
                with org_tabs[i]:
                    st.subheader(f"Perfil de {org}")
                    df_org = self.df_filtered[self.df_filtered['Organization'] == org]
                    self._render_org_details(df_org, org, top_n)
        else:
            for org in selected_orgs:
                st.subheader(f"Perfil de {org}")
                df_org = self.df_filtered[self.df_filtered['Organization'] == org]
                col1, col2 = st.columns(2)
                with col1:
                    df_org_year_data = data_handler.get_org_bytes_per_year(df_org)
                    fig_org_trend = visualizations.plot_org_trend(df_org_year_data, org)
                    if fig_org_trend: st.plotly_chart(fig_org_trend, use_container_width=True)
                with col2:
                    df_top_langs_org = data_handler.get_top_languages_for_org(df_org, top_n)
                    fig_org_langs = visualizations.plot_org_top_languages(df_top_langs_org, org, top_n)
                    if fig_org_langs: st.plotly_chart(fig_org_langs, use_container_width=True)

    def _render_org_details(self, df_org, org_name, top_n):
        """Renderiza os gráficos de detalhes para uma única organização (usado na aba 'Organizações')."""
        # Gráfico de tendência temporal
        df_org_year_data = data_handler.get_org_bytes_per_year(df_org)
        fig_org_trend = visualizations.plot_org_trend(df_org_year_data, org_name)
        if fig_org_trend: st.plotly_chart(fig_org_trend, use_container_width=True)

        # Top linguagens
        df_top_langs_org = data_handler.get_top_languages_for_org(df_org, top_n)
        fig_org_langs = visualizations.plot_org_top_languages(df_top_langs_org, org_name, top_n)
        if fig_org_langs: st.plotly_chart(fig_org_langs, use_container_width=True)

    def _render_tab_dados_brutos(self):
        """Renderiza o conteúdo da aba 'Dados Brutos'."""
        st.header("Dados Detalhados")
        st.dataframe(
            self.df_filtered.sort_values(['Organization', 'Year', 'Bytes'], ascending=[True, False, False]),
            use_container_width=True,
            height=600
        )
        try:
            csv = self.df_filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Baixar Dados Filtrados em CSV",
                data=csv,
                file_name="github_languages_filtered.csv",
                mime="text/csv",
            )
        except Exception as e:
            st.error(f"Não foi possível preparar os dados para download: {e}")

    def run(self):
        """Executa o fluxo principal da aplicação Streamlit."""
        self._setup_page()
        self._apply_custom_css() 
        self._load_initial_data()

        selected_orgs, selected_years, top_n = self._render_sidebar()

        # --- Interface Principal ---
        st.markdown("<h1 style='text-align: center; padding: 20px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); background-color: #FFFFFF; margin-bottom: 15px;'>Análise do uso de linguagens de programação por organizações com base em repositórios publicos.</h1>", unsafe_allow_html=True)

        if self.df_full is not None and selected_orgs: # tem dados e algum org?
            self.df_filtered = data_handler.filter_data(self.df_full, selected_orgs, selected_years)

            if not self.df_filtered.empty:
                self._render_kpis() 

                # --- Abas ---
                tab1, tab2, tab3, tab4 = st.tabs(["Visão Geral", "Análise Temporal", "Organizações", "Dados Brutos"])

                with tab1: self._render_tab_visao_geral(top_n)
                with tab2: self._render_tab_analise_temporal(top_n)
                with tab3: self._render_tab_organizacoes(selected_orgs, top_n) 
                with tab4: self._render_tab_dados_brutos()

            else:
                st.warning("⚠️ Nenhum dado corresponde aos filtros selecionados. Ajuste os filtros na barra lateral.")

        elif not selected_orgs and self.df_full is not None:
             st.warning("⬅️ Por favor, selecione pelo menos uma organização na barra lateral para exibir os dados.")

# --- FIM DA CLASSE

if __name__ == "__main__":
    app = DashboardApp()
    app.run()