# Documentação Técnica do Projeto ETL ENEM

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

![Diagrama modelo estrela](diagramas\process.png)

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

![Diagrama modelo estrela](diagramas\diagrama_modelo_estrela.png)

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

## Considerações Finais

Este projeto é uma implementação básica de um pipeline ETL utilizando PySpark e MySQL. Ele pode ser expandido para incluir mais transformações, análises e visualizações. Certifique-se de que todas as dependências estão corretamente configuradas antes de executar o projeto.

Para mais informações, consulte a documentação oficial das bibliotecas utilizadas e o código fonte no repositório do projeto.
