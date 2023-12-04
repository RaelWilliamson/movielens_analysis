build-yarn:
	docker-compose -f docker-compose.yml build

down-yarn:
	docker-compose -f docker-compose.yml down --volumes --remove-orphans

run-yarn:
	make down-yarn && docker-compose -f docker-compose.yml up

run-yarn-scaled:
	make down-yarn && docker-compose -f docker-compose.yml up --scale spark-yarn-worker=3

submit-yarn-test:
	docker exec da-spark-yarn-master spark-submit --master yarn --deploy-mode cluster ./examples/src/main/python/pi.py