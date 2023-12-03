from pyspark.sql.types import DoubleType
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, max, min, avg, round
import sys
import json

sys.path.append("..")
from src.modules.helpers import read_config


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
    spark = SparkSession.builder.appName("movies_cleaned").getOrCreate()

    try:
        # Get the config file path passed via spark-submit
        config = read_config(sys.argv[1])
        cleaned_path = config["cleaned_path"]
        transformed_path = config["transformed_path"]

        # Read cleaned data from lake
        movies_cleaned_df = spark.read.parquet(f"{cleaned_path}/movies_cleaned.parquet")
        ratings_cleaned_df = spark.read.parquet(
            f"{cleaned_path}/ratings_cleaned.parquet"
        )

        # Get summarised ratings data
        summarised_ratings_df = summarise_ratings(ratings_cleaned_df)

        # Join summarised ratings data with movie data
        movies_with_ratings = movies_cleaned_df.join(
            summarised_ratings_df, "MovieId", "left"
        )

        # Write out the dataframe to the lake transformed location
        movies_with_ratings.write.mode("overwrite").parquet(
            f"{transformed_path}/question_2.parquet"
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
