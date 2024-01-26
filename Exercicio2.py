#!/usr/bin/env python
# coding: utf-8

# # Exercícios 
# 
# Utilize os arquivos do **RECLAME AQUI** e crie um dashboard com algumas caracteristicas. 
# 
# Empresas: 
# - Hapvida
# - Nagem
# - Ibyte
# 
# O painel deve conter tais informações: 
# 
# 1. Série temporal do número de reclamações. 
# 
# 2. Frequência de reclamações por estado. 
# 
# 3. Frequência de cada tipo de **STATUS**
# 
# 4. Distribuição do tamanho do texto (coluna **DESCRIÇÃO**) 
# 
# 
# Alguns botões devem ser implementados no painel para operar filtros dinâmicos. Alguns exemplos:: 
# 
# 1. Seletor da empresa para ser analisada. 
# 
# 2. Seletor do estado. 
# 
# 3. Seletor por **STATUS**
# 
# 4. Seletor de tamanho do texto 
# 
# Faça o deploy da aplicação. Dicas: 
# 
# https://www.youtube.com/watch?v=vw0I8i7QJRk&list=PLRFQn2r6xhgcDMhp9NCWMqDYGfeeYsn5m&index=16&t=252s
# 
# https://www.youtube.com/watch?v=HKoOBiAaHGg&t=515s
# 
# Exemplo do github
# https://github.com/jlb-gmail/streamlit_teste
# 
# 
# **OBSERVAÇÃO**
# 
# A resposta do exercicio é o link do github e o link da aplicação. Coloque-os abaixo.  
# 

# - MBA em Ciência de Dados - Turma 05
# - Nome: David Jonatas Vieira de Oliveira
# - Disciplina: Dashboard
# - Prof.: Jorge Araujo

# 1 - IMPORTANDO OS DADOS

import pandas as pd
# Carregar os dados
hapvida_data = pd.read_csv('RECLAMEAQUI_HAPVIDA.csv')
nagem_data = pd.read_csv('RECLAMEAQUI_NAGEM.csv')
ibyte_data = pd.read_csv('RECLAMEAQUI_IBYTE.csv')

hapvida_data.head()

nagem_data.head()

ibyte_data.head()

# Adicionar uma coluna para identificar a empresa
hapvida_data['EMPRESA'] = 'Hapvida'
nagem_data['EMPRESA'] = 'Nagem'
ibyte_data['EMPRESA'] = 'Ibyte'

# Juntar os dataframes
df = pd.concat([hapvida_data, nagem_data, ibyte_data], ignore_index=True)

# Exibir as primeiras linhas para verificar
df.head()

# 2 - Analisando e tratando os dados

df.info()

# Verificar campos em branco
df.isna().sum()

# Verificar valores nulos
df.isnull().sum()

# Mudar o tipo da coluna 'ID' de objeto para string
df['ID'] = df['ID'].astype(str)

# Mudar a variável de data
df['TEMPO'] = pd.to_datetime(df['TEMPO'])

# Criar uma nova coluna 'ESTADO' extraindo a UF da coluna 'LOCAL'
df['ESTADO'] = df['LOCAL'].apply(lambda x: x.split(' - ')[-1])

df['ESTADO'].value_counts()

# Substituir valores inconsistentes por NaN
import numpy as np
df.replace(['naoconsta       ', 'P', '--', 'C'], np.nan, inplace=True)

df['ESTADO'].value_counts()

# Remover linhas que contêm NaN
df.dropna(inplace=True)

df['ESTADO'].value_counts()

# Excluir linhas onde qualquer coluna contém 'naoconsta'
df = df[~df.apply(lambda row: row.astype(str).str.contains('naoconsta').any(), axis=1)]

df['ESTADO'].value_counts()


# 3 - Criando o dashboard

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Iniciar o Streamlit app
st.title('Dashboard de Reclamações')

# Modificar o DataFrame usando .loc[]
df.loc[:, 'COMPRIMENTO_DESCRICAO'] = df['DESCRICAO'].apply(len)

# E - Seletor da Empresa para ser analisada

# Seletor de Empresa
empresa_selecionada = st.selectbox('Selecione a Empresa', df['EMPRESA'].unique())

# Filtrar os dados com base na empresa selecionada
dados_filtrados = df[df['EMPRESA'] == empresa_selecionada]

# F - Seletor do Estado

# Seletor de Estado com Multiselect
estados_selecionados = st.multiselect('Selecione os Estados', df['ESTADO'].unique())

# Filtrar os dados com base na empresa e estado selecionados
dados_filtrados = df[(df['EMPRESA'] == empresa_selecionada) & (df['ESTADO'].isin(estados_selecionados))]

# G - Seletor do Status

# Seletor de Status usando Radio Button
status_selecionado = st.radio('Selecione o Status', df['STATUS'].unique())

# Filtrar os dados com base na empresa, estado e status selecionados
dados_filtrados = df[(df['EMPRESA'] == empresa_selecionada) & 
                       (df['ESTADO'].isin(estados_selecionados)) &
                       (df['STATUS'] == status_selecionado)]


# H - Seletor de tamanho do texto

# Seletor de Tamanho do Texto com Slider
min_len, max_len = int(df['COMPRIMENTO_DESCRICAO'].min()), int(df['COMPRIMENTO_DESCRICAO'].max())
tamanho_selecionado = st.slider('Selecione o Intervalo de Tamanho do Texto', min_len, max_len, (min_len, max_len))

# Filtrar os dados com base no tamanho selecionado
dados_filtrados = df[(df['EMPRESA'] == empresa_selecionada) & 
                       (df['ESTADO'].isin(estados_selecionados)) &
                       (df['STATUS'] == status_selecionado) &
                       (df['COMPRIMENTO_DESCRICAO'] >= tamanho_selecionado[0]) &
                       (df['COMPRIMENTO_DESCRICAO'] <= tamanho_selecionado[1])]

# A - Série temporal do número de reclamações

# Agrupar por data e contar o número de reclamações
serie_temporal = df.groupby(df['TEMPO']).size()

# Série Temporal do Número de Reclamações
st.subheader('Série Temporal do Número de Reclamações')
plt.figure(figsize=(10, 4))
plt.plot(serie_temporal.index, serie_temporal.values, marker='o')
plt.xticks(rotation=45)
plt.xlabel('Data')
plt.ylabel('Número de Reclamações')
st.pyplot(plt)

# B - Frequência de reclamações por estado

# Frequência de reclamações por estado
frequencia_por_estado = df['ESTADO'].value_counts()

# Frequência de Reclamações por Estado
st.subheader('Frequência de Reclamações por Estado')
plt.figure(figsize=(10, 6))
plt.bar(frequencia_por_estado.index, frequencia_por_estado.values)
plt.xlabel('Estado')
plt.ylabel('Número de Reclamações')
plt.xticks(rotation=45)
st.pyplot(plt)

# C - Frequência de cada tipo de status

# Frequência de cada tipo de status
frequencia_status = df['STATUS'].value_counts()

# Frequência de Cada Tipo de Status
st.subheader('Frequência de Cada Tipo de Status')
plt.figure(figsize=(10, 6))
plt.bar(frequencia_status.index, frequencia_status.values, color='orange')
plt.xlabel('Status')
plt.ylabel('Número de Reclamações')
plt.xticks(rotation=45)
st.pyplot(plt)

# D - Distribuição do tamanho do texto (coluna DESCRIÇÃO) 

# Distribuição do Tamanho do Texto (coluna DESCRIÇÃO)
st.subheader('Distribuição do Tamanho do Texto das Descrições')
plt.figure(figsize=(10, 6))
plt.hist(df['COMPRIMENTO_DESCRICAO'], bins=30, color='skyblue', edgecolor='black')
plt.xlabel('Comprimento da Descrição')
plt.ylabel('Frequência')
st.pyplot(plt)