default:
	@echo "make image        build Docker image"
	@echo "make container    create and run Docker container"
	@echo "make shell        interactive shell in Docker container"

.PHONY: image container shell start_server create_test_db test

image:
	docker image rm -f fastsubtrees || true
	docker build --tag fastsubtrees .

container: image
	if [ -z "$$(docker ps -a | grep fastsubtreesC)" ]; then \
		docker run --detach --name fastsubtreesC fastsubtrees; \
	else \
		docker start fastsubtreesC; \
	fi

shell: #container
	docker exec -it fastsubtreesC bash

start_server: container
	docker exec -d fastsubtreesC bash
	sleep 5

create_test_db: start_server
	docker exec -it fastsubtreesC bash \
		-c "mariadb -u root -prootpass < /fastsubtrees/docker/create_db.sql"

test: create_test_db
	docker exec -it fastsubtreesC bash -c "cd /fastsubtrees && make tests"

benchmarks_sql: create_test_db
	docker exec -it fastsubtreesC bash -e /fastsubtrees/docker/benchmarks_sql.sh
	docker cp fastsubtreesC:/benchmarks_sql.tsv .

benchmarks_fst:
	docker exec -it fastsubtreesC bash -e /fastsubtrees/docker/benchmarks_fst.sh
	docker cp fastsubtreesC:/benchmarks_fst.tsv .
