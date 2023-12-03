from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql import SparkSession
import sys
import json


def read_config(config_path):
    with open(config_path, "r") as file:
        return json.load(file)


def main():
    # Get Spark Context
    spark = SparkSession.builder.appName("movies_cleaned").getOrCreate()

    # Get the config file path passed via spark-submit
    config = read_config(sys.argv[1])
    raw_path = config["raw_path"]
    cleaned_path = config["cleaned_path"]

    # Define Movies Schema
    movies_schema = StructType(
        [
            StructField("MovieId", IntegerType(), True),
            StructField("Title", StringType(), True),
            StructField("Genres", StringType(), True),
        ]
    )

    movies_df = (
        spark.read.format("csv")
        .option("sep", "::")
        .schema(movies_schema)
        .load(f"{raw_path}/movies.dat")
    )

    # Write out the dataframe to the lake cleaned location
    movies_df.write.mode("overwrite").parquet(f"{cleaned_path}/movies_cleaned.parquet")


if __name__ == "__main__":
    main()
