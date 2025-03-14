ano = 2024
caminho_dados = f"/content/drive/MyDrive/Colab Notebooks/Ad/{ano}_Viagem.csv"
caminho_saída_tabela = f"/content/drive/MyDrive/Colab Notebooks/Ad/output/tabela_{ano}.xlsx"
caminho_saída_grafico1 = f"/content/drive/MyDrive/Colab Notebooks/Ad/output/gráfico1_{ano}.png"
caminho_saída_grafico2 = f"/content/drive/MyDrive/Colab Notebooks/Ad/output/gráfico2_{ano}.png"

from typing import AsyncContextManager
import pandas as pd
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '`{:.2f}'.format)

# Lendo os dados

df_viagens = pd.read_csv(caminho_dados, encoding="Windows-1252", sep=";", decimal=",")

# Criando coluna de despesas

df_viagens['Despesas'] = df_viagens['Valor diárias'] + df_viagens['Valor passagens'] + df_viagens['Valor outros gastos']

# ajustando valores nulos para os cargos
df_viagens['Cargo'] = df_viagens['Cargo'].fillna("NÃO IDENTIFICADO")

# Convertendo colunas de datas
df_viagens["Período - Data de início"] = pd.to_datetime(df_viagens["Período - Data de início"], format="%d/%m/%Y")
df_viagens["Período - Data de fim"] = pd.to_datetime(df_viagens["Período - Data de fim"], format="%d/%m/%Y")

# Criando novas colunas de datas

## alterando para nome do mês
df_viagens['Mês da viagem'] = df_viagens['Período - Data de início'].dt.month_name()

## dias que duraram a viagem
df_viagens['Dias de viagem'] = (df_viagens['Período - Data de fim'] - df_viagens['Período - Data de início']).dt.days

# Criando a tabela consolidada

df_viagens_consolidado = (
  df_viagens
 .groupby("Cargo")
 .agg(
     despesa_media=('Despesas', 'mean'),
     duracao_media = ('Dias de viagem', 'mean'),
     despesas_totais=('Despesas', 'sum'),
     destino_mais_frequentes=("Destinos",pd.Series.mode), #pd.Series.mode calcula a função Moda
     n_viagens=('Nome', 'count')
     )
 .reset_index()
 .sort_values(by='despesas_totais', ascending=False)
 )

# Filtrando a tabela consolidada por cargos relevantes (>1% das viagens)
df_cargos = df_viagens['Cargo'].value_counts(normalize=True).reset_index()
cargos_relevantes = df_cargos.loc[df_cargos['proportion']>0.01, 'Cargo']
filtro = df_viagens_consolidado['Cargo'].isin(cargos_relevantes) #isin está dentro da tabela cargos relevantes

#Chegando na tabela final - consolidada e filtrada
df_final = df_viagens_consolidado[filtro].sort_values(by='n_viagens', ascending=False)

#Salvando a tabela final
df_final.to_excel(caminho_saída_tabela, index=False)

# Gráfico de Número de Viagens por Cargo

fig, ax = plt.subplots(figsize=(16, 6))
ax.barh(df_final['Cargo'], df_final['n_viagens'], color="#49deac" )
ax.invert_yaxis()
ax.set_facecolor('#3b3b47')
fig.suptitle(f'Viagens por cargo público {ano}')
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.figtext(0.75, 0.89, 'Fonte: Portal da Transparência', fontsize=(8))
plt.yticks(fontsize=8)
plt.xlabel('Número de Viagens')

plt.savefig(caminho_saída_grafico1, bbox_inches='tight')

# Gráfico de Despesa Média por Cargo Público

fig, ax = plt.subplots(figsize=(16, 6))
ax.barh(df_final['Cargo'], df_final['despesa_media'], color="#49deac" )
ax.invert_yaxis()
ax.set_facecolor('#3b3b47')
fig.suptitle(f'Despesa Média por cargo público {ano}')
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.figtext(0.75, 0.89, 'Fonte: Portal da Transparência', fontsize=(8))
plt.yticks(fontsize=8)
plt.xlabel('Despesa Média')

plt.savefig(caminho_saída_grafico2, bbox_inches='tight')
