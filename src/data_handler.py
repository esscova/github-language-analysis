"""

Módulo responsável pelo carregamento, tratamento e agregação dos dados.

Este script contém funções para:
- Carregar dados do arquivo CSV especificado.
- Padronizar nomes de organizações.
- Tratar tipos de dados (como o ano).
- Filtrar o DataFrame principal com base nas seleções do usuário.
- Calcular métricas agregadas (KPIs, totais por linguagem/organização/ano)
  necessárias para as visualizações no dashboard.
Utiliza o cache do Streamlit (@st.cache_data) na função de carregamento
para otimizar a performance.

"""
# --- IMPORTS ---

import pandas as pd
import os
import streamlit as st #! precisa para o @st.cache_data

# --- CONSTANTES ---

CSV_FILE = './data/languages_by_year.csv'
PADRONIZACAO_NOMES = {
    'microsoft': 'Microsoft',
    'APPLE': 'Apple',
    'nvidia': 'NVIDIA',
    'facebook': 'Meta',
    'amzn': 'Amazon',
    'netflix': 'Netflix',
    'google': 'Alphabet/Google',
    'uber': 'Uber'
}

# --- FUNÇÕES DE CARREGAMENTO E FILTRAGEM ---

@st.cache_data 
def load_data():
    """
    Carrega os dados do CSV, aplica padronização de nomes, trata tipos
    e retorna o DataFrame completo. Retorna None em caso de erro.
    """
    if not os.path.exists(CSV_FILE):
        st.error(f"Erro: Arquivo '{CSV_FILE}' não encontrado.")
        return None
    try:
        df = pd.read_csv(CSV_FILE)
        df['Organization'] = df['Organization'].replace(PADRONIZACAO_NOMES)
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        df.dropna(subset=['Year'], inplace=True) 
        df['Year'] = df['Year'].astype(int)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar ou processar o arquivo CSV: {e}")
        return None

def filter_data(df, selected_orgs, selected_years):
    """
    Filtra o DataFrame com base nas organizações e anos selecionados.
    """
    if df is None or not selected_orgs: 
        return pd.DataFrame() 

    return df[
        (df['Organization'].isin(selected_orgs)) &
        (df['Year'] >= selected_years[0]) &
        (df['Year'] <= selected_years[1])
    ].copy() # para evitar SettingWithCopyWarning

# --- FUNÇÕES DE MÉTRICAS ---

def get_kpi_metrics(df_filtered):
    """Calcula métricas para os KPIs."""
    if df_filtered.empty:
        return 0, 0, 0
    
    total_bytes = df_filtered['Bytes'].sum()
    num_orgs = df_filtered['Organization'].nunique() 
    num_langs = df_filtered['Language'].nunique()

    return total_bytes, num_orgs, num_langs

def get_top_languages_overall(df_filtered, top_n):
    """Calcula as Top N linguagens gerais nos dados filtrados."""
    if df_filtered.empty:
        return pd.DataFrame(columns=['Language', 'Bytes'])
    
    return df_filtered.groupby('Language')['Bytes'].sum().nlargest(top_n).reset_index()

def get_bytes_per_org(df_filtered):
    """Calcula o total de bytes por organização."""
    if df_filtered.empty:
        return pd.DataFrame(columns=['Organization', 'Bytes'])
    
    return df_filtered.groupby('Organization')['Bytes'].sum().reset_index().sort_values('Bytes', ascending=False)

def get_bytes_per_year(df_filtered):
    """Calcula o total de bytes por ano."""
    if df_filtered.empty:
        return pd.DataFrame(columns=['Year', 'Bytes'])
    
    return df_filtered.groupby('Year')['Bytes'].sum().reset_index()

def get_language_trends_over_time(df_filtered, top_n_lang_names):
    """Prepara dados para o gráfico de tendências de linguagens ao longo do tempo."""
    if df_filtered.empty or not top_n_lang_names:
        return pd.DataFrame(columns=['Year', 'Language', 'Bytes'])
    
    df_temp_trends = df_filtered[df_filtered['Language'].isin(top_n_lang_names)]
    return df_temp_trends.groupby(['Year', 'Language'])['Bytes'].sum().reset_index()

# --- FUNÇÕES AUXILIARES ---
def get_org_bytes_per_year(df_org):
    """Calcula bytes por ano para UMA organização específica."""
    if df_org.empty:
        return pd.DataFrame(columns=['Year', 'Bytes'])
    return df_org.groupby('Year')['Bytes'].sum().reset_index()

def get_top_languages_for_org(df_org, top_n):
    """Calcula as Top N linguagens para UMA organização específica."""
    if df_org.empty:
        return pd.DataFrame(columns=['Language', 'Bytes'])
    return df_org.groupby('Language')['Bytes'].sum().nlargest(top_n).reset_index()