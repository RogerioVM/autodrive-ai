# spark_processor.py
from pyspark.sql import SparkSession

def process_file(file_path):
    spark = SparkSession.builder.appName("AutoDriveAI").getOrCreate()

    # Detecta o tipo do arquivo
    if file_path.endswith('.csv'):
        df = spark.read.option("header", True).csv(file_path)
    else:
        print("Formato ainda não suportado.")
        return

    # Exemplo: contar registros
    print("[SPARK] Linhas no arquivo:", df.count())

    # Aqui você pode aplicar transformações com PySpark
    df.show(5)

    spark.stop()
    