
class Answer:
    
    def __init__(self, spark, dim_aluno, dim_escola, dim_municipio, fato_enem):
        self.spark = spark
        self.dim_aluno = dim_aluno
        self.dim_escola = dim_escola
        self.dim_municipio = dim_municipio
        self.fato_enem = fato_enem

        # Cria views temporárias para as tabelas
        self.dim_aluno.createOrReplaceTempView("dim_aluno")
        self.dim_escola.createOrReplaceTempView("dim_escola")
        self.dim_municipio.createOrReplaceTempView("dim_municipio")
        self.fato_enem.createOrReplaceTempView("fato_enem")
        
    def get_top_school(self):
        """Retorna a escola com a maior média de notas."""
        top_school = self.spark.sql("""
            SELECT
                e.nom_municipio AS escola,
                e.estado,
                AVG(f.nota_CN + f.nota_CH + f.nota_LC + f.nota_MT + f.nota_redacao) / 5 AS media_escola
            FROM
                fato_enem f
            JOIN dim_escola e ON f.codigo_municipio = e.codigo_municipio
            WHERE
                f.nota_CN IS NOT NULL
                AND f.nota_CH IS NOT NULL
                AND f.nota_LC IS NOT NULL
                AND f.nota_MT IS NOT NULL
                AND f.nota_redacao IS NOT NULL
            GROUP BY
                e.nom_municipio, e.estado
            ORDER BY
                media_escola DESC
            LIMIT 1
        """)
        return top_school

    def get_top_student(self):
        """Retorna o aluno com a maior média de notas."""
        top_student = self.spark.sql("""
            SELECT
                a.numero_inscricao,
                a.sexo,
                a.etnia,
                AVG(f.nota_CN + f.nota_CH + f.nota_LC + f.nota_MT + f.nota_redacao) / 5 AS media_notas
            FROM
                fato_enem f
            JOIN dim_aluno a ON f.numero_inscricao = a.numero_inscricao
            WHERE
                f.nota_CN IS NOT NULL
                AND f.nota_CH IS NOT NULL
                AND f.nota_LC IS NOT NULL
                AND f.nota_MT IS NOT NULL
                AND f.nota_redacao IS NOT NULL
            GROUP BY
                a.numero_inscricao, a.sexo, a.etnia
            ORDER BY
                media_notas DESC
            LIMIT 1
        """)
        return top_student

    def get_average_score(self):
        """Retorna a média geral das notas."""
        average_score = self.spark.sql("""
            SELECT
                AVG(f.nota_CN + f.nota_CH + f.nota_LC + f.nota_MT + f.nota_redacao) / 5 AS media_geral
            FROM
                fato_enem f
            WHERE
                f.nota_CN IS NOT NULL
                AND f.nota_CH IS NOT NULL
                AND f.nota_LC IS NOT NULL
                AND f.nota_MT IS NOT NULL
                AND f.nota_redacao IS NOT NULL
        """)
        return average_score

    def get_absent_percentage(self):
        """Retorna o percentual de ausentes."""
        absent_percentage = self.spark.sql("""
                                           
            SELECT
                COUNT(f.numero_inscricao) * 100.0 / (SELECT COUNT(*) FROM fato_enem) AS percentual_ausentes
            FROM
                fato_enem f
            WHERE
                f.presenca_CN = 0
                OR f.presenca_CH = 0
                OR f.presenca_LC = 0
                OR f.presenca_MT = 0
        """)
        return absent_percentage

    def get_total_students(self):
        """Retorna o número total de inscritos."""
        total_students = self.spark.sql("""
            SELECT
                COUNT(*) AS total_inscritos
            FROM
                fato_enem
        """)
        return total_students

    def get_average_by_discipline(self):
        """Retorna a média por disciplina."""
        average_by_discipline = self.spark.sql("""
            SELECT
                AVG(f.nota_CN) AS media_CN,
                AVG(f.nota_CH) AS media_CH,
                AVG(f.nota_LC) AS media_LC,
                AVG(f.nota_MT) AS media_MT,
                AVG(f.nota_redacao) AS media_redacao
            FROM
                fato_enem f
            WHERE
                f.nota_CN IS NOT NULL
                AND f.nota_CH IS NOT NULL
                AND f.nota_LC IS NOT NULL
                AND f.nota_MT IS NOT NULL
                AND f.nota_redacao IS NOT NULL
        """)
        return average_by_discipline

    def get_average_by_gender(self):
        """Retorna a média por sexo."""
        average_by_gender = self.spark.sql("""
            SELECT
                a.sexo,
                AVG(f.nota_CN + f.nota_CH + f.nota_LC + f.nota_MT + f.nota_redacao) / 5 AS media_sexo
            FROM
                fato_enem f
            JOIN dim_aluno a ON f.numero_inscricao = a.numero_inscricao
            WHERE
                f.nota_CN IS NOT NULL
                AND f.nota_CH IS NOT NULL
                AND f.nota_LC IS NOT NULL
                AND f.nota_MT IS NOT NULL
                AND f.nota_redacao IS NOT NULL
            GROUP BY
                a.sexo
        """)
        return average_by_gender

    def get_average_by_ethnicity(self):
        """Retorna a média por etnia."""
        average_by_ethnicity = self.spark.sql("""
            SELECT
                a.etnia,
                AVG(f.nota_CN + f.nota_CH + f.nota_LC + f.nota_MT + f.nota_redacao) / 5 AS media_etnia
            FROM
                fato_enem f
            JOIN dim_aluno a ON f.numero_inscricao = a.numero_inscricao
            WHERE
                f.nota_CN IS NOT NULL
                AND f.nota_CH IS NOT NULL
                AND f.nota_LC IS NOT NULL
                AND f.nota_MT IS NOT NULL
                AND f.nota_redacao IS NOT NULL
            GROUP BY
                a.etnia
        """)
        return average_by_ethnicity



# class Answer:
    
#     def __init__(self, spark, df):
#         self.df = df
#         self.spark = spark
#         self.df.createOrReplaceTempView("enem_view")
        
#     def get_top_school(self):
        
#         top_school = self.spark.sql("""
#             SELECT
#                 codigo_municipio,
#                 nom_municipio,
#                 estado,
#                 AVG((nota_CN + nota_CH + nota_LC + nota_MT + nota_redacao) / 5) AS media_escola
#             FROM
#                 enem_view
#             WHERE 
#                 nota_CN IS NOT NULL
#                 AND nota_CH IS NOT NULL
#                 AND nota_LC IS NOT NULL
#                 AND nota_MT IS NOT NULL
#                 AND nota_redacao IS NOT NULL
#             GROUP BY 
#                 codigo_municipio,
#                 nom_municipio,
#                 estado
#             ORDER BY 
#                 media_escola DESC
#             LIMIT 1
#         """)
#         return top_school

#     def get_top_student(self):
        
#         top_student = self.spark.sql("""
#             SELECT
#                 numero_inscricao,
#                 AVG((nota_CN + nota_CH + nota_LC + nota_MT + nota_redacao) / 5) AS media_notas
#             FROM
#                 enem_view
#             WHERE
#                 nota_CN IS NOT NULL
#                 AND nota_CH IS NOT NULL
#                 AND nota_LC IS NOT NULL
#                 AND nota_MT IS NOT NULL
#                 AND nota_redacao IS NOT NULL
#             GROUP BY
#                 numero_inscricao
#             ORDER BY
#                 media_notas DESC
#             LIMIT 1
#         """)
#         return top_student

#     def get_average_score(self):
        
#         average_score = self.spark.sql("""
#             SELECT
#                 AVG((nota_CN + nota_CH + nota_LC + nota_MT + nota_redacao) / 5) AS media_geral
#             FROM
#                 enem_view
#             WHERE
#                 nota_CN IS NOT NULL
#                 AND nota_CH IS NOT NULL
#                 AND nota_LC IS NOT NULL
#                 AND nota_MT IS NOT NULL
#                 AND nota_redacao IS NOT NULL
#         """)
#         return average_score

#     def get_absent_percentage(self):
        
#         absent_percentage = self.spark.sql("""
#             SELECT
#                 COUNT(numero_inscricao) AS quantidade_ausentes
#             FROM
#                 enem_view
#             WHERE 
#                     presenca_CN = 0
#                 OR
#                     presenca_CH = 0
#                 OR
#                     presenca_LC = 0
#                 OR
#                     presenca_MT = 0;
#         """)
#         return absent_percentage

#     def get_total_students(self):
        
#         total_students = self.spark.sql("""
#             SELECT
#                 COUNT(*) AS total_inscritos
#             FROM
#                 enem_view
#         """)
#         return total_students

#     def get_average_by_discipline(self):
        
#         average_by_discipline = self.spark.sql("""
#             SELECT
#                 AVG(nota_CN) AS media_CN,
#                 AVG(nota_CH) AS media_CH,
#                 AVG(nota_LC) AS media_LC,
#                 AVG(nota_MT) AS media_MT,
#                 AVG(nota_redacao) AS media_redacao
#             FROM
#                 enem_view
#             WHERE
#                 nota_CN IS NOT NULL
#                 AND nota_CH IS NOT NULL
#                 AND nota_LC IS NOT NULL
#                 AND nota_MT IS NOT NULL
#                 AND nota_redacao IS NOT NULL
#         """)
#         return average_by_discipline

#     def get_average_by_gender(self):
        
#         average_by_gender = self.spark.sql("""
#             SELECT
#                 sexo,
#                 AVG((nota_CN + nota_CH + nota_LC + nota_MT + nota_redacao) / 5) AS media_sexo
#             FROM
#                 enem_view
#             WHERE
#                 nota_CN IS NOT NULL
#                 AND nota_CH IS NOT NULL
#                 AND nota_LC IS NOT NULL
#                 AND nota_MT IS NOT NULL
#                 AND nota_redacao IS NOT NULL
#             GROUP BY
#                 sexo
#         """)
#         return average_by_gender

#     def get_average_by_ethnicity(self):
        
#         average_by_ethnicity = self.spark.sql("""
#             SELECT
#                 etnia,
#                 AVG((nota_CN + nota_CH + nota_LC + nota_MT + nota_redacao) / 5) AS media_etnia
#             FROM
#                 enem_view
#             WHERE
#                 nota_CN IS NOT NULL
#                 AND nota_CH IS NOT NULL
#                 AND nota_LC IS NOT NULL
#                 AND nota_MT IS NOT NULL
#                 AND nota_redacao IS NOT NULL
#             GROUP BY
#                 etnia
#         """)
#         return average_by_ethnicity