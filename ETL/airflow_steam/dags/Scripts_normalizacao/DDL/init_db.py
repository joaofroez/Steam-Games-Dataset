import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from DML.config import DB_CONFIG

def create_database_if_not_exists():
    print("Verificando existência do Banco de Dados...")
    
    data_name = DB_CONFIG['dbname']

    config_init = DB_CONFIG.copy()
    config_init['dbname'] = 'postgres'
    
    try:
        conn = psycopg2.connect(**config_init)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
        cur = conn.cursor()
        
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{data_name}'")
        exists = cur.fetchone()
        
        if not exists:
            print(f"Banco '{data_name}' não encontrado. Criando.")
            cur.execute(f'CREATE DATABASE "{data_name}"')
            print(f"Banco '{data_name}' criado com sucesso!")
        else:
            print(f"Banco '{data_name}' já existe. Nada a fazer.")
            
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Erro ao tentar criar database: {e}")
        raise e