from pyspark.sql.types import StructType, StructField, IntegerType, LongType
from pyspark.sql import SparkSession
import sys
import json
from pyspark.sql.functions import from_unixtime

sys.path.append("..")
from src.modules.helpers import read_config


def main():
    """
    Main function to clean ratings data and write it to a specified location.
    """
    # Get Spark Session
    spark = SparkSession.builder.appName("ratings_cleaned").getOrCreate()

    try:
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

        # Load raw ratings data into a DataFrame
        ratings_df = (
            spark.read.format("csv")
            .option("sep", "::")
            .schema(ratings_schema)
            .load(f"{raw_path}/ratings.dat")
        )

        # Clean ratings data: Convert Timestamp to timestamp format
        ratings_df = ratings_df.withColumn(
            "Timestamp", from_unixtime("Timestamp").cast("timestamp")
        )

        # Write out the dataframe to the cleaned location in Parquet format
        ratings_df.write.mode("overwrite").parquet(
            f"{cleaned_path}/ratings_cleaned.parquet"
        )

    except IndexError:
        print("Please provide the path to the config file.")
        sys.exit(1)
    except KeyError as e:
        print(f"Missing key in config file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
