# Steam-Games-Dataset
Repositório dedicado ao controle de versionamento do Banco de Dados "[Steam Games Dataset](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset)".

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

# ⚙️ Entregável 2 — Análise da Base, Ajustes e Indexação

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

# 🧩 Entregável 3 — Automatizações no PostgreSQL

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

# 🗄️ Entregável 4 — Modelagem do Data Warehouse (DW)

## Objetivo
Desenvolver o DW usando modelagem dimensional.

## Checklist
- [x] Escolher o tipo de modelagem (estrela, floco de neve etc.)
- [x] Criar pelo menos 1 tabela fato
- [x] Criar pelo menos 3 dimensões
- [ ] Justificar o DW, explicando:
  - [ ] Quais perguntas de negócio ele responde
  - [ ] Qual valor analítico ele gera

# 🔄 Entregável 5 — ETL para popular o DW

## Objetivo
Carregar o DW de forma automatizada utilizando uma ferramenta de ETL.

## Ferramentas (escolher uma)
- [ ] Apache NiFi
- [ ] Apache Airflow
- [ ] Pentaho
- [ ] Kafka

## Checklist
- [ ] Desenvolver o pipeline de ETL
- [ ] Popular o DW automaticamente
- [ ] Garantir que o processo seja reproduzível
- [ ] Demonstrar o funcionamento do ETL

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
