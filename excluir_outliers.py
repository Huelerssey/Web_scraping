import pandas as pd

# Carregar o arquivo Excel
df = pd.read_excel(
    r"C:\Data Science\web_scraping\retificacao_manual\Parnamirim_RN.xlsx"
)

# Remover as linhas com outliers
df = df[
    (df["Preço"] <= 1000000)
    & (df["Quartos"] != 0)
    & (df["Banheiros"] != 0)
    & (df["Garagem"] <= 4)
]

# Salvar o DataFrame atualizado em um novo arquivo Excel
df.to_excel(
    r"C:\Data Science\web_scraping\dataset_final\Parnamirim_RN_Final.xlsx", index=False
)

print("Arquivo atualizado salvo com sucesso.")
