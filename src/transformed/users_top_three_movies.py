from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, row_number
from pyspark.sql.window import Window
import sys
import logging

sys.path.append("..")
from src.modules.helpers import read_config

# Set up logging configurations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_top_three_movies(df):
    """
    Finds the top three movies for each user based on their ratings.

    Args:
    - df (DataFrame): Input DataFrame containing ratings data.

    Returns:
    - DataFrame: DataFrame containing each user's top 3 movies based on rating.
    """
    windowSpec = Window.partitionBy("UserID").orderBy(col("Rating").desc())
    ranked_df = df.withColumn("rank", row_number().over(windowSpec))
    top3_movies_per_user = ranked_df.filter(col("rank") <= 3).drop("rank")
    return top3_movies_per_user


def main():
    """
    Main function to find top 3 movies per user based on ratings and save results.
    """
    # Get Spark Session
    spark = SparkSession.builder.appName("users_top_three_movies").getOrCreate()

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

        logger.info("Calculating users top three movies based on ratings...")

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

        logger.info(f'Read {movies_cleaned_df.count()} rows from movies data')
        logger.info(f'Read {ratings_cleaned_df.count()} rows from ratings data')

        # Create DataFrame with top 3 movies per user
        logger.info("Finding top three movies")
        ranked_movies = find_top_three_movies(ratings_cleaned_df)

        # Join with movie details and select necessary columns
        logger.info("Adding movie data and selecting desired fields")
        ranked_movies_with_details = ranked_movies.join(
            movies_cleaned_df, "MovieId", "left"
        )
        final_df = ranked_movies_with_details.select("UserID", "Title", "Rating")

        logger.info(
            f"Writing results to datalake at {transformed_path}/users_top_three_movies.parquet"
        )

        # Write out the dataframe to the lake transformed location
        final_df.write.mode("overwrite").parquet(
            f"{transformed_path}/users_top_three_movies.parquet"
        )

        logger.info(f"Writen {final_df.count()} rows as output")

        logger.info("Calculating users top three movies based on ratings completed.")

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
