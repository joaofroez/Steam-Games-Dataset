import sys
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# --- 1. CONFIGURAÇÃO DE CAMINHOS ---
sys.path.append('/opt/airflow/dags/Scripts_normalizacao')

# --- 2. IMPORTAÇÃO DAS SUAS FUNÇÕES ---
try:
    from Scripts_normalizacao.DDL.create_tables_ import create_tables
    from Scripts_normalizacao.DDL.create_dw_tables_ import create_dw_tables
    from Scripts_normalizacao.DML.import_ import import_games  
    from Scripts_normalizacao.DML.import_dw_ import import_dw
except ImportError as e:
    print(f"Erro de importação (será resolvido no Docker): {e}")

# --- 3. DEFINIÇÃO DA DAG ---
default_args = {
    'owner': 'grupo_5',
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='steam_etl_v1',
    default_args=default_args,
    description='Pipeline ETL Steam: DDL -> DML',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@once',
    catchup=False,
) as dag:
    
    def create_database():
        create_tables()
        create_dw_tables()
        pass

    task_install_deps = BashOperator(
        task_id='0_instalar_libs',
        bash_command='pip install ijson'
    )

    # Criar/Recriar Tabelas
    task_ddl = PythonOperator(
        task_id='1_criar_estrutura',
        python_callable=create_database 
    )

    # Importar Dados no banco normalizado
    task_ingestion = PythonOperator(
        task_id='2_popular_banco',
        python_callable=import_games  
    )

    # Popular o Data Warehouse 
    task_dw_load = PythonOperator(
        task_id='3_carregar_dw',
        python_callable=import_dw
    )

    task_install_deps >> task_ddl >> task_ingestion >> task_dw_load