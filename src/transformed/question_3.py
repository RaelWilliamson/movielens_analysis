from pyspark.sql import SparkSession
from pyspark.sql.functions import col, row_number
from pyspark.sql.window import Window
import sys
import json


def read_config(config_path):
    with open(config_path, "r") as file:
        return json.load(file)


def find_top_three_movies(df):
    # Define a window partitioned by userId and ordered by rating in descending order
    windowSpec = Window.partitionBy("UserId").orderBy(col("Rating").desc())
    # Add a row number to each row within the window partition
    ranked_df = df.withColumn("rank", row_number().over(windowSpec))
    # Filter the DataFrame to keep only the top 3 movies per user
    top3_movies_per_user = ranked_df.filter(col("rank") <= 3).drop("rank")

    return top3_movies_per_user


def main():
    # Get Spark Context
    spark = SparkSession.builder.appName("movies_cleaned").getOrCreate()

    # Get the config file path passed via spark-submit
    config = read_config(sys.argv[1])
    cleaned_path = config["cleaned_path"]
    transformed_path = config["transformed_path"]

    # Read cleaned data from lake
    ratings_cleaned_df = spark.read.parquet(f"{cleaned_path}/ratings_cleaned.parquet")
    movies_cleaned_df = spark.read.parquet(f"{cleaned_path}/movies_cleaned.parquet")

    # Create a new dataframe which contains each user’s (userId in the ratings data) top 3 movies based on their rating.
    ranked_movies = find_top_three_movies(ratings_cleaned_df)

    # Join with Movies data and clean output
    ranked_movies_with_details = ranked_movies.join(
        movies_cleaned_df, "MovieId", "left"
    )
    final_df = ranked_movies_with_details.select("UserID", "Title", "Rating")

    # Write out the dataframe to the lake transformed location
    final_df.write.mode("overwrite").parquet(f"{transformed_path}/question_3.parquet")


if __name__ == "__main__":
    main()
