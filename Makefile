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

run-question-2-local:
	cd dependencies && \
	python job_submitter.py \
	local \
	$(ROOT_PATH)/config/local_config.json \
	$(ROOT_PATH)/src/transformed/question_2.py

run-question-3-local:
	cd dependencies && \
	python job_submitter.py \
	local \
	$(ROOT_PATH)/config/local_config.json \
	$(ROOT_PATH)/src/transformed/question_3.py

run-pipeline-question_2:
	make run-movies-clean-local && \
	make run-ratings-clean-local && \
	make run-question-2-local

run-pipeline-question_3:
	make run-movies-clean-local && \
	make run-ratings-clean-local && \
	make run-question-3-local

