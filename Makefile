all:
	@echo
	@echo "Available targets"
	@echo ""
	@echo "build           -- build python package"
	@echo ""
	@echo "pypi            -- upload package to pypi"
	@echo ""
	@echo "test            -- execute test suite"
	@echo ""
	@echo "pylint          -- run pylint tests"
	@echo ""
	@echo "pre-commit      -- run pre-commit tests"
	@echo ""
	@echo "pydocstyle      -- run pydocstyle tests"
	@echo ""
	@echo "tox            -- run tox tests"
	@echo ""
	@echo "coverage        -- create coverage report"
	@echo ""
	@echo "clean           -- cleanup working directory"

test:
	pytest

build:
	@python3 -m build

pypi:
	@rm -f dist/*
	@python setup.py sdist
	@twine upload dist/*

pylint:
	@pylint --jobs=0 pygruenbeck_cloud *.py
	@pylint --jobs=0 --disable=protected-access,abstract-class-instantiated tests/*

pre-commit:
	@pre-commit run --all-files

pydocstyle:
	@pydocstyle pygruenbeck_cloud tests/*.py tests/*.py *.py

tox:
	@tox

coverage:
	pytest --cov-report html --cov pygruenbeck_cloud --verbose

clean:
	-rm -rf build dist pygruenbeck_cloud.egg-info
	-rm -rf .tox
	-rm -rf .coverage htmlcov

.PHONY: test build clean
