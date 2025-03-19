# Documentação Técnica do Projeto ETL ENEM

# Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura do Projeto](#arquitetura-do-projeto)
   - [Visão Geral da Arquitetura](#visão-geral-da-arquitetura)
   - [Diagrama da Arquitetura](#diagrama-da-arquitetura)
   - [Componentes da Arquitetura](#componentes-da-arquitetura)
     - [Extração (Extract)](#1-extração-extract)
     - [Transformação (Transform)](#2-transformação-transform)
     - [Carregamento (Load)](#3-carregamento-load)
     - [Docker](#4-docker)
     - [Hadoop](#5-hadoop)
   - [Fluxo de Dados](#fluxo-de-dados)
   - [Benefícios da Arquitetura](#benefícios-da-arquitetura)
3. [Requisitos](#requisitos)
   - [Dependências](#dependências)
   - [Bibliotecas Python](#bibliotecas-python)
   - [Configuração do Ambiente](#configuração-do-ambiente)
4. [Tecnologias Utilizadas](#tecnologias-utilizadas)
   - [Docker](#1-docker)
   - [MySQL](#2-mysql)
   - [PySpark](#3-pyspark)
   - [Hadoop](#4-hadoop)
   - [Jupyter Notebook](#5-jupyter-notebook)
   - [Python](#6-python)
   - [Bibliotecas Python](#7-bibliotecas-python)
5. [Estrutura do Projeto](#estrutura-do-projeto)
   - [Diretórios](#diretórios)
   - [Notebook](#notebook)
   - [Perguntas Respondidas](#perguntas-respondidas)
6. [Execução do Projeto](#execução-do-projeto)
7. [Modelagem de Dados](#modelagem-de-dados)
   - [Esquema Estrela](#esquema-estrela)
     - [Tabela Fato: `fato_enem`](#1-tabela-fato-fato_enem)
     - [Tabela de Dimensão: `dim_aluno`](#2-tabela-de-dimensão-dim_aluno)
     - [Tabela de Dimensão: `dim_escola`](#3-tabela-de-dimensão-dim_escola)
     - [Tabela de Dimensão: `dim_municipio`](#4-tabela-de-dimensão-dim_municipio)
     - [Tabela de Dimensão: `dim_etnia`](#5-tabela-de-dimensão-dim_etnia)
8. [Instalação e Configuração](#instalação-e-configuração)
   - [Instalação do Docker](#1-instalação-do-docker)
   - [Configuração do Hadoop](#2-configuração-do-hadoop)
   - [Instalação do PySpark](#3-instalação-do-pyspark)
   - [Configuração do Arquivo `.env`](#4-configuração-do-arquivo-env)
9. [Fluxo de Trabalho (Workflow)](#fluxo-de-trabalho-workflow)
   - [Extração (Extract)](#1-extração-extract)
   - [Transformação (Transform)](#2-transformação-transform)
   - [Carregamento (Load)](#3-carregamento-load)
10. [Estrutura do Código](#estrutura-do-código)
    - [Estrutura do Projeto](#1-estrutura-do-projeto)
    - [Módulos Principais](#2-módulos-principais)
    - [Funções Principais](#3-funções-principais)
11. [Solução de Problemas (Troubleshooting)](#solução-de-problemas-troubleshooting)
    - [Erro de Conexão com o MySQL](#1-erro-de-conexão-com-o-mysql)
    - [Erro ao Executar o PySpark](#2-erro-ao-executar-o-pyspark)
    - [Problemas com o Docker](#3-problemas-com-o-docker)
    - [Erros de Leitura do Arquivo CSV](#4-erros-de-leitura-do-arquivo-csv)
12. [Boas Práticas e Considerações de Desempenho](#boas-práticas-e-considerações-de-desempenho)
    - [Otimização do PySpark](#1-otimização-do-pyspark)
    - [Modelagem de Dados no MySQL](#2-modelagem-de-dados-no-mysql)
    - [Escalabilidade](#3-escalabilidade)
13. [Referências e Links Úteis](#referências-e-links-úteis)
    - [Documentação Oficial](#1-documentação-oficial)
    - [Tutoriais e Artigos](#2-tutoriais-e-artigos)
14. [Versionamento e Contribuição](#versionamento-e-contribuição)
    - [Versionamento](#1-versionamento)
    - [Contribuição](#2-contribuição)
15. [Licença](#licença)
    - [Licença MIT](#1-licença-mit)
16. [Glossário](#glossário)
    - [ETL](#1-etl)
    - [Schema Estrela](#2-schema-estrela)
    - [PySpark](#3-pyspark)
    - [Parquet](#4-parquet)
17. [Histórico de Versões](#histórico-de-versões)
    - [Versão 1.0.0](#1-versão-100)
    - [Versão 1.1.0](#2-versão-110)
18. [Considerações Finais](#considerações-finais)

## Visão Geral

Este projeto tem como objetivo realizar a extração, transformação e carregamento (ETL) dos dados do Exame Nacional do Ensino Médio (ENEM) de 2020. O processo envolve a utilização de um contêiner Docker para o banco de dados MySQL, onde os dados são modelados em um esquema estrela com 4 dimensões e 1 fato. O projeto é implementado em Python utilizando PySpark para processamento de grandes volumes de dados.

## Arquitetura do Projeto

A arquitetura do projeto foi projetada para realizar o processo de **Extração, Transformação e Carregamento (ETL)** dos dados do ENEM 2020, utilizando tecnologias modernas e escaláveis. O sistema é composto por vários componentes que trabalham em conjunto para garantir a eficiência e a confiabilidade do pipeline de dados. Abaixo está uma visão detalhada da arquitetura utilizada:

---

### Visão Geral da Arquitetura

A arquitetura do projeto é baseada em um **pipeline ETL** que segue as seguintes etapas:

1. **Extração (Extract)**: Os dados brutos são extraídos de um arquivo CSV.
2. **Transformação (Transform)**: Os dados são processados e modelados para atender ao esquema estrela.
3. **Carregamento (Load)**: Os dados transformados são carregados em um banco de dados MySQL e salvos em arquivos Parquet.

O sistema utiliza as seguintes tecnologias principais:
- **Docker**: Para containerização do banco de dados MySQL.
- **PySpark**: Para processamento distribuído dos dados.
- **Hadoop**: Para suporte ao PySpark em ambientes Windows.
- **MySQL**: Para armazenamento dos dados transformados.
- **Parquet**: Para armazenamento eficiente dos dados em formato colunar.

---

### Diagrama da Arquitetura

Abaixo está um diagrama simplificado da arquitetura do projeto:

![Diagrama modelo estrela](https://github.com/xing-wang-kai/DESAFIO_DATA_MESHA/blob/main/diagramas/process.png)

---

### Componentes da Arquitetura

### 1. **Extração (Extract)**
   - **Fonte de Dados**: O arquivo `MICRODADOS_ENEM_2020.csv` contém os dados brutos do ENEM 2020.
   - **Ferramenta**: PySpark.
   - **Processo**:
     - O PySpark lê o arquivo CSV.
     - Configurações como delimitador, cabeçalho e codificação são aplicadas.
     - Os dados são carregados em um DataFrame para processamento.

#### 2. **Transformação (Transform)**
   - **Ferramenta**: PySpark.
   - **Processo**:
     - Seleção e renomeação de colunas.
     - Cálculo de novas métricas (ex: `NOTA_MEDIA`).
     - Remoção de duplicatas.
     - Criação de DataFrames para as tabelas dimensionais (`dim_aluno`, `dim_escola`, `dim_municipio`) e a tabela de fatos (`fato_enem`).

#### 3. **Carregamento (Load)**
   - **Destino 1: MySQL**:
     - Os dados transformados são carregados em um banco de dados MySQL rodando em um contêiner Docker.
     - O MySQL é utilizado para consultas rápidas e análises adicionais.
   - **Destino 2: Parquet**:
     - Os dados também são salvos em arquivos Parquet para armazenamento eficiente e processamento futuro.
     - O formato Parquet é ideal para grandes volumes de dados, pois é otimizado para leitura e escrita.

#### 4. **Docker**
   - **Função**: Containerização do banco de dados MySQL.
   - **Benefícios**:
     - Isolamento do ambiente de banco de dados.
     - Facilidade de configuração e replicação.
     - Compatibilidade com diferentes sistemas operacionais.

#### 5. **Hadoop**
   - **Função**: Suporte ao PySpark em ambientes Windows.
   - **Benefícios**:
     - Permite o uso do PySpark em sistemas Windows.
     - Fornece suporte para processamento distribuído.

---

### Fluxo de Dados

1. **Extração**:
   - O arquivo CSV é lido pelo PySpark.
   - Os dados brutos são carregados em um DataFrame.

2. **Transformação**:
   - Os dados são limpos, transformados e modelados.
   - São criados DataFrames para as tabelas dimensionais e de fatos.

3. **Carregamento**:
   - Os dados são persistidos no MySQL e em arquivos Parquet.
   - O MySQL é utilizado para consultas e análises.
   - Os arquivos Parquet são utilizados para armazenamento eficiente.

---

### Benefícios da Arquitetura

- **Escalabilidade**: O uso do PySpark e do formato Parquet permite o processamento de grandes volumes de dados.
- **Flexibilidade**: A containerização do MySQL com Docker facilita a replicação e o gerenciamento do ambiente.
- **Eficiência**: O formato Parquet é otimizado para leitura e escrita, reduzindo o tempo de processamento.
- **Portabilidade**: O projeto pode ser executado em diferentes sistemas operacionais, graças ao Docker e ao Hadoop.

---

## Requisitos

### Dependências

- **Docker**: Para rodar o contêiner do MySQL.
- **Hadoop**: Necessário para o funcionamento do PySpark. Baixe a versão 3.3.6 do [link oficial](https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz).
- **Winutils.exe**: Baixe o `winutils.exe` e salve em `C:\\hadoop-3.3.6\\bin` ou em outra pasta e informe o caminho correto no arquivo `.env`.
- **Dados do ENEM 2020**: Baixe os dados do ENEM 2020 do [link oficial](https://download.inep.gov.br/microdados/microdados_enem_2020.zip). Após descompactar, mova o arquivo `MICRODADOS_ENEM_2020.csv` para a pasta `database/raw`.

### Bibliotecas Python

As bibliotecas necessárias estão listadas no arquivo `requirements.txt`. Para instalar, execute:

```bash
pip install -r requirements.txt
```

### Configuração do Ambiente

1. **Docker**: Certifique-se de que o Docker está instalado e rodando. O contêiner do MySQL será iniciado automaticamente com as configurações necessárias.

2. **Hadoop**: Configure o Hadoop após baixar o arquivo e salvar o winultis.exe na pasta bin do hadoop copie e cole o caminho do hadoop no arquivo `.env`.
3. **Arquivo `.env`**: Configure as variáveis de ambiente necessárias, como o caminho do Hadoop e as credenciais do MySQL.
## Tecnologias Utilizadas

### 1. **Docker**
   - **Descrição**: Plataforma de virtualização que permite criar, implantar e executar aplicações em contêineres.
   - **Uso no Projeto**: Utilizado para rodar o banco de dados MySQL em um contêiner isolado, garantindo consistência e facilidade de configuração.

### 2. **MySQL**
   - **Descrição**: Sistema de gerenciamento de banco de dados relacional (SGBDR) de código aberto.
   - **Uso no Projeto**: Armazenamento dos dados transformados em um esquema estrela, composto por tabelas de dimensões e fatos.

### 3. **PySpark**
   - **Descrição**: API do Apache Spark para Python, utilizada para processamento distribuído de grandes volumes de dados.
   - **Uso no Projeto**: Realiza a extração, transformação e carregamento (ETL) dos dados do ENEM 2020.

### 4. **Hadoop**
   - **Descrição**: Framework de software para processamento distribuído de grandes volumes de dados.
   - **Uso no Projeto**: Necessário para o funcionamento do PySpark, especialmente em ambientes Windows (via `winutils.exe`).

### 5. **Jupyter Notebook**
   - **Descrição**: Ambiente interativo de desenvolvimento para Python, ideal para análise de dados e prototipagem.
   - **Uso no Projeto**: Utilizado para desenvolver e executar o código do ETL de forma interativa.

### 6. **Python**
   - **Descrição**: Linguagem de programação de alto nível, amplamente utilizada para análise de dados e automação.
   - **Uso no Projeto**: Linguagem principal para implementação do pipeline ETL.

### 7. **Bibliotecas Python**
   - **Pandas**: Para manipulação de dados em memória.
   - **PySpark**: Para processamento distribuído de dados.
   - **MySQL Connector**: Para conexão e interação com o banco de dados MySQL.
   - **SQLAlchemy**: Para facilitar a conexão e operações com o banco de dados.
   - **Findspark**: Para integrar o PySpark com o Jupyter Notebook.

---

## Estrutura do Projeto

### Diretórios

- **database/raw**: Contém o arquivo CSV bruto dos dados do ENEM 2020.
- **database/transformed**: Armazena os dados transformados em formato Parquet.
- **notebook**: Contém o notebook Jupyter com o código do projeto.
- **uteis**: Módulos utilitários para ETL, carregamento de dados e respostas às perguntas.

### Notebook

O notebook `PROJETO_ETL_ENEM.ipynb` contém o código completo do projeto, incluindo:

1. **Extração**: Leitura do arquivo CSV e carregamento dos dados em um DataFrame do PySpark.
2. **Transformação**: Criação das dimensões e da tabela fato.
3. **Carregamento**: Persistência dos dados transformados em formato Parquet e no MySQL.
4. **Respostas às Perguntas**: Consultas para responder às perguntas propostas.

### Perguntas Respondidas

1. **Qual a escola com a maior média de notas?**
2. **Qual o aluno com a maior média de notas e o valor dessa média?**
3. **Qual a média geral?**
4. **Qual o % de Ausentes?**
5. **Qual o número total de Inscritos?**
6. **Qual a média por disciplina?**
7. **Qual a média por Sexo?**
8. **Qual a média por Etnia?**

## Execução do Projeto

1. **Inicie o contêiner Docker**:
   ```bash
   docker-compose up -d
   ```
    a. Verifique se o container está rodando corretamente com o comando:
    ```bash
    docker ps
    ```
    b. Tente conectar o banco de dados configurando no My workbench com host = localhost e port 1143 senha 1234 ou então pelo comando:

    ```bash
    docker exec -it db mysql -u root -p
    ```
    insira seu logim e senha.


2. **Execute o notebook**:
   - Abra o notebook `PROJETO_ETL_ENEM.ipynb` no Jupyter.
   - Execute as células na ordem para realizar o ETL e responder às perguntas.

3. **Verifique os dados no MySQL**:
   - Após a execução, os dados estarão disponíveis no banco de dados MySQL.

## Modelagem de Dados

### Esquema Estrela

O esquema estrela é composto por 4 tabelas de dimensões e 1 tabela fato:

![Diagrama modelo estrela](https://github.com/xing-wang-kai/DESAFIO_DATA_MESHA/blob/main/diagramas/diagrama_modelo_estrela.png)

#### 1. **Tabela Fato: `fato_enem`**
   - **Descrição**: Armazena as notas e informações de presença dos alunos no ENEM.
   - **Campos**:
     - `numero_inscricao`: Número de inscrição do aluno.
     - `codigo_municipio`: Código do município onde o aluno realizou a prova.
     - `nota_CN`: Nota da prova de Ciências da Natureza.
     - `nota_CH`: Nota da prova de Ciências Humanas.
     - `nota_LC`: Nota da prova de Linguagens e Códigos.
     - `nota_MT`: Nota da prova de Matemática.
     - `nota_redacao`: Nota da redação.
     - `NOTA_MEDIA`: Média das notas do aluno.
     - `presenca_CN`: Presença na prova de Ciências da Natureza (0 = ausente, 1 = presente).
     - `presenca_CH`: Presença na prova de Ciências Humanas.
     - `presenca_LC`: Presença na prova de Linguagens e Códigos.
     - `presenca_MT`: Presença na prova de Matemática.

#### 2. **Tabela de Dimensão: `dim_aluno`**
   - **Descrição**: Armazena informações demográficas e pessoais dos alunos.
   - **Campos**:
     - `numero_inscricao`: Número de inscrição do aluno.
     - `sexo`: Sexo do aluno (M = Masculino, F = Feminino).
     - `etnia`: Código da etnia do aluno.
     - `situacao_conclusao`: Situação de conclusão do ensino médio (1 = concluído, 2 = cursando).

#### 3. **Tabela de Dimensão: `dim_escola`**
   - **Descrição**: Armazena informações sobre as escolas dos alunos.
   - **Campos**:
     - `codigo_municipio`: Código do município da escola.
     - `nom_municipio`: Nome do município da escola.
     - `estado`: Sigla do estado da escola.

#### 4. **Tabela de Dimensão: `dim_municipio`**
   - **Descrição**: Armazena informações sobre os municípios onde as provas foram realizadas.
   - **Campos**:
     - `codigo_municipio`: Código do município.
     - `nom_municipio`: Nome do município.
     - `estado`: Sigla do estado.

#### 5. **Tabela de Dimensão: `dim_etnia`**
   - **Descrição**: Armazena informações sobre a etnia dos alunos.
   - **Campos**:
     - `codigo_etnia`: Código da etnia.
     - `descricao_etnia`: Descrição da etnia (ex: Branca, Preta, Parda, etc.).

---

## Instalação e Configuração

Este tópico fornece um guia passo a passo para instalar e configurar todas as dependências necessárias para executar o projeto.

### 1. **Instalação do Docker**
   - **Passo 1**: Baixe e instale o Docker Desktop a partir do [site oficial](https://www.docker.com/products/docker-desktop).
   - **Passo 2**: Inicie o Docker Desktop e verifique se ele está rodando corretamente.
   - **Passo 3**: Crie um contêiner MySQL usando o seguinte comando:
     ```bash
     docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=1234 -p 3306:3306 -d mysql:latest
     ```
   - **Passo 4**: Verifique se o contêiner está rodando:
     ```bash
     docker ps
     ```

### 2. **Configuração do Hadoop**
   - **Passo 1**: Baixe o Hadoop 3.3.6 do [site oficial](https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz).
   - **Passo 2**: Extraia o arquivo baixado e mova a pasta para `C:\hadoop-3.3.6`.
   - **Passo 3**: Baixe o `winutils.exe` e salve-o em `C:\hadoop-3.3.6\bin`.
   - **Passo 4**: Configure as variáveis de ambiente no Windows:
     - Adicione `C:\hadoop-3.3.6\bin` ao `PATH`.
     - Defina `HADOOP_HOME` e `hadoop.home.dir` como `C:\hadoop-3.3.6`.

### 3. **Instalação do PySpark**
   - **Passo 1**: Instale o PySpark usando o pip:
     ```bash
     pip install pyspark
     ```
   - **Passo 2**: Verifique a instalação:
     ```bash
     pyspark --version
     ```

### 4. **Configuração do Arquivo `.env`**
   - Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
     ```env
     HADOOP_PATH=C:\\hadoop-3.3.6
     DATABASE_PATH=..\\database\\raw\\MICRODADOS_ENEM_2020.csv
     PARQUET_PATH=..\\database\\transformed\\dados_enem_parquet
     HOST=localhost
     PORT=3306
     USER=root
     PASSWORD=1234
     ```

---

## Fluxo de Trabalho (Workflow)

Este tópico descreve o fluxo de trabalho do projeto, desde a extração dos dados até a geração dos resultados.

### 1. **Extração (Extract)**
   - **Descrição**: Os dados brutos são extraídos do arquivo CSV `MICRODADOS_ENEM_2020.csv`.
   - **Ferramenta**: PySpark.
   - **Processo**:
     - O arquivo CSV é lido usando o PySpark.
     - Configurações como delimitador, cabeçalho e codificação são aplicadas.
     - Os dados são carregados em um DataFrame para processamento.

### 2. **Transformação (Transform)**
   - **Descrição**: Os dados brutos são transformados e modelados para atender ao esquema estrela.
   - **Ferramenta**: PySpark.
   - **Processo**:
     - Seleção e renomeação de colunas.
     - Cálculo de novas métricas (ex: `NOTA_MEDIA`).
     - Remoção de duplicatas.
     - Criação de DataFrames para as tabelas dimensionais (`dim_aluno`, `dim_escola`, `dim_municipio`) e a tabela de fatos (`fato_enem`).

### 3. **Carregamento (Load)**
   - **Descrição**: Os dados transformados são carregados no MySQL e salvos em arquivos Parquet.
   - **Ferramenta**: PySpark e MySQL.
   - **Processo**:
     - Os dados são persistidos no MySQL para consultas rápidas.
     - Os dados também são salvos em arquivos Parquet para armazenamento eficiente.

---

## Estrutura do Código

Este tópico descreve a estrutura do código e os principais módulos/funções do projeto.

### 1. **Estrutura do Projeto**
   - **`database/raw`**: Contém o arquivo CSV bruto (`MICRODADOS_ENEM_2020.csv`).
   - **`database/transformed`**: Armazena os dados transformados em formato Parquet.
   - **`notebook`**: Contém o notebook Jupyter com o código do projeto.
   - **`uteis`**: Módulos utilitários para ETL, carregamento de dados e respostas às perguntas.

### 2. **Módulos Principais**
   - **`ETL.py`**: Contém a classe `ETL` com os métodos `extract`, `transform` e `load`.
   - **`load_to_database.py`**: Contém a função `load_to_mysql` para carregar os dados no MySQL.
   - **`answer.py`**: Contém a classe `Answer` para responder às perguntas do projeto.

### 3. **Funções Principais**
   - **`extract(spark, file_path)`**:
     - **Descrição**: Extrai os dados do arquivo CSV.
     - **Exemplo de Uso**:
       ```python
       df = etl.extract(spark, "database/raw/MICRODADOS_ENEM_2020.csv")
       ```
   - **`transform(df)`**:
     - **Descrição**: Transforma os dados brutos em DataFrames para as tabelas dimensionais e de fatos.
     - **Exemplo de Uso**:
       ```python
       dim_aluno, dim_escola, dim_municipio, fato_enem = etl.transform(df)
       ```
   - **`load(dim_aluno, dim_escola, dim_municipio, fato_enem, parquet_path)`**:
     - **Descrição**: Salva os DataFrames como arquivos Parquet.
     - **Exemplo de Uso**:
       ```python
       etl.load(dim_aluno, dim_escola, dim_municipio, fato_enem, "database/transformed")
       ```

---

## Solução de Problemas (Troubleshooting)

Este tópico fornece um guia para solucionar problemas comuns que podem ocorrer durante a execução do projeto.

### 1. **Erro de Conexão com o MySQL**
   - **Sintoma**: Falha ao conectar ao banco de dados MySQL.
   - **Solução**:
     - Verifique as credenciais no arquivo `.env` (host, port, user, password).
     - Certifique-se de que o contêiner Docker do MySQL está rodando:
       ```bash
       docker ps
       ```
     - Verifique os logs do contêiner MySQL para identificar possíveis erros:
       ```bash
       docker logs mysql-container
       ```

### 2. **Erro ao Executar o PySpark**
   - **Sintoma**: Erros relacionados ao Hadoop ou ao PySpark.
   - **Solução**:
     - Verifique se o `winutils.exe` está corretamente configurado no diretório `C:\hadoop-3.3.6\bin`.
     - Certifique-se de que as variáveis de ambiente `HADOOP_HOME` e `hadoop.home.dir` estão configuradas corretamente.
     - Reinicie o ambiente após fazer alterações nas variáveis de ambiente.

### 3. **Problemas com o Docker**
   - **Sintoma**: Contêiner Docker não inicia ou falha.
   - **Solução**:
     - Verifique se o Docker Desktop está rodando.
     - Reinicie o Docker Desktop e tente novamente.
     - Verifique os logs do Docker para mais detalhes:
       ```bash
       docker logs <container_id>
       ```

### 4. **Erros de Leitura do Arquivo CSV**
   - **Sintoma**: Falha ao ler o arquivo CSV.
   - **Solução**:
     - Verifique o caminho do arquivo no arquivo `.env`.
     - Certifique-se de que o arquivo CSV está no formato correto e não está corrompido.

---

## Boas Práticas e Considerações de Desempenho

Este tópico fornece recomendações para otimizar o desempenho do projeto e boas práticas para modelagem de dados.

### 1. **Otimização do PySpark**
   - **Ajuste de Partições**: Ajuste o número de partições para melhorar o desempenho do processamento distribuído.
     ```python
     df = df.repartition(100)
     ```
   - **Uso de Cache**: Utilize o cache para armazenar DataFrames frequentemente acessados.
     ```python
     df.cache()
     ```
   - **Evite Shuffling**: Minimize operações que causam shuffling, como `join` e `groupBy`.

### 2. **Modelagem de Dados no MySQL**
   - **Índices**: Adicione índices às colunas frequentemente consultadas para melhorar a performance.
     ```sql
     CREATE INDEX idx_numero_inscricao ON dim_aluno(numero_inscricao);
     ```
   - **Normalização**: Utilize a normalização para evitar redundância de dados.
   - **Chaves Primárias e Estrangeiras**: Defina chaves primárias e estrangeiras para garantir a integridade dos dados.

### 3. **Escalabilidade**
   - **Grandes Volumes de Dados**: Para grandes volumes de dados, considere o uso de clusters Spark e bancos de dados distribuídos.
   - **Particionamento de Dados**: Utilize particionamento de dados para melhorar a eficiência de consultas e processamento.

---

## Referências e Links Úteis

Este tópico fornece links para documentação oficial e recursos adicionais.

### 1. **Documentação Oficial**
   - **PySpark**: [Documentação do PySpark](https://spark.apache.org/docs/latest/api/python/)
   - **Docker**: [Documentação do Docker](https://docs.docker.com/)
   - **MySQL**: [Documentação do MySQL](https://dev.mysql.com/doc/)
   - **Hadoop**: [Documentação do Hadoop](https://hadoop.apache.org/docs/stable/)

### 2. **Tutoriais e Artigos**
   - **Tutorial de PySpark**: [Tutorial PySpark](https://sparkbyexamples.com/pyspark-tutorial/)
   - **Guia de Docker para Iniciantes**: [Docker para Iniciantes](https://docker-curriculum.com/)
   - **Boas Práticas de Modelagem de Dados**: [Modelagem de Dados](https://www.guru99.com/database-normalization.html)

---

## Versionamento e Contribuição

Este tópico descreve como o versionamento é feito e como contribuir para o projeto.

### 1. **Versionamento**
   - **Git**: O projeto utiliza Git para versionamento. Cada versão é marcada com uma tag.
   - **Tags**: As versões são marcadas seguindo o padrão `vX.Y.Z` (ex: `v1.0.0`).

### 2. **Contribuição**
   - **Pull Requests**: Contribuições são bem-vindas através de pull requests.
   - **Diretrizes**:
     - Siga as boas práticas de codificação.
     - Adicione testes para novas funcionalidades.
     - Documente as mudanças no `CHANGELOG.md`.

---

## Licença

Este tópico descreve a licença sob a qual o projeto é distribuído.

### 1. **Licença MIT**
   - **Descrição**: O projeto é distribuído sob a licença MIT, que permite uso, modificação e distribuição livre, desde que o aviso de copyright e a permissão sejam incluídos.
   - **Texto Completo**: Consulte o arquivo `LICENSE` no repositório do projeto.

---

## Glossário

Este tópico define termos técnicos e conceitos utilizados no projeto.

### 1. **ETL**
   - **Definição**: Processo de Extração, Transformação e Carregamento de dados.

### 2. **Schema Estrela**
   - **Definição**: Modelo de dados que consiste em uma tabela de fatos central e várias tabelas dimensionais.

### 3. **PySpark**
   - **Definição**: API do Apache Spark para Python, utilizada para processamento distribuído de dados.

### 4. **Parquet**
   - **Definição**: Formato de armazenamento de dados colunar, otimizado para grandes volumes de dados.

---

## Histórico de Versões

Este tópico registra as mudanças e atualizações do projeto.

### 1. **Versão 1.0.0**
   - **Data**: 10/10/2023
   - **Mudanças**:
     - Implementação inicial do pipeline ETL.
     - Adição de suporte a Docker e MySQL.
     - Criação da documentação técnica.

### 2. **Versão 1.1.0**
   - **Data**: 15/10/2023
   - **Mudanças**:
     - Adição de suporte a arquivos Parquet.
     - Melhorias na documentação.

---


## Considerações Finais

Este projeto é uma implementação básica de um pipeline ETL utilizando PySpark e MySQL. Ele pode ser expandido para incluir mais transformações, análises e visualizações. Certifique-se de que todas as dependências estão corretamente configuradas antes de executar o projeto.

Para mais informações, consulte a documentação oficial das bibliotecas utilizadas e o código fonte no repositório do projeto.
