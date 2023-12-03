build:
	docker-compose build

down:
	docker-compose down --volumes --remove-orphans

run:
	make down && docker-compose up

stop:
	docker-compose stop

submit:
	docker exec da-spark-master spark-submit --master spark://spark-master:7077 --deploy-mode client ./apps/$(app)