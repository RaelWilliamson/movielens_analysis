from pyspark.sql import SparkSession
from pyspark.sql.functions import col, row_number
from pyspark.sql.window import Window
import sys
import json

sys.path.append("..")
from src.modules.helpers import read_config


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
    spark = SparkSession.builder.appName("movies_cleaned").getOrCreate()

    try:
        # Get the config file path passed via spark-submit
        config = read_config(sys.argv[1])
        cleaned_path = config["cleaned_path"]
        transformed_path = config["transformed_path"]

        # Read cleaned data from lake
        ratings_cleaned_df = spark.read.parquet(
            f"{cleaned_path}/ratings_cleaned.parquet"
        )
        movies_cleaned_df = spark.read.parquet(f"{cleaned_path}/movies_cleaned.parquet")

        # Create DataFrame with top 3 movies per user
        ranked_movies = find_top_three_movies(ratings_cleaned_df)

        # Join with movie details and select necessary columns
        ranked_movies_with_details = ranked_movies.join(
            movies_cleaned_df, "MovieId", "left"
        )
        final_df = ranked_movies_with_details.select("UserID", "Title", "Rating")

        # Write out the dataframe to the lake transformed location
        final_df.write.mode("overwrite").parquet(
            f"{transformed_path}/users_top_three_movies.parquet"
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
