IMAGE_NAME="fastsubtrees"
CONTAINER_NAME="fastsubtreesC"
DOCKERHUB_USER=ggonnella
VERSION=$(shell grep -P -o "(?<=__version__=\")[^\"]*" fastsubtrees/__init__.py)

default:
	@echo "Python package:"
	@echo "  make install         install as user editable package"
	@echo "  make sdist           create source distribution"
	@echo "  make wheel           create wheel distribution"
	@echo "  make clean           remove build artifacts"
	@echo "  make upload          create distribution and upload to PyPI"
	@echo ""
	@echo "Test suite:"
	@echo "  make tests           run tests using pytest, locally"
	@echo "  make testcov         pytest-cov coverage report"
	@echo ""
	@echo "Create Docker image/container:"
	@echo "  make image           build Docker image from the Dockerfile"
	@echo "  make image-no-cache  build Docker image, disabling the cache"
	@echo "  make download-image  download Docker image from the Dockerhub"
	@echo "  make container       create and run Docker container from the image"
	@echo "  make docker-push     push Docker image to the Dockerhub"
	@echo ""
	@echo "Use Docker container:"
	@echo "  make docker-clean    remove Docker image and container"
	@echo "  make docker-shell    interactive shell in Docker container"
	@echo "  make docker-benchmarks"
	@echo "                       run benchmarks except very slow ones, in Docker"
	@echo "  make docker-benchmarks-all"
	@echo "                       run all benchmarks (in Docker container)"
	@echo "  make docker-start-example-app"
	@echo "                       start example app web server, in Docker"
	@echo "  make docker-tests    run the test suite in the Docker container"

.PHONY: install sdist wheel clean upload \
	      image image-no-cache download-image container docker-push \
				docker-clean docker-shell docker-benchmarks docker-benchmarks-all \
				docker-start-example-app tests docker-tests testcov

PYTHON?=python3
PIP?=pip3

# Install using pip
install:
	${PIP} install --upgrade --user --editable .

# Source distribution
sdist:
	${PYTHON} setup.py sdist

# Pure Python Wheel
wheel:
	${PYTHON} setup.py bdist_wheel

# Remove distribution files
clean:
	rm -rf dist/ build/ gfapy.egg-info/

tests:
	pytest

testcov:
	pip install pytest-cov
	pytest --cov=fastsubtrees -v tests/

upload: tests clean sdist wheel
	cd dist; \
  for file in *; do \
    twine check $$file && \
    twine upload $$file; \
  done

docker-clean:
	docker container rm -f ${CONTAINER_NAME} || true
	docker image rm -f ${IMAGE_NAME} || true

image:
	docker build --tag ${IMAGE_NAME} . --build-arg CACHEBUST=$$(date +%s)

image-no-cache:
	docker build --tag ${IMAGE_NAME} . --no-cache

version:
	@echo ${VERSION}

docker-push:
	docker login
	docker tag ${IMAGE_NAME} ${DOCKERHUB_USER}/${IMAGE_NAME}:${VERSION}
	docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${VERSION}

docker-download:
	docker pull ${DOCKERHUB_USER}/${IMAGE_NAME}:${VERSION}
	docker tag ${DOCKERHUB_USER}/${IMAGE_NAME}:${VERSION} ${IMAGE_NAME}

container:
	@if [ -z "$$(docker ps -a | grep ${CONTAINER_NAME})" ]; then \
		docker run -p 8050:8050 --detach --name ${CONTAINER_NAME} ${IMAGE_NAME}; \
	else \
		docker start ${CONTAINER_NAME}; \
	fi || echo "\n\nImage not available\n"  \
	   "use 'make image' to build the image"

docker-shell:
	@docker exec -it ${CONTAINER_NAME} bash || \
		echo "\n\nContainer not running\n"  \
		"use 'make container' to start the container"

docker-start-example-app:
	docker exec -it ${CONTAINER_NAME} start-example-app

docker-tests:
	docker exec -it ${CONTAINER_NAME} tests

docker-benchmarks:
	docker exec -it ${CONTAINER_NAME} benchmarks
	docker cp ${CONTAINER_NAME}:/fastsubtrees/benchmarks_sql.tsv .
	docker cp ${CONTAINER_NAME}:/fastsubtrees/benchmarks_fst.tsv .
	docker cp ${CONTAINER_NAME}:/fastsubtrees/benchmarks_attr.tsv .

docker-benchmarks-all:
	docker exec -it ${CONTAINER_NAME} benchmarks --all
	docker cp ${CONTAINER_NAME}:/fastsubtrees/benchmarks_sql.tsv .
	docker cp ${CONTAINER_NAME}:/fastsubtrees/benchmarks_construct.tsv .
	docker cp ${CONTAINER_NAME}:/fastsubtrees/benchmarks_fst.tsv .
	docker cp ${CONTAINER_NAME}:/fastsubtrees/benchmarks_attr.tsv .
