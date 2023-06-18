import pandas as pd
import time
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor


# 1 -> Entendimento da Área/Empresa

"""
O modelo de previsão a baixo tem como objetivo utilizar machine learning para prever o preço de um imóvel na região de Natal/Parnamirim, dadas as caracteristicas de um imóvel
sendo elas disponíveis para análise:
 - Preço
 - Área
 - Quartos
 - Garagem
 - Banheiros
 - Cep
"""

# 2 -> Extração/Obtenção de dados

"""
Os dados deste dataframe são um resultado de web scraping, retirando informações do site: www.zapimoveis.com.br minimamente tratadas no processo.
"""

# Criando o dataframe
tabela1 = pd.read_excel(r'C:\Data Science\Web_scraping\dataset_final_pq\Natal_RN_Final.xlsx')
tabela2 = pd.read_excel(r'C:\Data Science\Web_scraping\dataset_final_pq\Parnamirim_RN_Final.xlsx')
tabela = pd.concat([tabela1, tabela2])

# 3 -> Data Cleaning

#print(tabela.dtypes)
"""
Atualmente nossa tabela possui os seguintes tipos:
Preço         int64
Área         object
Quartos       int64
Garagem       int64
Banheiros     int64
Bairro       object
Cidade       object
Estado       object
País         object
Cep          object

Será necessário transformar Área e Cep no tipo int para adiciona-la a análise.
O que indentificava essas colunas como texto era o hífen ("-") descrevendo 45 - 65,
e o "m²". Então, vamos remover eles.
"""

# Função para extrair o primeiro valor antes do hífen
def extrair_primeiro_valor(value):
    if '-' in value:
        return value.split('-')[0].strip()
    else:
        return value

# Apaga a string "m²" do valor
tabela['Área'] = tabela['Área'].str.replace('m²', '')

# Aplica a função na coluna de área
tabela['Área'] = tabela['Área'].apply(extrair_primeiro_valor)

# Trasnforma a coluna Área em int
tabela['Área'] = tabela['Área'].astype('int64')

# Apaga a string "-" do Cep
tabela['Cep'] = tabela['Cep'].str.replace('-', '')

# Trasnforma a coluna Cep em int
tabela['Cep'] = tabela['Cep'].astype('int64')

# Realizar one-hot encoding na coluna 'Bairro'
tabela = pd.get_dummies(tabela, columns=['Bairro'])

# Excluir colunas irrelevantes para análise
tabela = tabela.drop(columns=['Cidade', 'Estado', 'País', 'Cep'])

# 4 -> Análise exploratória e tratamento de outliers

# print(tabela.corr()['Preço'])
# Preço        1.000000
# Área         0.090506
# Quartos      0.473679
# Garagem      0.510230
# Banheiros    0.634200
# Cep          0.054930


# correlation = tabela.corr()[['Preço']]
# correlation_sorted = correlation.sort_values(by='Preço', ascending=False)
# sns.heatmap(correlation_sorted, cmap="Blues", annot=True, fmt='.0%')
# plt.show()

"""
Percebemos que a coluna de banheiros possui forte corelação com o preço e a coluna
Área e Cep quase não impactam no preço.
"""

# Funções para análises e exclusão de outliers
def limites(coluna):
    """retorna o limite inferior e o limite superior"""
    q1 = coluna.quantile(0.25)
    q3 = coluna.quantile(0.75)
    amplitude = q3 - q1
    return (q1 - 1.5 * amplitude, q3 + 1.5 * amplitude)

def excluir_outliers(df, nome_coluna):
    """Exclui outliers e retorna o novo dataframe e também a quantidade de linhas removidas"""
    qtde_linhas = df.shape[0]
    lim_inf, lim_sup = limites(df[nome_coluna])
    df = df.loc[(df[nome_coluna] >= lim_inf) & (df[nome_coluna] <= lim_sup), : ]
    linhas_removidas = qtde_linhas - df.shape[0]
    return df, linhas_removidas

# Demonstra os valores do limite inferior e superior
# limites_colunas = tabela.apply(limites)
# print(limites_colunas)
#        Preço   Área  Quartos  Garagem  Banheiros
# 0  -283012.5  -59.0      0.5     -0.5        0.5
# 1  1117007.5  253.0      4.5      3.5        4.5

# Excluir outliers na coluna 'Preço'
tabela, linhas_removidas = excluir_outliers(tabela, 'Preço')
#print(f'{linhas_removidas} linhas removidas da coluna Preço')

# Visualização dos valores dos imóveis em um histograma
# plt.figure(figsize=(8, 6))
# plt.hist(tabela['Preço'], bins=20)
# plt.xlabel('Preço')
# plt.ylabel('Frequência')
# plt.title('Distribuição dos valores dos imóveis')
# plt.show()

# Visualização dos valores dos imóveis em um boxplot
# plt.figure(figsize=(8, 6))
# plt.boxplot(tabela['Preço'])
# plt.ylabel('Preço')
# plt.title('Boxplot dos valores dos imóveis')
# plt.show()

# tabela = tabela.loc[(tabela['Preço'] > 200000) & (tabela['Preço'] < 600000)]

# Excluir outliers na coluna 'Área"
tabela, linhas_removidas = excluir_outliers(tabela, 'Área')
#print(f'{linhas_removidas} linhas removidas da coluna Área')

# Visualização dos valores das Áreas em um histograma
# plt.figure(figsize=(8, 6))
# plt.hist(tabela['Área'], bins=20)
# plt.xlabel('Área')
# plt.ylabel('Frequência')
# plt.title('Distribuição dos valores das Áreas')
# plt.show()

# Visualização dos valores das Áreas em um boxplot
# plt.figure(figsize=(8, 6))
# plt.boxplot(tabela['Área'])
# plt.ylabel('Área')
# plt.title('Boxplot dos valores das Áreas')
# plt.show()

tabela = tabela.loc[(tabela['Área'] >= 50) & (tabela['Área'] <= 200)]

# Excluir outliers na coluna 'Quartos'
tabela, linhas_removidas = excluir_outliers(tabela, 'Quartos')
#print(f'{linhas_removidas} linhas removidas da coluna Quartos')

# Visualização dos valores dos quartos em um histograma
# plt.figure(figsize=(8, 6))
# plt.hist(tabela['Quartos'], bins=20)
# plt.xlabel('Quartos')
# plt.ylabel('Frequência')
# plt.title('Distribuição dos valores dos quartos')
# plt.show()

# Visualização dos valores dos quartos em um boxplot
# plt.figure(figsize=(8, 6))
# plt.boxplot(tabela['Quartos'])
# plt.ylabel('Quartos')
# plt.title('Boxplot dos valores dos quartos')
# plt.show()

# Excluir outliers na coluna 'Garagem'
tabela, linhas_removidas = excluir_outliers(tabela, 'Garagem')
#print(f'{linhas_removidas} linhas removidas da coluna Garagem')

# Visualização dos valores das garagens em um histograma
# plt.figure(figsize=(8, 6))
# plt.hist(tabela['Garagem'], bins=20)
# plt.xlabel('Garagem')
# plt.ylabel('Frequência')
# plt.title('Distribuição dos valores das garagens')
# plt.show()

# Visualização dos valores das garagens em um boxplot
# plt.figure(figsize=(8, 6))
# plt.boxplot(tabela['Garagem'])
# plt.ylabel('Garagem')
# plt.title('Boxplot dos valores das garagens')
# plt.show()

# tabela = tabela.loc[(tabela['Garagem'] >= 1) & (tabela['Garagem'] <= 2)]

# Excluir outliers na coluna 'Banheiros'
tabela, linhas_removidas = excluir_outliers(tabela, 'Banheiros')
#print(f'{linhas_removidas} linhas removidas da coluna Banheiros')

# Visualização dos valores dos banheiros em um histograma
# plt.figure(figsize=(8, 6))
# plt.hist(tabela['Banheiros'], bins=20)
# plt.xlabel('Banheiros')
# plt.ylabel('Frequência')
# plt.title('Distribuição dos valores dos banheiros')
# plt.show()

# Visualização dos banheiros em um boxplot
# plt.figure(figsize=(8, 6))
# plt.boxplot(tabela['Banheiros'])
# plt.ylabel('Banheiros')
# plt.title('Boxplot dos numeros de banheiros')
# plt.show()

# tabela = tabela.loc[(tabela['Banheiros'] >= 1) & (tabela['Banheiros'] <= 3)]

# 5 -> Modelagem e Algoritmos

# Representa a coluna de previsão
y = tabela['Preço']

# Representa as colunas de treino
x = tabela.drop('Preço', axis=1)

# Função auxiliar para avaliar o melhor modelo
def avaliar_modelo(nome_modelo, y_teste, previsao):
    tempo_inicial = time.time()
    r2 = r2_score(y_teste, previsao)
    rsme = np.sqrt(mean_squared_error(y_teste, previsao))
    mae = mean_absolute_error(y_teste, previsao)
    mape = np.mean(np.abs((y_teste - previsao) / y_teste)) * 100
    tempo_final = time.time()
    tempo_execucao = tempo_final - tempo_inicial
    return f'MODELO: {nome_modelo}\nR²: {r2:.2%}\nRSME: {rsme:.2f}\nMAE: {mae:.2f}\nMAPE: {mape:.2f}%\nTEMPO: {tempo_execucao:.2f}'

# Função que divide a base de dados
x_treino, x_teste, y_treino, y_teste = train_test_split(x, y, test_size=0.1, random_state=20)

# Lista de modelos
modelos = [
    ('RegressaoLinear', LinearRegression()),
    ('RandomForest', RandomForestRegressor()),
]

# Treinamento, teste e avaliação dos modelos
for nome_modelo, modelo in modelos:
    # Treina o modelo
    modelo.fit(x_treino, y_treino)
    
    # Testa o modelo
    previsao = modelo.predict(x_teste)
    
    # Avalia o modelo
    print(avaliar_modelo(nome_modelo, y_teste, previsao))
    print('-' * 50)

"""
MODELO: RegressaoLinear
R²: 45.40%
RSME: 169725.32
TEMPO: 0.00
--------------------------------------------------
MODELO: RandomForest
R²: 56.41%
RSME: 151654.04
TEMPO: 0.00
--------------------------------------------------
MODELO: ExtraTrees
R²: 50.20%
RSME: 162089.01
TEMPO: 0.00
--------------------------------------------------
MODELO: GradientBoosting
R²: 56.90%
RSME: 150795.01
TEMPO: 0.00
--------------------------------------------------
MODELO: Ridge
R²: 45.40%
RSME: 169725.31
TEMPO: 0.00
--------------------------------------------------
MODELO: ElasticNet
R²: 42.17%
RSME: 174681.63
TEMPO: 0.00
--------------------------------------------------

Com a abordagem atual, percebemos que nenhum dos modelos consegue obter uma precisão
significativa para prever preços. Então, ajustes e melhorias foram aplicadas no modelo, como adição da coluna de cep,
Área, ecooding da coluna bairro, tamanho da amostra de treino/test e aumento na quantidade de dados no dataset.

Mesmo com todas as alterações no dataset o modelo que teve melhor performance foi:
MODELO: RandomForest
R²: 74.18%
RSME: 109968.86
MAE: 73659.17
MAPE: 29.05%
TEMPO: 0.00

A hipótese mais provável é que os preços dos imóveis podem ter uma grande variabilidade, 
mesmo para imóveis semelhantes. Isso pode ser causado por fatores externos e
difíceis de capturar no modelo, como preferências pessoais dos compradores,
negociações individuais, entre outros. 
Essa variabilidade torna dificil obter um modelo que preveja com precisão os preços 
dos imóveis em todos os casos.
Com os dados disponíveis o máximo de precisão atingida foi de 75%
tornando a utilização deste modelo inviável. Seria necessário a obtenção de mais caracteristicas
nas quais podem descrever o preço de um imóvel na qual o site não fornece.
"""

# 6 -> Resultados, ajustes finais e deploy da aplicação

# Ia escolhida
modelo_arvoredecisao = RandomForestRegressor()

# Ia treinada
modelo_arvoredecisao.fit(x_treino, y_treino)

# Plota um gráfico com as importancias que cada coluna exerce
# importancia_features = pd.DataFrame(modelo_arvoredecisao.feature_importances_, x_treino.columns)
# importancia_features = importancia_features.sort_values(by=0, ascending=False)

# plt.figure(figsize=(15, 5))
# ax = sns.barplot(x=importancia_features.index, y=importancia_features[0])
# ax.tick_params(axis='x', rotation=90)
# plt.show()

# Previsão da Ia
# print(x.columns)
# ['Área', 'Quartos', 'Garagem', 'Banheiros', 'Bairro']
