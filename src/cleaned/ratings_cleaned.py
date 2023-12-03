from pyspark.sql.types import StructType, StructField, IntegerType, LongType
from pyspark.sql import SparkSession
import sys
import json
from pyspark.sql.functions import from_unixtime


def read_config(config_path):
    with open(config_path, "r") as file:
        return json.load(file)


def main():
    # Get Spark Context
    spark = SparkSession.builder.appName("ratings_cleaned").getOrCreate()

    # Get the config file path passed via spark-submit
    config = read_config(sys.argv[1])
    raw_path = config["raw_path"]
    cleaned_path = config["cleaned_path"]

    # Define Ratings Schema
    ratings_schema = StructType(
        [
            StructField("UserID", IntegerType(), True),
            StructField("MovieID", IntegerType(), True),
            StructField("Rating", IntegerType(), True),
            StructField("Timestamp", LongType(), True),
        ]
    )

    ratings_df = (
        spark.read.format("csv")
        .option("sep", "::")
        .schema(ratings_schema)
        .load(f"{raw_path}/ratings.dat")
    )

    # Clean ratings data
    ratings_df = ratings_df.withColumn(
        "Timestamp", from_unixtime("Timestamp").cast("timestamp")
    )

    # Write out the dataframe to the lake cleaned location
    ratings_df.write.mode("overwrite").parquet(
        f"{cleaned_path}/ratings_cleaned.parquet"
    )


if __name__ == "__main__":
    main()
