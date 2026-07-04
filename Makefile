PYTHON ?= python3
VENV := .venv
BIN := $(VENV)/bin

.PHONY: install lint test format clean

install:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -e cli/repo_health[dev]

lint:
	$(BIN)/ruff check .
	$(BIN)/ruff format --check .
	find . -type f -name '*.sh' -not -path './$(VENV)/*' -not -path './.git/*' -print0 | xargs -0 -r $(BIN)/shellcheck

test:
	$(BIN)/pytest cli/

format:
	$(BIN)/ruff format .
	$(BIN)/ruff check --fix .

clean:
	rm -rf $(VENV)
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '*.egg-info' -exec rm -rf {} +
