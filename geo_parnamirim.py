import pandas as pd
from geopy.geocoders import GoogleV3

# Inicialize o geocodificador
geolocator = GoogleV3(api_key='AIzaSyBCdXQweuLK7xr9K0wCFv6LvXv7xSGYXnA')

# Lista dos bairros de Natal
bairros = [
    'Nova Parnamirim',
    'Parque das Nações',
    'Liberdade',
    'Parque de Exposições',
    'Pirangi do Norte',
    'Passagem de Areia',
    'Emaús',
    'Pium',
    'Cotovelo',
    'Cajupiranga',
    'Parque das Árvores',
    'Nova Esperança',
    'Vida Nova',
    'Centro',
    'Rosa dos Ventos',
    'Vale do Sol',
    'Cohabinal',
    'Praia de Pirangi',
    'Bela Parnamirim',
    'Cidade Verde',
    'Parque Do Jiqui',
    'Monte Castelo',
    'Jardim Planalto',
    'Santa Tereza',
    'Boa Esperança',
    'Encanto Verde',
    'Parque dos Eucaliptos',
    'Santos Reis',
    'Joquey Club',
    'Conjunto Cophab',
    'Praia de Cotovelo',
    'Bela Vista'
]

# Dicionário para armazenar os pares bairro -> CEP
bairros_cep = {}

# Obtenha o CEP para cada bairro
for bairro in bairros:
    try:
        # Geocode do bairro para obter as coordenadas
        location = geolocator.geocode(bairro + ', Natal, RN, Brasil')

        # Geocode reverso para obter o endereço completo
        address = geolocator.reverse((location.latitude, location.longitude))

        # Obtenha o CEP do endereço completo
        cep = address.raw['address_components'][-1]['long_name']

        # Adicione o par bairro -> CEP ao dicionário
        bairros_cep[bairro] = cep

    except Exception as e:
        print(f'Erro ao obter CEP para o bairro {bairro}: {str(e)}')

# Imprima os pares bairro -> CEP
# for bairro, cep in bairros_cep.items():
#     print(f'{bairro}: {cep}')

# Caminho para o arquivo Excel
caminho_arquivo = r'C:\Data Science\Web_scraping\dataset_final_pq\Parnamirim_RN_Final.xlsx'

# Carregar o arquivo Excel como um DataFrame
df = pd.read_excel(caminho_arquivo)

# Adicionar a coluna de CEP ao DataFrame com base no dicionário de bairros e CEPs
df['CEP'] = df['Bairro'].map(bairros_cep)

# Salvar o DataFrame atualizado de volta no arquivo Excel
with pd.ExcelWriter(caminho_arquivo, mode='a', engine='openpyxl') as writer:
    df.to_excel(writer, index=False)
    writer.book.active = writer.book.sheetnames.index('novo_dataset')  # Substitua 'Sheet1' pelo nome da planilha que deseja definir como ativa

print("Coluna de CEP adicionada com sucesso!")

"""
Resultado:
Nova Parnamirim: 59151-902
Parque das Nações: 59158-182
Liberdade: 59150-080
Parque de Exposições: 59146-640
Pirangi do Norte: 59161-250
Passagem de Areia: 59145-060
Emaús: 59149-260
Pium: 59160-390
Cotovelo: 59161-180
Cajupiranga: 59042-530
Parque das Árvores: 59154-000
Nova Esperança: 59074-380
Vida Nova: 59020-030
Centro: 59020-030
Rosa dos Ventos: 59140-971
Vale do Sol: 59153-150
Cohabinal: 59140-680
Praia de Pirangi: 59151-440
Bela Parnamirim: 59140-971
Cidade Verde: 59123-690
Parque Do Jiqui: 59153-210
Monte Castelo: 59112-160
Jardim Planalto: 59155-230
Santa Tereza: 59073-152
Boa Esperança: 59020-030
Encanto Verde: 59114-340
Parque dos Eucaliptos: 59140-971
Santos Reis: 59010-000
Joquey Club: 59020-030
Conjunto Cophab: 59025-290
Praia de Cotovelo: 59161-175
Bela Vista: 59073-156
"""