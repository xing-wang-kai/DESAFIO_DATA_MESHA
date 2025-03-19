from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.functions import col
from typing import Tuple

class ETL:
    """
    Classe responsável por realizar o processo de ETL (Extract, Transform, Load) em dados do ENEM.
    """

    def extract(self, spark: SparkSession, file_path: str) -> DataFrame:
        """
        Extrai os dados de um arquivo CSV e retorna um DataFrame.

        Args:
            spark (SparkSession): Sessão do Spark.
            file_path (str): Caminho do arquivo CSV.

        Returns:
            DataFrame: DataFrame contendo os dados extraídos.
        """
        df: DataFrame = spark.read \
            .option("delimiter", ";") \
            .option("header", "true") \
            .option("encoding", "ISO-8859-1") \
            .csv(file_path)
        return df

    def transform(self, df: DataFrame) -> Tuple[DataFrame, DataFrame, DataFrame, DataFrame]:
        """
        Transforma os dados brutos em DataFrames estruturados para as tabelas dimensionais e de fatos.

        Args:
            df (DataFrame): DataFrame contendo os dados brutos.

        Returns:
            Tuple[DataFrame, DataFrame, DataFrame, DataFrame]: 
                - dim_aluno: DataFrame da dimensão 'aluno'.
                - dim_escola: DataFrame da dimensão 'escola'.
                - dim_municipio: DataFrame da dimensão 'municipio'.
                - fato_enem: DataFrame da tabela fato 'fato_enem'.
        """
        # Seleciona e renomeia as colunas necessárias
        df = df.select(
            col("NU_INSCRICAO").cast("string").alias("numero_inscricao"),
            col("TP_SEXO").cast("string").alias("sexo"),
            col("TP_COR_RACA").cast("integer").alias("etnia"),
            col("CO_MUNICIPIO_ESC").cast("integer").alias("codigo_municipio"),
            col("NO_MUNICIPIO_ESC").cast("string").alias("nom_municipio"),
            col("SG_UF_ESC").cast("string").alias("estado"),
            col("TP_PRESENCA_CN").cast("integer").alias("presenca_CN"),
            col("TP_PRESENCA_CH").cast("integer").alias("presenca_CH"),
            col("TP_PRESENCA_LC").cast("integer").alias("presenca_LC"),
            col("TP_PRESENCA_MT").cast("integer").alias("presenca_MT"),
            col("NU_NOTA_CN").cast("double").alias("nota_CN"),
            col("NU_NOTA_CH").cast("double").alias("nota_CH"),
            col("NU_NOTA_LC").cast("double").alias("nota_LC"),
            col("NU_NOTA_MT").cast("double").alias("nota_MT"),
            col("NU_NOTA_REDACAO").cast("string").alias("nota_redacao"),
            col("TP_ST_CONCLUSAO").cast("integer").alias("situacao_conclusao")
        )
        
        # Adiciona a coluna NOTA_MEDIA
        df = df.withColumn(
            "NOTA_MEDIA", 
            (col("nota_MT") + col("nota_CN") + col("nota_CH") + col("nota_LC") + col("nota_redacao")) / 5
        )

        # Cria os DataFrames para as tabelas dimensionais e de fatos
        dim_aluno: DataFrame = df.select(
            "numero_inscricao",
            "sexo",
            "etnia",
            "situacao_conclusao"
        ).distinct()  # Remove duplicatas

        dim_escola: DataFrame = df.select(
            "codigo_municipio",
            "nom_municipio",
            "estado"
        ).distinct()  # Remove duplicatas

        dim_municipio: DataFrame = df.select(
            "codigo_municipio",
            "nom_municipio",
            "estado"
        ).distinct()  # Remove duplicatas

        # Tabela de fatos
        fato_enem: DataFrame = df.select(
            "numero_inscricao",
            "codigo_municipio",
            "nota_CN",
            "nota_CH",
            "nota_LC",
            "nota_MT",
            "nota_redacao",
            "NOTA_MEDIA",
            "presenca_CN",
            "presenca_CH",
            "presenca_LC",
            "presenca_MT"
        )

        return dim_aluno, dim_escola, dim_municipio, fato_enem

    def load(self, dim_aluno: DataFrame, dim_escola: DataFrame, dim_municipio: DataFrame, fato_enem: DataFrame, parquet_path: str) -> None:
        """
        Salva os DataFrames como arquivos Parquet no caminho especificado.

        Args:
            dim_aluno (DataFrame): DataFrame da dimensão 'aluno'.
            dim_escola (DataFrame): DataFrame da dimensão 'escola'.
            dim_municipio (DataFrame): DataFrame da dimensão 'municipio'.
            fato_enem (DataFrame): DataFrame da tabela fato 'fato_enem'.
            parquet_path (str): Caminho onde os arquivos Parquet serão salvos.

        Returns:
            None
        """
        dim_aluno.write.parquet(f"{parquet_path}/dim_aluno", mode="overwrite")
        dim_escola.write.parquet(f"{parquet_path}/dim_escola", mode="overwrite")
        dim_municipio.write.parquet(f"{parquet_path}/dim_municipio", mode="overwrite")
        fato_enem.write.parquet(f"{parquet_path}/fato_enem", mode="overwrite")