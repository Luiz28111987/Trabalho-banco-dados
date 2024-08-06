import pandas as pd
from sqlalchemy import create_engine

# Caminho completo para o arquivo
file_path = "C:/Users/Luiz/Desktop/Estudos/Trabalho-banco-dados/CONTROLE_ENTREGA_JULHO_2024_MOTORISTAS.xlsx"

# Cabeçalho personalizado para o DataFrame
cabecalho = ['MOTORISTA','Placa','Data_Entrega','Hora_Saida','KM_Inicial',
             'Quantidade_Notas_Fiscais','Quantidade_Coletas','KM_Final','TOTAL_DIA','REGIAO']

# Verifica se o arquivo existe no caminho especificado
try:
    df = pd.read_excel(file_path,skiprows=1, header=None, names=cabecalho)
except FileNotFoundError as e:
    print(f"Erro: {e}")
    df = pd.DataFrame()  # cria um DataFrame vazio para evitar erros subsequentes

# Formatar a data para outro formato ( 08/11/2018 - 2018/11/08)
df['Data_Entrega'] = pd.to_datetime(df['Data_Entrega'], format='%d/%m/%Y').dt.strftime('%Y/%m/%d')
df['Data_Entrega'] = pd.to_datetime(df['Data_Entrega'])

# Extrair apenas a data (sem a parte do tempo)
df['Data_Entrega'] = df['Data_Entrega'].dt.date

# Preenchemos o valor NA por ( 0 )
# inplace = True / para altera o proprio DataFrame
dado = 0
df['Quantidade_Coletas'] = df['Quantidade_Coletas'].fillna(value = dado)

# Convertendo uma única coluna para inteiro
df['Quantidade_Coletas'] = df['Quantidade_Coletas'].astype(int)

df['Quantidade_Notas_Fiscais'] = df['Quantidade_Notas_Fiscais'].fillna(value = dado)

# Convertendo uma única coluna para inteiro
df['Quantidade_Notas_Fiscais'] = df['Quantidade_Notas_Fiscais'].astype(int)

# Substituindo nomes das regiões
df['REGIAO'] = df['REGIAO'].str.replace('SOB', 'SOBRADINHO')
df['REGIAO'] = df['REGIAO'].str.replace('PLANA-DF', 'PLANALTINA-DF')
df['REGIAO'] = df['REGIAO'].str.replace('VICENTE P', 'VICENTE PIRES')
df['REGIAO'] = df['REGIAO'].str.replace('CEI', 'CEILANDIA')
df['REGIAO'] = df['REGIAO'].str.replace('PARQUE W', 'PARK WAY')
df['REGIAO'] = df['REGIAO'].str.replace('CIDADE O', 'CIDADE OCIDENTAL')
df['REGIAO'] = df['REGIAO'].str.replace('TAGUA-SUL', 'TAGUATINGA-SUL')
df['REGIAO'] = df['REGIAO'].str.replace('S SEB', 'SAO SEBASTIAO')
df['REGIAO'] = df['REGIAO'].str.replace('SAI', 'SIA')
df['REGIAO'] = df['REGIAO'].str.replace('SANTA M', 'SANTA MARIA')
df['REGIAO'] = df['REGIAO'].str.replace('RIACHO F', 'RIACHO FUNDO')
df['REGIAO'] = df['REGIAO'].str.replace('PLANA-GO', 'PLANALTINA-GO')
df['REGIAO'] = df['REGIAO'].str.replace('BRASLÂNDIA', 'BRAZLANDIA')
df['REGIAO'] = df['REGIAO'].str.replace('TAGUA-NORTE', 'TAGUATINGA-NORTE')
df['REGIAO'] = df['REGIAO'].str.replace('V PIRES', 'VICENTE PIRES')
df['REGIAO'] = df['REGIAO'].str.replace('A LINDAS', 'AGUAS LINDAS')
df['REGIAO'] = df['REGIAO'].str.replace('TAGUA NORTE', 'TAGUATINGA-NORTE')
df['REGIAO'] = df['REGIAO'].str.replace('PLANALTINA-DF-GO', 'PLANALTINA-DF/PLANLTINA-GO')
df['REGIAO'] = df['REGIAO'].str.replace('CANDANGO', 'CANDANGOLANDIA')
df['REGIAO'] = df['REGIAO'].str.replace('CANDANGA', 'CANDANGOLANDIA')
df['REGIAO'] = df['REGIAO'].str.replace('NUCLEO B', 'NUCLEO BANDEIRANTE')
df['REGIAO'] = df['REGIAO'].str.replace('SICIA', 'SCIA')
df['REGIAO'] = df['REGIAO'].str.replace('VAL', 'VALPARAISO-GO')
df['REGIAO'] = df['REGIAO'].str.replace('SOF-NORTE-SUL', 'SOF-NORTE/SOF-SUL')
df['REGIAO'] = df['REGIAO'].str.replace('TAGUATINGA-NORTE-SUL', 'TAGUATINGA-NORTE/TAGUATINGA-SUL')
df['REGIAO'] = df['REGIAO'].str.replace('CIDADE A', 'CIDADE DO AUTOMOVEL')

# Obtendo os valores únicos
# unique_names = df['REGIAO'].unique()

# print(unique_names)

# Divida a Coluna em Listas
df['REGIAO'] = df['REGIAO'].str.split('/')

# Transformar Listas em Linhas Separadas
df_exploded = df.explode('REGIAO')

# Remova Espaços em Branco Extras
df_exploded['REGIAO'] = df_exploded['REGIAO'].str.strip()

print(df_exploded)

"""
try:
    # Criar uma conexão com o banco de dados PostgreSQL
    engine = create_engine('postgresql://postgres:1234@localhost:5432/trabalho_extensao')

    # Importar dados para a tabela
    df.to_sql('dados', engine, if_exists='append', index=False)
    print("Dados importados com sucesso.")

except Exception as e:
    print(f"Erro ao conectar ao banco de dados ou importar dados: {e}")

"""