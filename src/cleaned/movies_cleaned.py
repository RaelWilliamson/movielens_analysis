from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql import SparkSession
import sys
import logging

sys.path.append("..")
from src.modules.helpers import read_config

# Set up logging configurations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

        logger.info("Cleaning movie data...")

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

        logger.info(
            f"Writing results to datalake at {cleaned_path}/movies_cleaned.parquet"
        )

        # Write out the dataframe to the cleaned location in Parquet format
        movies_df.coalesce(1).write.mode("overwrite").format("parquet").save(
            f"{cleaned_path}/movies_cleaned.parquet"
        )

        logger.info(f"Writen {movies_df.count()} rows as output")

        logger.info("Movie data cleaning completed.")

    except IndexError:
        logger.error("Please provide the path to the config file.")
        sys.exit(1)
    except KeyError as e:
        logger.error(f"Missing key in config file: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
