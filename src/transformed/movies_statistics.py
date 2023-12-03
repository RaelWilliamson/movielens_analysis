from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType
from pyspark.sql.types import DoubleType
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, max, min, avg, round
import sys
import logging

sys.path.append("..")
from src.modules.helpers import read_config

# Set up logging configurations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def summarise_ratings(df):
    """
    Summarizes ratings data by calculating max, min, and average ratings per movie.

    Args:
    - df (DataFrame): Input DataFrame containing ratings data.

    Returns:
    - DataFrame: DataFrame with aggregated summary statistics for ratings by movie.
    """
    summary_df = df.groupBy("MovieID").agg(
        max(col("Rating")).alias("max_rating"),
        min(col("Rating")).alias("min_rating"),
        round(avg(col("Rating")), 2).cast(DoubleType()).alias("avg_rating"),
    )
    return summary_df


def main():
    """
    Main function to process movie and ratings data, summarize ratings, and save results.
    """
    # Get Spark Session
    spark = SparkSession.builder.appName("movies_statistics").getOrCreate()

    # Define schemas for read
    movies_schema = StructType(
        [
            StructField("MovieId", IntegerType(), True),
            StructField("Title", StringType(), True),
            StructField("Genres", StringType(), True),
        ]
    )

    ratings_schema = StructType(
        [
            StructField("UserID", IntegerType(), True),
            StructField("MovieID", IntegerType(), True),
            StructField("Rating", IntegerType(), True),
            StructField("Timestamp", LongType(), True),
        ]
    )

    try:
        # Get the config file path passed via spark-submit
        config = read_config(sys.argv[1])
        cleaned_path = config["cleaned_path"]
        transformed_path = config["transformed_path"]

        logger.info("Calculating movie statistics...")

        # Read cleaned data from lake
        movies_cleaned_df = (
            spark.read.format("parquet")
            .schema(movies_schema)
            .load(f"{cleaned_path}/movies_cleaned.parquet")
        )
        ratings_cleaned_df = (
            spark.read.format("parquet")
            .schema(ratings_schema)
            .load(f"{cleaned_path}/ratings_cleaned.parquet")
        )

        logger.info(f"Read {movies_cleaned_df.count()} rows from movies data")
        logger.info(f"Read {ratings_cleaned_df.count()} rows from ratings data")

        # Get summarised ratings data
        logger.info("Generating movie summary statistics")
        summarised_ratings_df = summarise_ratings(ratings_cleaned_df)

        # Join summarised ratings data with movie data
        logger.info("Adding move dimension data")
        movies_with_ratings = movies_cleaned_df.join(
            summarised_ratings_df, "MovieId", "left"
        )

        logger.info(
            f"Writing results to datalake at {transformed_path}/movies_statistics.parquet"
        )

        # Write out the dataframe to the lake transformed location
        movies_with_ratings.write.mode("overwrite").parquet(
            f"{transformed_path}/movies_statistics.parquet"
        )

        logger.info(f"Writen {movies_with_ratings.count()} rows as output")

        logger.info("Generating movie statistics completed.")

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
