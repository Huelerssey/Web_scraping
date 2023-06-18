import pandas as pd
from geopy.geocoders import GoogleV3

# Inicialize o geocodificador
geolocator = GoogleV3(api_key='AIzaSyBCdXQweuLK7xr9K0wCFv6LvXv7xSGYXnA')

# Lista dos bairros de Natal
bairros = [
    'Lagoa Nova',
    'Tirol',
    'Ponta Negra',
    'Mãe Luíza',
    'Capim Macio',
    'Barro Vermelho',
    'Petrópolis',
    'Pajuçara',
    'Lagoa Seca',
    'Neópolis',
    'Candelária',
    'Nossa Senhora De Nazaré',
    'Nova Descoberta',
    'Cidade Alta',
    'Nordeste',
    'Rocas',
    'Dix-Sept Rosado',
    'Alecrim',
    'Cidade Da Esperança',
    'Nossa Senhora Da Apresentação',
    'Praia Do Meio',
    'Potengi',
    'Pirangi',
    'Pitimbu',
    'Ribeira',
    'Lagoa Azul',
    'Areia Preta',
    'Planalto',
    'Felipe Camarão',
    'Redinha',
    'Cidade Verde',
    'Cidade Nova',
    'Cidade Satelite',
    'Igapó',
    'Santos Reis',
    'Morro Branco',
    'Centro',
    'Quintas',
    'Parque Das Colinas',
    'Potilandia',
    'Zona Norte',
    'San Vale',
    'Cidade Jardim',
    'Guarapés',
    'Bom Pastor',
    'Liberdade',
    'Alagamar'
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
caminho_arquivo = r'C:\Data Science\Web_scraping\dataset_final_pq\Natal_RN_Final.xlsx'

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
Lagoa Nova: 59064-741
Tirol: 59015-145
Ponta Negra: 59090-260
Mãe Luíza: 59014-680
Capim Macio: 59078-400
Barro Vermelho: 59022-110
Petrópolis: 59012-310
Pajuçara: 59133-280
Lagoa Seca: 59031-080
Neópolis: 59088-010
Candelária: 59065-150
Nossa Senhora De Nazaré: 59060-200
Nova Descoberta: 59056-125
Cidade Alta: 59025-330
Nordeste: 59020-030
Rocas: 59010-250
Dix-Sept Rosado: 59056-425
Alecrim: 59031-270
Cidade Da Esperança: 59070-510
Nossa Senhora Da Apresentação: 59114-246
Praia Do Meio: 59010-030
Potengi: 59120-000
Pirangi: 59088-050
Pitimbu: 59068-450
Ribeira: 59012-180
Lagoa Azul: 59138-600
Areia Preta: 59014-060
Planalto: 59074-827
Felipe Camarão: 59074-626
Redinha: 59122-170
Cidade Verde: 59123-690
Cidade Nova: 59072-500
Cidade Satelite: 59067-425
Igapó: 59104-300
Santos Reis: 59010-000
Morro Branco: 59056-425
Centro: 59020-030
Quintas: 59040-000
Parque Das Colinas: 59066-080
Potilandia: 59076-680
Zona Norte: 59020-030
San Vale: 59068-450
Cidade Jardim: 59078-600
Guarapés: 59074-752
Bom Pastor: 59062-330
Liberdade: 59150-080
Alagamar: 59575-000
"""