import psycopg2

def connect_and_query():
    try:
        # Conecte-se ao banco de dados
        connection = psycopg2.connect(
            user="postgres",
            password="1234",
            host="127.0.0.1",
            port="5432",
            database="escola"
        )
        
        cursor = connection.cursor()
        
        # Execute a consulta SELECT
        query = "SELECT * FROM alunos;"
        cursor.execute(query)
        
        # Obtenha todos os resultados da consulta
        records = cursor.fetchall()
        
        # Exiba os resultados
        for row in records:
            print(row)
    
    except (Exception, psycopg2.Error) as error:
        print("Erro ao conectar ao PostgreSQL", error)
    
    finally:
        # Feche a conexão com o banco de dados
        if connection:
            cursor.close()
            connection.close()
            print("Conexão com PostgreSQL encerrada")

# Chame a função para conectar e consultar
connect_and_query()