from pyspark.sql import SparkSession, functions as F
from pyspark.sql.functions import col

class ETL:
    
    def extract(self, spark, file_path):
        """Extrai os dados do arquivo CSV."""
        df = spark.read \
            .option("delimiter", ";") \
            .option("header", "true") \
            .option("encoding", "ISO-8859-1") \
            .csv(file_path)
        return df

    def transform(self, df):
        """Transforma os dados e retorna DataFrames para as tabelas dim e fato."""
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
        df = df.withColumn("NOTA_MEDIA", 
                          (col("nota_MT") + col("nota_CN") + col("nota_CH") + col("nota_LC") + col("nota_redacao")) / 5)

        # Cria os DataFrames para as tabelas dimensionais e de fatos
        dim_aluno = df.select(
            "numero_inscricao",
            "sexo",
            "etnia",
            "situacao_conclusao"
        ).distinct()  # Remove duplicatas

        dim_escola = df.select(
            "codigo_municipio",
            "nom_municipio",
            "estado"
        ).distinct()  # Remove duplicatas

        dim_municipio = df.select(
            "codigo_municipio",
            "nom_municipio",
            "estado"
        ).distinct()  # Remove duplicatas

        # Tabela de fatos
        fato_enem = df.select(
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

    def load(self, dim_aluno, dim_escola, dim_municipio, fato_enem, parquet_path):
        """Salva os DataFrames como arquivos Parquet."""
        dim_aluno.write.parquet(f"{parquet_path}/dim_aluno", mode="overwrite")
        dim_escola.write.parquet(f"{parquet_path}/dim_escola", mode="overwrite")
        dim_municipio.write.parquet(f"{parquet_path}/dim_municipio", mode="overwrite")
        fato_enem.write.parquet(f"{parquet_path}/fato_enem", mode="overwrite")


# class ETL:
    
#     def extract(self, spark, file_path):
#         df = spark.read \
#             .option("delimiter", ";") \
#             .option("header", "true") \
#             .option("encoding", "ISO-8859-1") \
#             .csv(file_path)
#         return df


#     def transform(self, df, col):
#         df = df.select(
#             col("NU_INSCRICAO").cast("string"),
#             col("TP_SEXO").cast("string"),
#             col("TP_COR_RACA").cast("integer"),
#             col("CO_MUNICIPIO_ESC").cast("integer"),
#             col("NO_MUNICIPIO_ESC").cast("string"),
#             col("SG_UF_ESC").cast("string"),
#             col("TP_PRESENCA_CN").cast("integer"),
#             col("TP_PRESENCA_CH").cast("integer"),
#             col("TP_PRESENCA_LC").cast("integer"),
#             col("TP_PRESENCA_MT").cast("integer"),
#             col("NU_NOTA_CN").cast("double"),
#             col("NU_NOTA_CH").cast("double"),
#             col("NU_NOTA_LC").cast("double"),
#             col("NU_NOTA_MT").cast("double"),
#             col("NU_NOTA_REDACAO").cast("string"),
#             col("TP_ST_CONCLUSAO").cast("integer")
#         )
        
    
#         df = df.withColumn("NOTA_MEDIA", (col("NU_NOTA_MT") + col("NU_NOTA_CN") + col("NU_NOTA_CH") + col("NU_NOTA_LC") + col("NU_NOTA_REDACAO")) / 5)

#         nomes_novos = {
#             'NU_INSCRICAO':'numero_inscricao', 
#             'TP_SEXO':'sexo', 
#             'TP_COR_RACA':'etnia', 
#             'CO_MUNICIPIO_ESC':'codigo_municipio', 
#             'NO_MUNICIPIO_ESC':'nom_municipio', 
#             'SG_UF_ESC':'estado', 
#             'TP_PRESENCA_CN':'presenca_CN', 
#             'TP_PRESENCA_CH':'presenca_CH', 
#             'TP_PRESENCA_LC':'presenca_LC', 
#             'TP_PRESENCA_MT':'presenca_MT', 
#             'NU_NOTA_CN':'nota_CN', 
#             'NU_NOTA_CH':'nota_CH', 
#             'NU_NOTA_LC':'nota_LC', 
#             'NU_NOTA_MT':'nota_MT', 
#             'NU_NOTA_REDACAO':'nota_redacao', 
#             'TP_ST_CONCLUSAO':'situacao_conclusao'}
        
#         for key, value in nomes_novos.items():
#             df = df.withColumnRenamed(key, value)
        
#         return df


#     def load(self, df, parquet_path):
#         df.write.parquet(parquet_path, mode="overwrite")