# Steam-Games-Dataset
Repositório dedicado ao controle de versionamento do Banco de Dados "[Steam Games Dataset](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset)".


# 🎮 Steam ETL Pipeline

Este projeto consiste em um pipeline de Engenharia de dados completo para ingestão, processamento, importação e análise do dataset de jogos da Steam. O sistema envolve a leitura de dados brutos, normalização para um banco transacional (OLTP), criação de automatizações no PostgreSQL e transformação final para um Data Warehouse (OLAP/Star Schema).

![Badge Airflow](https://img.shields.io/badge/Orchestration-Apache%20Airflow-blue?style=for-the-badge&logo=apacheairflow)
![Badge Docker](https://img.shields.io/badge/Container-Docker-2496ED?style=for-the-badge&logo=docker)
![Badge Postgres](https://img.shields.io/badge/Database-PostgreSQL-336791?style=for-the-badge&logo=postgresql)
![Badge Python](https://img.shields.io/badge/Code-Python-3776AB?style=for-the-badge&logo=python)

---

## 🏗️ Arquitetura do Projeto

O pipeline foi desenhado para ser **reproduzível** via Docker.

1.  **Extract (Extração):** Leitura de arquivo `JSON` (Steam Games Dataset) utilizando processamento em stream (`ijson`) para alta performance.
2.  **Transform (Transformação):**
    * Limpeza de dados (Data Cleaning) e tratamento de tipos.
    * Normalização de dados (Terceira Forma Normal) para tabelas relacionais (`games`, `publishers`, `developers`).
3.  **Load (Carga):**
    * Modelagem Dimensional (Star Schema).
    * Carga na Tabela Fato (`fato_performance_steam`) e Dimensões (`dim_tempo`, `dim_jogo`, `dim_publisher`).

---

## 📋 Pré-requisitos

Para rodar este projeto, você precisa apenas ter instalado na sua máquina:

* **[Docker Desktop](https://www.docker.com/products/docker-desktop/)**
* **Git** (Para clonar o repositório)

> **Nota:** Não é necessário instalar Python ou Airflow localmente. O Docker cuidará de todas as dependências.

---

## 🚀 Como Executar (Passo a Passo)

Siga estas instruções para subir o ambiente do zero.

### 1° Clone o Repositório
Rode o comando:
```bash
git clone https://github.com/HenriqueIgreja/Steam-Games-Dataset.git
cd Steam-Games-Dataset
```


### 2° Configure o arquivo config.py
Verifique o arquivo dags/Scripts_normalizacao/DML/config.py. O projeto está configurado para rodar no Docker conectando-se ao PostgreSQL local.

Host: host.docker.internal (Padrão para Docker comunicar com Windows/Mac)

Database: postgres (Banco padrão)

Senha: Certifique se a senha no arquivo bate com a senha do seu banco local, ou ajuste conforme necessário


### 3° Suba o Ambiente (Docker)
Com docker aberto, abra a raiz do projeto (onde está o docker-compose.yaml), e então execute:
```docker compose up -d```

### 4° Acesse o Airflow
Abra seu navegador e acesse:

URL:  [http://localhost:8080](http://localhost:8080)

Usuário: ```airflow```

Senha: ```airflow```

### 5° Execute o Pipeline
Na lista de DAGs, procure por ```steam_etl_v1```

Ative a DAG clicando no interruptor na esquerda.

Clique no botão play na direita e selecione "Trigger DAG".

### 6° Acompanhe o Processo
Clique no nome da DAG e vá para a aba "Graph". Você verá as tarefas sendo executadas:

✅ 0_instalar_libs: Instala dependências Python (ijson, psycopg2)

✅ 0.5_criar_database: Cria o banco de dados automaticamente se não existir

✅ 1_infraestrutura_db: Cria/Recria as tabelas (OLTP e OLAP)

✅ 2_ingestao_json: Popula o banco transacional

✅ 3_carga_dw: Carrega o Data Warehouse


# Importação dos Dados
- Instale o Python 3.12+ 
- Clone o repositório
- Crie um ambiente virtual na pasta raiz do projeto com o comando `py -m venv venv`
- Ative o ambiente com o comando `venv\Scripts\activate`
- Instale as libs necessárias com o comando `pip install psycopg2 ijson`
- Ajuste o arquivo config.py colocando sua senha corretamente.
- Rode o arquivo main.py
- Espere a importação de todos registros acabarem
- Pronto!
# 📦 Entregável 1 — Dicionário de Dados Inicial (Concluído)

## Objetivo
Compreender completamente a estrutura atual da base de dados original antes de qualquer alteração.

## Checklist
- [x] Analisar a base de dados original (sem modificar nada)
- [x] Listar todas as tabelas existentes
- [x] Documentar cada coluna contendo:
  - Tipo de dado
  - Descrição
  - Observações relevantes
- [x] Identificar todas as chaves:
- [x] Primárias
- [x] Estrangeiras
- [x] Criar o dicionário de dados (Excel, Word ou PDF)

Arquivo .csv contendo o Dicionário de Dados Inicial se encontra no caminho [Dicionário_de_Dados_Inicial](/DW/Dicionário_de_Dados_Inicial.csv).

# ⚙️ Entregável 2 — Análise da Base, Ajustes e Indexação (Concluído)

## Objetivo
Corrigir problemas estruturais, normalizar, ajustar relações e preparar um novo modelo consistente.

## Checklist
- [x] Identificar problemas da base:
  - [x] Falta de normalização
  - [x] Relações mal definidas
  - [x] Estruturas inadequadas
  - [x] Tipos incorretos/inconsistentes
- [x] Propor todas as correções necessárias
- [x] Aplicar as correções no banco
- [x] Criar um script de migração da versão antiga para a nova (preservando 100% dos dados)
- [x] Documentar e justificar cada modificação realizada
- [x] Criar índices para todas as tabelas
  - [x] Explicar utilidade dos índices para:
    - [x] Performance
    - [x] Integridade
    - [x] Consultas frequentes
- [x] Criar o novo dicionário de dados

# 🧩 Entregável 3 — Automatizações no PostgreSQL (Concluído)

## Objetivo
Criar automações significativas que agreguem valor ao domínio da base.

## Devem ser criados
- [x] 3 Triggers
- [x] 3 Functions
- [x] 3 Views
- [x] 3 Procedures

## Regras
- [x] Automatizações devem ser coerentes com o domínio
- [x] Não pode ser trivial (ex.: SELECT simples)
- [x] Cada automação deve ter justificativa explicando:
  - [x] Por que existe
  - [x] Qual problema resolve
  - [x] Como melhora o sistema
- [x] Adicionar nova seção no novo dicionário de dados

---

# 🗄️ Entregável 4 — Modelagem do Data Warehouse (DW) (Concluído)

## Objetivo
Desenvolver o DW usando modelagem dimensional.

## Checklist
- [x] Escolher o tipo de modelagem (estrela, floco de neve etc.)
- [x] Criar pelo menos 1 tabela fato
- [x] Criar pelo menos 3 dimensões
- [x] Justificar o DW, explicando:
  - [x] Quais perguntas de negócio ele responde
  - [x] Qual valor analítico ele gera

# 🔄 Entregável 5 — ETL para popular o DW (Concluído)

## Objetivo
Carregar o DW de forma automatizada utilizando uma ferramenta de ETL.

## Ferramentas (escolher uma)
- [ ] Apache NiFi
- [x] Apache Airflow
- [ ] Pentaho
- [ ] Kafka

## Checklist
- [x] Desenvolver o pipeline de ETL
- [x] Popular o DW automaticamente
- [x] Garantir que o processo seja reproduzível
- [x] Demonstrar o funcionamento do ETL

---

# ⭐ Bônus (opcional, mas vale nota extra)

## 🎁 Bônus 1 — Backup Automático
- [ ] Implementar backup com:
  - [ ] pgBackRest  
  - [ ] ou pgBarman  

---

## 📊 Bônus 2 — Monitoramento do Banco

### Ferramentas possíveis
- [ ] pgBadger
- [ ] TemBoard
- [ ] Prometheus + Grafana

### Checklist
- [ ] Implementar monitoramento
- [ ] Gerar consultas mal otimizadas
- [ ] Demonstrar nos dashboards:
  - [ ] Gargalos
  - [ ] Alertas
  - [ ] Problemas de performance
- [ ] Mostrar como o monitoramento auxilia na melhoria do banco

# 📈 Bônus 3 — Visualização Analítica

- [ ] Criar dashboards usando Apache Superset com dados do DW

---

# 📌 Observações Importantes

- Todas as entregas devem ser feitas pelo GitHub

## A avaliação considerará:
- Commits de cada aluno
- Clareza no histórico do repositório

## Cada aluno deve enviar:
-  Um vídeo de ~10 minutos explicando o que desenvolveu