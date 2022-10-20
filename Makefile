IMAGE_NAME="fastsubtrees"
CONTAINER_NAME="fastsubtreesC"
DOCKERHUB_USER=ggonnella
VERSION=$(shell grep -P -o "(?<=__version__=\")[^\"]*" fastsubtrees/__init__.py)

default:
	@echo "Python package:"
	@echo "  make install            install as user editable package"
	@echo "  make sdist              create source distribution"
	@echo "  make wheel              create wheel distribution"
	@echo "  make clean              remove build artifacts"
	@echo "  make upload             create distribution and upload to PyPI"
	@echo ""
	@echo "Test suite:"
	@echo "  make tests              run tests using pytest, locally"
	@echo "  make testcov            pytest-cov coverage report"
	@echo "  make testcov-html       pytest-cov coverage HTML report"
	@echo "  make flake              install and run flake8"
	@echo ""
	@echo "Create Docker image/container:"
	@echo "  make docker-image       build Docker image from the Dockerfile"
	@echo "  make docker-image-no-cache         (same, disabling the cache)"
	@echo "  make docker-pull        download Docker image from the Dockerhub"
	@echo "  make docker-push        push Docker image to the Dockerhub"
	@echo "  make docker-container   create and run Docker container from the image"
	@echo ""
	@echo "Use Docker container:"
	@echo "  make docker-clean       remove Docker image and container"
	@echo "  make docker-shell       interactive shell in Docker container"
	@echo "  make docker-benchmarks  run benchmarks in Docker container"
	@echo "  make docker-app         start example app web server in Docker container"
	@echo "  make docker-tests       run the test suite in the Docker container"

.PHONY: install sdist wheel clean upload \
	      docker-image docker-image-no-cache docker-pull docker-container \
				docker-push ensure_container_running \
				docker-clean docker-shell docker-benchmarks docker-benchmarks-all \
				docker-app tests docker-tests testcov

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

testcov-html:
	pip install pytest-cov -qqq
	pytest --cov=fastsubtrees --cov=bin --cov-report html -v tests/

testcov:
	pip install pytest-cov -qqq
	pytest --cov=fastsubtrees --cov=bin -v tests/

upload: tests clean sdist wheel
	cd dist; \
  for file in *; do \
    twine check $$file && \
    twine upload $$file; \
  done

docker-clean:
	docker container rm -f ${CONTAINER_NAME} || true
	docker image rm -f ${IMAGE_NAME} || true

docker-image:
	docker build --tag ${IMAGE_NAME} . --build-arg CACHEBUST=$$(date +%s)

docker-image-no-cache:
	docker build --tag ${IMAGE_NAME} . --no-cache

version:
	@echo ${VERSION}

docker-push:
	docker login
	docker tag ${IMAGE_NAME} ${DOCKERHUB_USER}/${IMAGE_NAME}:${VERSION}
	docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${VERSION}

docker-pull:
	docker pull ${DOCKERHUB_USER}/${IMAGE_NAME}:${VERSION}
	docker tag ${DOCKERHUB_USER}/${IMAGE_NAME}:${VERSION} ${IMAGE_NAME}

ensure_container_running:
	@if [ -z "$$(docker ps -a | grep ${CONTAINER_NAME})" ]; then \
		docker run -p 8050:8050 --detach --name ${CONTAINER_NAME} ${IMAGE_NAME}; \
	else \
		docker start ${CONTAINER_NAME}; \
	fi

docker-container:
	make ensure_container_running || \
		(make docker-image && make ensure_container_running)

docker-shell:
	docker exec -it ${CONTAINER_NAME} true || make docker-container
	docker exec -it ${CONTAINER_NAME} bash

docker-app:
	docker exec -it ${CONTAINER_NAME} true || make docker-container
	docker exec -it ${CONTAINER_NAME} start-example-app

docker-tests:
	docker exec -it ${CONTAINER_NAME} true || make docker-container
	docker exec -it ${CONTAINER_NAME} tests

docker-benchmarks-sql:
	docker exec -it ${CONTAINER_NAME} true || make docker-container
	docker exec -it ${CONTAINER_NAME} benchmarks sql
	docker cp ${CONTAINER_NAME}:/fastsubtrees/benchmarks_sql.tsv .

docker-benchmarks-construct:
	docker exec -it ${CONTAINER_NAME} true || make docker-container
	docker exec -it ${CONTAINER_NAME} benchmarks construct
	docker cp ${CONTAINER_NAME}:/fastsubtrees/benchmarks_construct.tsv .

docker-benchmarks-fst:
	docker exec -it ${CONTAINER_NAME} true || make docker-container
	docker exec -it ${CONTAINER_NAME} benchmarks fst
	docker cp ${CONTAINER_NAME}:/fastsubtrees/benchmarks_fst.tsv .

docker-benchmarks-attr:
	docker exec -it ${CONTAINER_NAME} true || make docker-container
	docker exec -it ${CONTAINER_NAME} benchmarks attr
	docker cp ${CONTAINER_NAME}:/fastsubtrees/benchmarks_attr.tsv .
	docker cp ${CONTAINER_NAME}:/fastsubtrees/benchmarks_attr.out .

tables: benchmarks_sql.tsv benchmarks_construct.tsv benchmarks_fst.tsv \
	      benchmarks_attr.tsv benchmarks_attr.out
	@echo "============================="
	@benchmarks/treesizes_from_output.py benchmarks_attr.out > \
		                                  benchmarks.treesizes.tsv
	@echo ""
	@echo "Table 1:"
	@echo ""
	@benchmarks/make_table1.py benchmarks_sql.tsv benchmarks_fst.tsv \
		                         benchmarks.treesizes.tsv | tee table1.md
	@echo ""
	@echo "Table 2:"
	@echo ""
	@benchmarks/make_table2.py benchmarks_attr.tsv benchmarks.treesizes.tsv \
	 													 genome_size | tee table2.md

docker-benchmarks: docker-benchmarks-sql \
	                 docker-benchmarks-construct \
	                 docker-benchmarks-fst \
									 docker-benchmarks-attr
	make tables

flake:
	@pip install flake8 -qqq
	@flake8
