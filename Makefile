default: install

.PHONY: install sdist wheel cleanup tests upload

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
cleanup:
	rm -rf dist/ build/ gfapy.egg-info/

tests:
	pytest

upload: tests cleanup sdist wheel
	cd dist; \
  for file in *; do \
    twine check $$file && \
    twine upload $$file; \
  done

