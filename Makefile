POETRY=poetry
PIP=$(POETRY) run pip
PYTEST=$(POETRY) run pytest

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  install             -- to install this project with virtualenv and Pip"
	@echo
	@echo "  clean               -- to clean EVERYTHING (Warning)"
	@echo "  clean-install       -- to clean Python side installation"
	@echo "  clean-pycache       -- to remove all __pycache__, this is recursive from current directory"
	@echo
	@echo "  test-reference      -- to launch Reference test suite using Pytest"
	@echo

clean-pycache:
	@echo ""
	@echo "==== Clear Python cache ===="
	@echo ""
	rm -Rf .pytest_cache
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*\.pyc"|xargs rm -f
.PHONY: clean-pycache

clean-install:
	@echo ""
	@echo "==== Clear installation ===="
	@echo ""
	poetry env remove python3.8
.PHONY: clean-install

clean: clean-install clean-pycache
.PHONY: clean

install:
	@echo ""
	@echo "==== Install everything for development ===="
	@echo ""
	$(POETRY) install
	$(POETRY) add --dev pytest
.PHONY: install

test-reference:
	@echo ""
	@echo "==== Running reference tests ===="
	@echo ""
	$(PYTEST) -vv reference_tests/
.PHONY: test
