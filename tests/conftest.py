import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark_session():
    spark = SparkSession.builder.appName("unit_test").master("local[2]").getOrCreate()

    yield spark
    spark.stop()


@pytest.fixture(scope="module")
def sample_ratings_data_averages(spark_session):
    # Create a sample DataFrame for testing
    data = [(1, 101, 4.5), (1, 102, 3.5), (2, 201, 5.0), (2, 202, 2.5)]
    columns = ["MovieID", "UserID", "Rating"]
    return spark_session.createDataFrame(data, columns)


@pytest.fixture(scope="module")
def sample_ratings_data_top_three(spark_session):
    # Create a sample DataFrame for testing find_top_three_movies function
    data = [
        (1, 101, 4.5),
        (1, 102, 3.5),
        (1, 103, 2.5),
        (1, 104, 5.0),
        (2, 201, 3.0),
        (2, 202, 4.0),
        (2, 203, 3.5),
        (2, 204, 2.0),
    ]
    columns = ["UserID", "MovieID", "Rating"]
    return spark_session.createDataFrame(data, columns)
