### BEGIN CFG CONSTANTS
PYTHON_VER := "3.9.7"
### END CFG CONSTANTS


ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

IS_PYENV_OK := $(shell pyenv prefix $(PYTHON_VER) > /dev/null 2> /dev/null; echo $$?)
TARGET_PYTHON := $(shell pyenv prefix $(PYTHON_VER) 2> /dev/null)/bin/python

VENV_DIR := $(ROOT_DIR)/venv
VENV_PIP := $(VENV_DIR)/bin/pip
VENV_PYTHON := $(VENV_DIR)/bin/python

CONFIG_FILE := $(ROOT_DIR)/config.py
REQUIREMENTS_FILE := $(ROOT_DIR)/requirements.txt


.PHONY: hooks
hooks: venv
	pre-commit install --install-hooks

.PHONY: venv
venv: $(VENV_DIR)
	$(VENV_PIP) install -r $(REQUIREMENTS_FILE)

.PHONY: install
install: venv
	/bin/bash cp -n public_config.py config.py

.PHONY: migrate
migrate:
	source $(VENV_DIR)/bin/activate; \
	flask db init; \
	flask db migrate; \
	flask db upgrade; \

.PHONY: run
run:
	$(VENV_PYTHON) app.py

$(VENV_DIR):
ifneq ($(IS_PYENV_OK),0)
	@echo "Please, use pyenv with python version $(PYTHON_VER) installed"
	exit 1
else
	$(TARGET_PYTHON) -m venv $(VENV_DIR)
endif
