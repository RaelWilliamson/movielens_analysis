# Intro

This project looks to consume data from the [movielens](http://files.grouplens.org/datasets/movielens/ml-1m.zip) data set, specifically movies and ratings data. This data is consumed, cleaned and tranformed to produce to output tables, these being:

- A movie table with min_rating, max_rating and average_rating for each movie
- A table showing each users top three rated movies

# Prerequisites 

1. The project uses **Poetry** for dependency and venv management.
2. The project additionally uses **Docker** for standing up a Spark cluster to submit jobs. These two tools are required in order to start the project.
3. The project uses spark locally so spark should be installed
4. Data is downloaded and placed in `data/raw` location in the root of the folder
5. In the makefile at the root level, change *LOCAL_PATH* to your path
6. In the local config file, change the path to the raw data to reflect your path

Getting started: 

## Starting a poetry shell (venv) and installing dependencies

​``` 
Poetry Shell
Poetry Install
​```
## Standing up a spark cluster using docker (if not running code locally)

Setting up the spark cluster involves building a docker container and then using docker compose to define a set of compute instances (worker, history and master). Data and scripts are copied across as volumes which are required for submitting and running jobs.

Navigate to the infra folder using ` cd infra` and run the following commands:

​``` 
make build
nake run
​```

Once the above has been completed you should be able to see the docker containers running.

# Project Overview

In order to replicate a data engineering environment where data is consumed and moved through ETL phases, the following steps were followed and will be expanded on in more detail:

1. Initial EDA to understand data (fields, quality)
2. Data Cleaning (preparing the data set for transformation)
3. Data Transforamtion (produces two output tables)
4. Simple data visualisation to validate the output and explore the data

## 1. Initial EDA

The initial EDA was performed using jupyter notebooks and pandas. The result of this activity determined the schema and any data cleaning required. The outputs can be found in the **eda** folder in **data_analysis.ipynb**. 

## 2. Data Cleaning

The following steps were performed on the raw data:

1. Headers were added
2. Formats were changed (unix timestamp to datetime)
3. Outputs cleaned data saved as parquet file

## 3. Data Transformation

In the transformation phase, the cleaned data is ingested and transformed to produce the two resulting datasets

## 4. Simple Data Viz

This activity was performed using jupyter notebooks and pandas. Graphs were generated using pyplot. The outputs can be found in the **eda** folder in **data_viz.ipynb**

# Usage

The following steps describe the process of running the ETL jobs. 

## Project Structure

The repo is structured using the following considerations:

1. A config file to define local and cluster variables. These files are found in *config* folder
2. A job submitter, which handles whether jobs are run locally or submitted to a cluster. This is found in the *dependencies* folder
3. All ETL jobs and helper functions are found in the *src* folder and grouped by the different activites and underlying lake structure
4. The "data lake" is structured to contain three levels (raw, cleaned and transformed) with respective dating being written in those locations associated with those tasks
5. Testing is performed using pytest and fixtures for data. The testing can be found in the *tests* folder
6. The code to build and deploy the spark cluster can be found in the *infra* folder
7. Makefiles are used to run commands and orchestrate the ETL jobs

## Running the code

There are two possible option: **Local** and **Cluster**. In order to use the cluster option, ensure that the cluster is running in docker.

### Running the ETL jobs

You can either run the ETL jobs on their own, or in one go. The following make commands are avaiable:

Local:

- ` make run-movies-clean-local`
- ` make run-ratings-clean-local`
- ` make run-movies-statistics-local`
- ` make run-users-top-three-movies-local`
- ` make run-pipeline-local`

Cluster:

- ` make run-movies-clean-cluster`
- ` make run-ratings-clean-cluster`
- ` make run-movies-statistics-cluster`
- ` make run-users-top-three-movies-cluster`
- ` make run-pipeline-cluster`

### Development

There are several commands used for easier development.

 - Black is used for code formatting: ` make format`
 - Repo cleaning: ` make clean`
 - Cleaning "data lake" files: ` make clean-lake-data`
 - Unit testing: ` make run-all-tests`




