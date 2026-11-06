#	Enviorment variables and paths
MAIN   = a_maze_ing.py
CONFIG = config.txt
VENV   = .venv
UV     = uv run

#	Default rule (make)
.DEFAULT_GOAL := run

#	Subjet rules

install:
	uv sync

run: install
	$(UV) python $(MAIN) $(CONFIG)

debug:
	$(UV) python -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info/

lint:
	$(UV) flake8 --exclude=$(VENV) .
	$(UV) mypy --exclude $(VENV) . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(UV) flake8 --exclude=$(VENV) .
	$(UV) mypy --exclude $(VENV) . --strict

fclean: clean
	rm -rf $(VENV)
	rm -f uv.lock

.PHONY: install run debug clean lint lint-strict fclean test
