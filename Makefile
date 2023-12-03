# Set a variable
LOCAL_PATH := /home/raelwilliamson/personal/movielens_analysis

format:
	black .

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -exec rm -r {} +
	find . -name '.pytest_cache' -type d -exec rm -r {} +

run-all-tests:
	cd tests && pytest

clean-lake-data:
	rm -rf $(LOCAL_PATH)/data/cleaned/*
	rm -rf $(LOCAL_PATH)/data/transformed/*

run-movies-clean-local:
	cd dependencies && \
	python job_submitter.py \
	local $(LOCAL_PATH)/config/local_config.json \
	$(LOCAL_PATH)/src/cleaned/movies_cleaned.py

run-movies-clean-cluster:
	cd dependencies && \
	python job_submitter.py \
	cluster ./config/cluster_config.json \
	./src/cleaned/movies_cleaned.py

run-ratings-clean-local:
	cd dependencies && \
	python job_submitter.py \
	local \
	$(LOCAL_PATH)/config/local_config.json \
	$(LOCAL_PATH)/src/cleaned/ratings_cleaned.py

run-ratings-clean-cluster:
	cd dependencies && \
	python job_submitter.py \
	cluster ./config/cluster_config.json \
	./src/cleaned/ratings_cleaned.py

run-movies-statistics-local:
	cd dependencies && \
	python job_submitter.py \
	local \
	$(LOCAL_PATH)/config/local_config.json \
	$(LOCAL_PATH)/src/transformed/movies_statistics.py

run-movies-statistics-cluster:
	cd dependencies && \
	python job_submitter.py \
	cluster ./config/cluster_config.json \
	./src/transformed/movies_statistics.py

run-users-top-three-movies-local:
	cd dependencies && \
	python job_submitter.py \
	local \
	$(LOCAL_PATH)/config/local_config.json \
	$(LOCAL_PATH)/src/transformed/users_top_three_movies.py

run-users-top-three-movies-cluster:
	cd dependencies && \
	python job_submitter.py \
	cluster ./config/cluster_config.json \
	./src/transformed/users_top_three_movies.py

run-pipeline-local:
	make run-movies-clean-local && \
	make run-ratings-clean-local && \
	make run-movies-statistics-local && \
	make run-users-top-three-movies-local

run-pipeline-cluster:
	make run-movies-clean-cluster && \
	make run-ratings-clean-cluster && \
	make run-movies-statistics-cluster && \
	make run-users-top-three-movies-cluster

