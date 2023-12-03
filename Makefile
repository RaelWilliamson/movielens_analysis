# Set a variable
ROOT_PATH := /home/raelwilliamson/personal/movielens_analysis

format:
	black .

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -exec rm -r {} +
	find . -name '.pytest_cache' -type d -exec rm -r {} +

run-all-tests:
	cd tests && pytest

clean-lake-data:
	rm -rf $(ROOT_PATH)/data/cleaned/*
	rm -rf $(ROOT_PATH)/data/transformed/*

run-movies-clean-local:
	cd dependencies && \
	python job_submitter.py \
	local $(ROOT_PATH)/config/local_config.json \
	$(ROOT_PATH)/src/cleaned/movies_cleaned.py

run-ratings-clean-local:
	cd dependencies && \
	python job_submitter.py \
	local \
	$(ROOT_PATH)/config/local_config.json \
	$(ROOT_PATH)/src/cleaned/ratings_cleaned.py

run-movies-statistics-local:
	cd dependencies && \
	python job_submitter.py \
	local \
	$(ROOT_PATH)/config/local_config.json \
	$(ROOT_PATH)/src/transformed/movies_statistics.py

run-users-top-three-movies-local:
	cd dependencies && \
	python job_submitter.py \
	local \
	$(ROOT_PATH)/config/local_config.json \
	$(ROOT_PATH)/src/transformed/users_top_three_movies.py

run-pipeline-local:
	make run-movies-clean-local && \
	make run-ratings-clean-local && \
	make run-movies-statistics-local && \
	make run-users-top-three-movies-local
	

