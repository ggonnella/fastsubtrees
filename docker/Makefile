default:
	@echo "make image        build Docker image"
	@echo "make container    create and run Docker container"
	@echo "make shell        interactive shell in Docker container"

.PHONY: image container shell start_server create_test_db test

IMAGE_NAME = "fastsubtrees"
CONTAINER_NAME = "fastsubtreesC"

cleanup:
	docker container rm -f ${CONTAINER_NAME} || true
	docker image rm -f ${IMAGE_NAME} || true

image:
	docker build --tag ${IMAGE_NAME} . --build-arg CACHEBUST=$$(date +%s)

container:
	if [ -z "$$(docker ps -a | grep ${CONTAINER_NAME})" ]; then \
		docker run --detach --name ${CONTAINER_NAME} ${IMAGE_NAME}; \
	else \
		docker start ${CONTAINER_NAME}; \
	fi

shell:
	docker exec -it ${CONTAINER_NAME} bash

start_server: container
	docker exec -d ${CONTAINER_NAME} bash
	sleep 5

start_app: container
	docker exec -i ${CONTAINER_NAME} bash \
		-c "cd /fastsubtrees/genomes-attributes-viewer/ && ./start.py"

create_test_db: start_server
	docker exec -it ${CONTAINER_NAME} bash \
		-c "mariadb -u root -prootpass < /fastsubtrees/docker/create_db.sql"

test: create_test_db
	docker exec -it ${CONTAINER_NAME} bash \
		-c "cd /fastsubtrees && make tests"

benchmarks_sql: create_test_db
	docker exec -it ${CONTAINER_NAME} bash \
		-e /fastsubtrees/docker/benchmarks_sql.sh
	docker cp ${CONTAINER_NAME}:/benchmarks_sql.tsv .

benchmarks_fst: container
	docker exec -it ${CONTAINER_NAME} bash \
		-e /fastsubtrees/docker/benchmarks_fst.sh
	docker cp ${CONTAINER_NAME}:/benchmarks_fst.tsv .
