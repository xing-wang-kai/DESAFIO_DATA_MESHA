import mysql.connector
from dotenv import load_dotenv
import os
from pyspark.sql import DataFrame
from typing import List, Tuple, Dict, Optional

def load_to_mysql(
    dim_aluno: DataFrame,
    dim_escola: DataFrame,
    dim_municipio: DataFrame,
    fato_enem: DataFrame,
    batch_size: int = 1000
) -> None:
    """
    Carrega os dados transformados (DataFrames) para o banco de dados MySQL.

    Args:
        dim_aluno (DataFrame): DataFrame contendo os dados da dimensão 'aluno'.
        dim_escola (DataFrame): DataFrame contendo os dados da dimensão 'escola'.
        dim_municipio (DataFrame): DataFrame contendo os dados da dimensão 'municipio'.
        fato_enem (DataFrame): DataFrame contendo os dados da tabela fato 'fato_enem'.
        batch_size (int, optional): Tamanho do lote para inserção no banco de dados. Padrão é 1000.

    Returns:
        None
    """
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()

    # Configurações de conexão com o MySQL
    host: str = os.getenv("HOST")
    port: int = int(os.getenv("PORT"))
    user: str = os.getenv("USER")
    password: str = os.getenv("PASSWORD")

    # Conecta ao MySQL
    conn: mysql.connector.MySQLConnection = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password
    )
    cursor: mysql.connector.cursor.MySQLCursor = conn.cursor()

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

    def insert_batch(table_name: str, columns: List[str], batch: List[Tuple]) -> None:
        """
        Insere um lote de registros em uma tabela do MySQL.

        Args:
            table_name (str): Nome da tabela onde os dados serão inseridos.
            columns (List[str]): Lista de colunas da tabela.
            batch (List[Tuple]): Lista de tuplas contendo os dados a serem inseridos.

        Returns:
            None
        """
        placeholders: str = ", ".join(["%s"] * len(columns))
        updates: str = ", ".join([f"{col} = VALUES({col})" for col in columns])
        query: str = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {updates}"
        cursor.executemany(query, batch)
        conn.commit()

    def insert_dim_data(df: DataFrame, table_name: str, columns: List[str]) -> None:
        """
        Insere os dados de uma dimensão (DataFrame) em uma tabela do MySQL.

        Args:
            df (DataFrame): DataFrame contendo os dados a serem inseridos.
            table_name (str): Nome da tabela de destino.
            columns (List[str]): Lista de colunas da tabela.

        Returns:
            None
        """
        batch: List[Tuple] = []
        for row in df.toLocalIterator():
            batch.append(tuple(row))
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

    # Mapeia as chaves estrangeiras
    cursor.execute("SELECT numero_inscricao, id_aluno FROM dim_aluno")
    aluno_map: Dict[str, int] = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.execute("SELECT codigo_municipio, id_escola FROM dim_escola")
    escola_map: Dict[int, int] = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.execute("SELECT codigo_municipio, id_municipio FROM dim_municipio")
    municipio_map: Dict[int, int] = {row[0]: row[1] for row in cursor.fetchall()}

    # Prepara os dados para a tabela fato_enem
    batch: List[Tuple] = []
    for row in fato_enem.toLocalIterator():
        id_aluno: Optional[int] = aluno_map.get(row["numero_inscricao"])
        id_escola: Optional[int] = escola_map.get(row["codigo_municipio"])
        id_municipio: Optional[int] = municipio_map.get(row["codigo_municipio"])

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