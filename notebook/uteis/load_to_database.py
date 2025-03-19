import mysql.connector

def load_to_mysql(dim_aluno, dim_escola, dim_municipio, fato_enem, batch_size=1000):
    # Conecta ao MySQL sem especificar um banco de dados inicial
    # conn = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="1234"
    # )
    
    conn = mysql.connector.connect(
        host="mysql",  # Nome do serviço no docker-compose
        user="root",
        password="1234",
        database="enem_db"
    )
    cursor = conn.cursor()

    # Cria o banco de dados se ele não existir
    cursor.execute("CREATE DATABASE IF NOT EXISTS enem_db")
    cursor.execute("USE enem_db")

    # Cria as tabelas dimensionais e de fatos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_aluno (
            id_aluno INT AUTO_INCREMENT PRIMARY KEY,
            numero_inscricao VARCHAR(20) UNIQUE,
            sexo VARCHAR(1),
            etnia INT,
            situacao_conclusao INT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_escola (
            id_escola INT AUTO_INCREMENT PRIMARY KEY,
            codigo_municipio INT,
            nom_municipio VARCHAR(100),
            estado VARCHAR(2)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_municipio (
            id_municipio INT AUTO_INCREMENT PRIMARY KEY,
            codigo_municipio INT UNIQUE,
            nom_municipio VARCHAR(100),
            estado VARCHAR(2)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fato_enem (
            id_fato INT AUTO_INCREMENT PRIMARY KEY,
            id_aluno INT,
            id_escola INT,
            id_municipio INT,
            nota_CN DOUBLE,
            nota_CH DOUBLE,
            nota_LC DOUBLE,
            nota_MT DOUBLE,
            nota_redacao VARCHAR(10),
            NOTA_MEDIA DOUBLE,
            presenca_CN INT,
            presenca_CH INT,
            presenca_LC INT,
            presenca_MT INT,
            FOREIGN KEY (id_aluno) REFERENCES dim_aluno(id_aluno),
            FOREIGN KEY (id_escola) REFERENCES dim_escola(id_escola),
            FOREIGN KEY (id_municipio) REFERENCES dim_municipio(id_municipio)
        )
    """)

    # Função para inserir um lote de dados em uma tabela
    def insert_batch(table_name, columns, batch):
        placeholders = ", ".join(["%s"] * len(columns))
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        cursor.executemany(query, batch)
        conn.commit()

    # Insere os dados nas tabelas dimensionais
    def insert_dim_data(df, table_name, columns):
        batch = []
        for row in df.toLocalIterator():
            batch.append(row)
            if len(batch) >= batch_size:
                insert_batch(table_name, columns, batch)
                batch = []
        if batch:
            insert_batch(table_name, columns, batch)

    # Insere dados na tabela dim_aluno
    insert_dim_data(
        dim_aluno.select("numero_inscricao", "sexo", "etnia", "situacao_conclusao"),
        "dim_aluno",
        ["numero_inscricao", "sexo", "etnia", "situacao_conclusao"]
    )

    # Insere dados na tabela dim_escola
    insert_dim_data(
        dim_escola.select("codigo_municipio", "nom_municipio", "estado"),
        "dim_escola",
        ["codigo_municipio", "nom_municipio", "estado"]
    )

    # Insere dados na tabela dim_municipio
    insert_dim_data(
        dim_municipio.select("codigo_municipio", "nom_municipio", "estado"),
        "dim_municipio",
        ["codigo_municipio", "nom_municipio", "estado"]
    )

    # Insere dados na tabela fato_enem
    # Primeiro, mapeia as chaves estrangeiras
    cursor.execute("SELECT numero_inscricao, id_aluno FROM dim_aluno")
    aluno_map = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.execute("SELECT codigo_municipio, id_escola FROM dim_escola")
    escola_map = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.execute("SELECT codigo_municipio, id_municipio FROM dim_municipio")
    municipio_map = {row[0]: row[1] for row in cursor.fetchall()}

    # Prepara os dados para a tabela fato_enem
    batch = []
    for row in fato_enem.toLocalIterator():
        id_aluno = aluno_map.get(row["numero_inscricao"])
        id_escola = escola_map.get(row["codigo_municipio"])
        id_municipio = municipio_map.get(row["codigo_municipio"])

        if id_aluno and id_escola and id_municipio:
            batch.append((
                id_aluno,
                id_escola,
                id_municipio,
                row["nota_CN"],
                row["nota_CH"],
                row["nota_LC"],
                row["nota_MT"],
                row["nota_redacao"],
                row["NOTA_MEDIA"],
                row["presenca_CN"],
                row["presenca_CH"],
                row["presenca_LC"],
                row["presenca_MT"]
            ))
            if len(batch) >= batch_size:
                insert_batch(
                    "fato_enem",
                    ["id_aluno", "id_escola", "id_municipio", "nota_CN", "nota_CH", "nota_LC", "nota_MT", "nota_redacao", "NOTA_MEDIA", "presenca_CN", "presenca_CH", "presenca_LC", "presenca_MT"],
                    batch
                )
                batch = []

    # Insere o último lote (se houver)
    if batch:
        insert_batch(
            "fato_enem",
            ["id_aluno", "id_escola", "id_municipio", "nota_CN", "nota_CH", "nota_LC", "nota_MT", "nota_redacao", "NOTA_MEDIA", "presenca_CN", "presenca_CH", "presenca_LC", "presenca_MT"],
            batch
        )

    # Fechamento da conexão
    cursor.close()
    conn.close()



# def load_to_mysql(df, mysql, table_name, batch_size=1000):
#     # Conecta ao MySQL sem especificar um banco de dados inicial
#     conn = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="1234"
#     )
#     cursor = conn.cursor()

#     # Cria o banco de dados se ele não existir
#     cursor.execute("CREATE DATABASE IF NOT EXISTS enem_db")
#     cursor.execute("USE enem_db")

#     # Cria a tabela se ela não existir
#     cursor.execute(f"""
#         CREATE TABLE IF NOT EXISTS {table_name} (
#             numero_inscricao VARCHAR(20) PRIMARY KEY,
#             sexo VARCHAR(1),
#             etnia INT,
#             codigo_municipio INT,
#             nom_municipio VARCHAR(100),
#             estado VARCHAR(2),
#             presenca_CN INT,
#             presenca_CH INT,
#             presenca_LC INT,
#             presenca_MT INT,
#             nota_CN DOUBLE,
#             nota_CH DOUBLE,
#             nota_LC DOUBLE,
#             nota_MT DOUBLE,
#             nota_redacao VARCHAR(10),
#             situacao_conclusao INT,
#             NOTA_MEDIA DOUBLE
#         )
#     """)

#     # Função para inserir um lote de dados
#     def insert_batch(batch):
#         query = f"""
#             INSERT INTO {table_name} (
#                 numero_inscricao, sexo, etnia, codigo_municipio, nom_municipio, estado, 
#                 presenca_CN, presenca_CH, presenca_LC, presenca_MT, 
#                 nota_CN, nota_CH, nota_LC, nota_MT, nota_redacao, situacao_conclusao, NOTA_MEDIA
#             ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         cursor.executemany(query, batch)
#         conn.commit()

#     # Processa os dados em lotes
#     batch = []
#     for row in df.toLocalIterator():  # Usa toLocalIterator para evitar coletar tudo na memória
#         batch.append(row)
#         if len(batch) >= batch_size:
#             insert_batch(batch)
#             batch = []

#     # Insere o último lote (se houver)
#     if batch:
#         insert_batch(batch)

#     # Fechamento da conexão
#     cursor.close()
#     conn.close()