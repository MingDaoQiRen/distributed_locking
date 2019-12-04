PROJECT_NAME=distributed_locking
PYCMD=python3.7
PIPCMD=pip3
PIP_SOURCE=-i https://pypi.tuna.tsinghua.edu.cn/simple
ENV_PATH=venv
PIP_INSTALL=$(PIPCMD) install $(PIP_SOURCE)
ROOT_PACKAGE=doc-processing

.PHONY: help env deps prod_deps lint lint_fix

help: Makefile
	@echo
	@echo " Choose a command to run in "$(PROJECT_NAME)":"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'

## env: Create a virtualenv
env:
	virtualenv -p $(PYCMD) $(ENV_PATH)

## deps: Install all the dependencies
deps:
	@cp .hooks/* .git/hooks/
	@if [ -z $(VIRTUAL_ENV) ]; then \
		echo 'You should source your virtualenv first by "source $(ENV_PATH)/bin/activate"'; \
	else \
		$(PIP_INSTALL) -r requirements.txt; \
	fi

prod_deps:
	$(PIP_INSTALL) -r requirements.txt

## dev: run the package
dev:
	@$(PYCMD) -m $(ROOT_PACKAGE)

## lint: Run pylint on all project files
lint:
	@find . -name "*.py" -not -path "./$(ENV_PATH)/*" -not -path "./tests/*" | xargs flake8

## lint_fix: Fix the basic linting problems
lint_fix:
	find . -name "*.py" -not -path "./$(ENV_PATH)/*" -not -path "./tests/*" | xargs autopep8 --in-place