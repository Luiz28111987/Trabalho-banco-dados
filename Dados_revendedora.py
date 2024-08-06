import pandas as pd
from sqlalchemy import create_engine

# Caminho completo para o arquivo
file_path = "C:/Users/Luiz/Desktop/Estudos/Python_projetos/Projeto_revendas/trabalho.txt"

# Cabeçalho personalizado para o DataFrame
cabecalho = ['regiao_sigla','estado_sigla','municipio','revenda','cnpj_da_revenda',
             'produto','data_da_coleta','valor_de_venda','valor_de_compra','unidade_de_medida','bandeira']

# Verifica se o arquivo existe no caminho especificado
try:
    df = pd.read_csv(file_path, sep='\t', encoding='utf-16', header=None, names=cabecalho)
except FileNotFoundError as e:
    print(f"Erro: {e}")
    df = pd.DataFrame()  # cria um DataFrame vazio para evitar erros subsequentes

# Substituindo os caracteres da coluna Unidade_de_Medida
df.loc[:,'unidade_de_medida'] = df['unidade_de_medida'].str.replace('R$ / litro', 'L', regex=False)

# Substituir vírgulas por pontos e converter a coluna para float ( Valor_de_Venda e Valor_de_Compra )
df['valor_de_venda'] = df['valor_de_venda'].str.replace(',', '.').astype(float)
df['valor_de_compra'] = df['valor_de_compra'].str.replace(',', '.').astype(float)

# Formatar a data para outro formato ( 08/11/2018 - 2018/11/08)
df['data_da_coleta'] = pd.to_datetime(df['data_da_coleta'], format='%d/%m/%Y').dt.strftime('%Y/%m/%d')
df['data_da_coleta'] = pd.to_datetime(df['data_da_coleta'])

# Extrair apenas a data (sem a parte do tempo)
df['data_da_coleta'] = df['data_da_coleta'].dt.date

# Preenchemos o valor NA por ( 0.00 )
# inplace = True / para altera o proprio DataFrame
dado = 0.00
df['valor_de_compra'] = df['valor_de_compra'].fillna(value = dado)

# Converter a coluna CNPJ para string e remover a notação científica
df.loc[:,'cnpj_da_revenda'] = df['cnpj_da_revenda'].astype(str).str.replace('[^\\d]+','', regex=True).astype(float).astype(str).str.zfill(14)

# Removendo o .0 do final dos números
df.loc[:,'cnpj_da_revenda'] = df['cnpj_da_revenda'].str.replace(r'\.0$', '', regex=True)

####  a partir daqui começa a putaria 

# Verifica se o DataFrame está vazio
if not df.empty:
    # Função para verificar espaços em branco no início ou no final das strings
    def verifica_espacos(x):
        if isinstance(x, str):
            return x.startswith(' ') or x.endswith(' ')
        return False

    # Verificar espaços em branco em cada coluna usando map e apply
    espacos_em_branco = df.apply(lambda col: col.map(verifica_espacos))

    # Filtrar o DataFrame para exibir apenas as células com espaços em branco
    celulas_com_espacos = df[espacos_em_branco.any(axis=1)]

    if not celulas_com_espacos.empty:
        # Tratamento de espaços em branco        
        print("Células com espaços em branco foram encontradas.")
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    else:
        print("Não existem células com espaços!")
else:
    print("O DataFrame está vazio. Verifique o caminho do arquivo e o conteúdo do arquivo.")

# Remover pontos e vírgulas no início dos dados da coluna 'dados'
df['revenda'] = df['revenda'].str.lstrip('.,;"')

# Remover pontos e vírgulas do início e do final dos dados da coluna 'dados'
df['revenda'] = df['revenda'].str.strip('.,;"')

# Imprimindo amostra do DataFrame
print(df.head())

# Informações DataFrame
df.info()

try:
    # Criar uma conexão com o banco de dados PostgreSQL
    engine = create_engine('postgresql://postgres:1234@localhost:5432/Trabalho_Revenda')

    # Importar dados para a tabela
    df.to_sql('dados', engine, if_exists='append', index=False)
    print("Dados importados com sucesso.")

except Exception as e:
    print(f"Erro ao conectar ao banco de dados ou importar dados: {e}")