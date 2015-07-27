.PHONY: clean-pyc clean-db


all: clean-pyc

clean: clean-pyc clean-db

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-db:
	find . -name '*.db' -exec rm -f {} +
