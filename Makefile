SHELL := /bin/bash

REQUIREMENTS_CACHE := .requirements_cache
REQUIREMENTS_HASH := $(shell cat requirements* | md5sum | cut -f1 -d " ")
REQUIREMENTS_CACHE_HASH := $(shell cat ${REQUIREMENTS_CACHE} 2> /dev/null)
PACKAGE := we
TEST_PACKAGE := tests
PYTHON_PATH := $(shell pwd)/${PACKAGE}
PYTEST := @env PYTHONPATH=$(PYTHONPATH) PYTEST=1 py.test
PYLINT := @env PYTHONPATH=$(PYTHONPATH) pylint --disable=I0011 --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}"
PEP8 := @env PYTHONPATH=$(PYTHONPATH) pycodestyle --repeat --ignore=E202,E501,E402

default:
	@echo "Known make targets:"
	@echo "  clean        		-  delete .pyc files"
	@echo "  configure    		-  install requirements"
	@echo "  test        	 	-  run all tests"
	@echo "  draw         		-  do the draw"

# have all shell commands executed in a single shell
.ONESHELL:

default: test

clean:
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} \;

configure: clean
	@if [ "${REQUIREMENTS_HASH}" != "${REQUIREMENTS_CACHE_HASH}" ]; then \
		echo "🏗  Installing requirements"; \
		pip install --upgrade pip; \
		pip install -r requirements.txt; \
		echo ${REQUIREMENTS_HASH} > ${REQUIREMENTS_CACHE}; \
	fi

check-coding-style: configure
	$(PEP8) $(PACKAGE)
	$(PYLINT) -E $(PACKAGE)

test: check-coding-style
	@echo "💫 Running unit tests..."
	$(PYTEST)

.PHONY: clean configure check-coding-style test
