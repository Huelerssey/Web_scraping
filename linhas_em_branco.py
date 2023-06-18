import pandas as pd

# Ler o arquivo Excel
df = pd.read_excel(r"C:\Data Science\web_scraping\imoveis_prn.xlsx")

# Deletar as linhas com valores nulos em qualquer coluna
df = df.dropna()

# Salvar o DataFrame em um novo arquivo Excel
df.to_excel(
    r"C:\Data Science\web_scraping\linhas_em_branco_deletadas\imoveis_prn_tratados.xlsx",
    index=False,
)
