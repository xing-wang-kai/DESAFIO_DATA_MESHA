# Usar uma imagem base com Python e Spark
FROM bitnami/spark:3.5.0

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto para o contêiner
COPY . .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl
RUN apk add --no-cache curl
# Instalar o MySQL Connector/J para o Spark
RUN curl -O https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.26/mysql-connector-java-8.0.26.jar && \
    mv mysql-connector-java-8.0.26.jar /opt/bitnami/spark/jars/

# Definir variáveis de ambiente para o Spark
ENV SPARK_HOME=/opt/bitnami/spark
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.7-src.zip:$PYTHONPATH
ENV PATH=$SPARK_HOME/bin:$PATH

# Expor a porta do Spark UI (opcional)
EXPOSE 4040

# Comando padrão para executar o Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]