from src.transformed.movies_statistics import summarise_ratings
from src.transformed.users_top_three_movies import find_top_three_movies


def test_summarise_ratings(sample_ratings_data_averages):
    # Perform the summarization on the sample data
    summary_df = summarise_ratings(sample_ratings_data_averages)

    # Check if the DataFrame has the expected columns
    expected_columns = ["MovieID", "max_rating", "min_rating", "avg_rating"]
    assert all(col in summary_df.columns for col in expected_columns)

    # Check if the summarization logic is correct for the sample data
    expected_result = [(1, 4.5, 3.5, 4.0), (2, 5.0, 2.5, 3.75)]
    for row in expected_result:
        movie_id = row[0]
        assert summary_df.filter(summary_df.MovieID == movie_id).collect()[0] == row


def test_find_top_three_movies(sample_ratings_data_top_three):
    # Perform the top three movies calculation on the sample data
    top_three_movies_df = find_top_three_movies(sample_ratings_data_top_three)

    # Check if the DataFrame has the expected columns
    expected_columns = ["UserID", "MovieID", "Rating"]
    assert all(col in top_three_movies_df.columns for col in expected_columns)

    # Check for each user if the top three movies are as expected
    expected_results = {
        1: [(104, 5.0), (101, 4.5), (102, 3.5)],
        2: [(202, 4.0), (203, 3.5), (201, 3.0)],
    }
    for user_id, movies in expected_results.items():
        user_movies = top_three_movies_df.filter(
            top_three_movies_df.UserID == user_id
        ).collect()
        for index, movie_info in enumerate(movies):
            assert (user_movies[index].MovieID, user_movies[index].Rating) == movie_info
