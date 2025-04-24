"""

Módulo responsável pela criação das figuras de visualização de dados.

Este script contém funções que utilizam a biblioteca Plotly Express para gerar
diferentes tipos de gráficos (barras, linhas, área, pizza) a partir de
DataFrames pré-processados (geralmente provenientes do módulo data_handler).
Cada função retorna um objeto de figura Plotly (plotly.graph_objects.Figure)
que pode ser exibido em uma aplicação Streamlit usando st.plotly_chart.

"""

# --- IMPORTS ---

import plotly.express as px
import pandas as pd 

# --- FUNÇÕES DE PLOTAGEM ---

def plot_top_languages_overall(df_top_langs: pd.DataFrame, top_n: int):
    """Cria gráfico de barras para as Top N linguagens gerais."""
    if df_top_langs.empty: return None
    fig = px.bar(
        df_top_langs,
        x='Language',
        y='Bytes',
        title=f"Top {top_n} Linguagens de Programação",
        labels={'Language': 'Linguagem', 'Bytes': 'Volume (Bytes)'},
        color='Language',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig.update_layout(height=500, showlegend=False)
    return fig

def plot_org_total_bytes(df_org_bytes: pd.DataFrame):
    """Cria gráfico de barras para o total de bytes por organização."""
    if df_org_bytes.empty: return None
    fig = px.bar(
        df_org_bytes,
        x='Organization',
        y='Bytes',
        title="Volume Total de Código por Organização",
        color='Organization',
        labels={'Organization': 'Organização', 'Bytes': 'Volume (Bytes)'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(height=500, showlegend=False)
    return fig

def plot_bytes_trend(df_bytes_year: pd.DataFrame):
    """Cria gráfico de linha para a evolução do total de bytes por ano."""
    if df_bytes_year.empty: return None
    fig = px.line(
        df_bytes_year,
        x='Year',
        y='Bytes',
        title="Volume de Código por Ano",
        markers=True,
        labels={'Year': 'Ano', 'Bytes': 'Volume (Bytes)'},
        color_discrete_sequence=['#3366CC'] 
    )
    fig.update_layout(height=400)
    return fig

def plot_language_trends(df_lang_trends: pd.DataFrame, top_n: int, top_n_lang_names: list):
    """Cria gráfico de área empilhada para a evolução das Top N linguagens."""
    if df_lang_trends.empty: return None
    fig = px.area(
        df_lang_trends,
        x='Year',
        y='Bytes',
        color='Language',
        title=f"Evolução das Top {top_n} Linguagens",
        labels={'Year': 'Ano', 'Bytes': 'Volume (Bytes)', 'Language': 'Linguagem'},
        category_orders={"Language": top_n_lang_names} # Mantém a ordem
    )
    fig.update_layout(height=500)
    return fig

# --- FUNÇÕES DE PLOTAGEM DE ORGANIZAÇÕES ---
def plot_org_trend(df_org_year_data: pd.DataFrame, org_name: str):
    """Cria gráfico de linha para a evolução de UMA organização."""
    if df_org_year_data.empty: return None
    fig = px.line(
        df_org_year_data,
        x='Year',
        y='Bytes',
        title=f"Evolução do Volume de Código - {org_name}",
        markers=True,
        labels={'Year': 'Ano', 'Bytes': 'Volume (Bytes)'}
    )
    return fig

def plot_org_top_languages(df_top_langs_org: pd.DataFrame, org_name: str, top_n: int):
    """Cria gráfico de pizza para as Top N linguagens de UMA organização."""
    if df_top_langs_org.empty: return None
    fig = px.pie(
        df_top_langs_org,
        values='Bytes',
        names='Language',
        title=f"Top {top_n} Linguagens - {org_name}",
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig