from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql import SparkSession
import sys

sys.path.append("..")
from src.modules.helpers import read_config


def main():
    """
    Main function to execute Spark job for cleaning movie data.
    """
    # Get Spark Session
    spark = SparkSession.builder.appName("movies_cleaned").getOrCreate()

    try:
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

        # Load raw movie data into a DataFrame
        movies_df = (
            spark.read.format("csv")
            .option("sep", "::")
            .schema(movies_schema)
            .load(f"{raw_path}/movies.dat")
        )

        # Write out the dataframe to the cleaned location in Parquet format
        movies_df.write.mode("overwrite").parquet(
            f"{cleaned_path}/movies_cleaned.parquet"
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
