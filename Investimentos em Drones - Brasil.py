import pandas as pd

import matplotlib.pyplot as plt


df = pd.read_csv('notas-fiscais - drone.csv', sep=';', encoding='utf-8') 

# Verificar os nomes das colunas
print(df.columns)

# Substituir o nome 'Ministério da Defesa - Unidades com vínculo direto' na coluna 'ÓRGÃO DESTINATÁRIO'
df['ÓRGÃO DESTINATÁRIO'] = df['ÓRGÃO DESTINATÁRIO'].replace('Ministério da Defesa - Unidades com vínculo direto', 'Ministério da Defesa')


# Remover pontos de milhar e substituir vírgulas por pontos decimais
df['VALOR DA NOTA (R$)'] = df['VALOR DA NOTA (R$)'].replace({'\.': '', ',': '.'}, regex=True).astype(float)


# Somar os valores da coluna 'VALOR DA NOTA (R$)'
df_soma = df['VALOR DA NOTA (R$)'].sum()
print(df_soma)

# Converter a coluna 'DATA DA EMISSÃO' para datetime
df['DATA DA EMISSÃO'] = pd.to_datetime(df['DATA DA EMISSÃO'], format='%d/%m/%Y')

# Extrair o ano da coluna 'DATA DA EMISSÃO'
df['ANO'] = df['DATA DA EMISSÃO'].dt.year


# Agrupar por ano e somar os valores
df_agrupado = df.groupby('ANO')['VALOR DA NOTA (R$)'].sum()
print(df_agrupado)


# Criar o gráfico
plt.figure(figsize=(10, 6))
df_agrupado.plot(kind='bar', color='skyblue')
plt.title('Somatório dos Valores das Notas por Ano')
plt.xlabel('Ano')
plt.ylabel('Somatório dos Valores das Notas (R$)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Mostrar o gráfico
plt.show()

# Filtrando os dados onde 'ORGÃO SUPERIOR DESTINATÁRIO' é igual a 'Ministério da Defesa'
df_superior_destinatario = df.loc[df['ORGÃO SUPERIOR DESTINATÁRIO'] == 'Ministério da Defesa']
df_destinatario = df_superior_destinatario.groupby('ÓRGÃO DESTINATÁRIO')['VALOR DA NOTA (R$)'].sum()
print(df_destinatario)

# Criando Gráfico para o Destinatário
plt.figure(figsize=(10, 6))
df_destinatario.plot(kind='bar', color='skyblue')
plt.title('Maiores Investimentos')
plt.xlabel('Orgãos')
plt.ylabel('Somatório dos Valores (R$)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Mostrar o gráfico
plt.show()

#print(df.columns)

# Filtrar os municípios dos fornecedores com valores acima de 100.000
df_fornecedor = df[df['VALOR DA NOTA (R$)'] > 200_000]

# Agrupar por município e somar os valores
df_agrupado_municipio = df_fornecedor.groupby('MUNICÍPIO DO FORNECEDOR')['VALOR DA NOTA (R$)'].sum()

# Ordenar do maior para o menor
df_agrupado_municipio = df_agrupado_municipio.sort_values(ascending=False)
print(df_agrupado_municipio)

# print(df_agrupado_municipio.shape)

# Criando Gráfico para os Fornecedores
plt.figure(figsize=(10, 10))
df_agrupado_municipio.plot(kind='bar', color='skyblue')
plt.title('Municípios Fornecedores Acima de R$200.000')
plt.xlabel('Municípios')
plt.ylabel('Somatório dos Valores (R$)')
plt.xticks(rotation=90)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Mostrar o gráfico
plt.show()