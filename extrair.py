import requests
from bs4 import BeautifulSoup
import pandas as pd


def extrair_dados_pagina(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    anuncios = soup.find_all("div", class_="simple-card__box")

    dados_imoveis = []
    for anuncio in anuncios:
        preco_element = anuncio.find("p", class_="simple-card__price")
        if preco_element:
            preco = preco_element.text.strip()
        else:
            preco = ""

        area_element = anuncio.find("li", class_="js-areas")
        if area_element:
            area = area_element.text.strip().split("\n")[-1].strip()
        else:
            area = ""

        quartos_element = anuncio.find("li", class_="js-bedrooms")
        if quartos_element:
            quartos = quartos_element.text.strip().split("\n")[-1].strip()
        else:
            quartos = ""

        garagem_element = anuncio.find("li", class_="js-parking-spaces")
        if garagem_element:
            garagem = garagem_element.text.strip().split("\n")[-1].strip()
        else:
            garagem = ""

        banheiros_element = anuncio.find("li", class_="js-bathrooms")
        if banheiros_element:
            banheiros = banheiros_element.text.strip().split("\n")[-1].strip()
        else:
            banheiros = ""

        endereco_element = anuncio.find("h2", class_="simple-card__address")
        if endereco_element:
            endereco = endereco_element.text.strip()
        else:
            endereco = ""

        dados_imoveis.append([preco, area, quartos, garagem, banheiros, endereco])

    return dados_imoveis


def salvar_excel(dados, nome_arquivo):
    df = pd.DataFrame(
        dados, columns=["Preço", "Área", "Quartos", "Garagem", "Banheiros", "Endereço"]
    )
    df.to_excel(nome_arquivo, index=False)
    print(f'Arquivo "{nome_arquivo}" salvo com sucesso.')


# URL do site com a primeira página
base_url = "https://www.zapimoveis.com.br/venda/imoveis/rn+natal/?onde=,Rio%20Grande%20do%20Norte,Natal,,,,,city,BR>Rio%20Grande%20do%20Norte>NULL>Natal,-5.924287,-35.26639,&transacao=Venda&tipo=Imóvel%20usado&pagina="

dados_totais = []

for pagina in range(1, 101):  # Extrai os dados das 3 primeiras páginas (1 a 3)
    url = base_url + str(pagina)
    dados_pagina = extrair_dados_pagina(url)
    dados_totais.extend(dados_pagina)

# Salvar os dados em um arquivo Excel
salvar_excel(dados_totais, "imoveis_nt.xlsx")
