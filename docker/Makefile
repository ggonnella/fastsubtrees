default:
	@echo "make image        build Docker image"
	@echo "make container    create and run Docker container"
	@echo "make shell        interactive shell in Docker container"

.PHONY: image container shell

image:
	docker build --tag fastsubtrees .

container: image
	if [ -z "$$(docker ps -a | grep fastsubtreesC)" ]; then \
		docker run --detach --name fastsubtreesC fastsubtrees; \
	else \
		docker start fastsubtreesC; \
	fi

shell: container
	docker exec -it fastsubtreesC bash

test: container
	docker exec -it fastsubtreesC bash -c "cd /fastsubtrees && make tests"
