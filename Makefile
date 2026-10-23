.PHONY: install test run trail clean

install:
	python3 -m venv .venv && .venv/bin/pip install -q -e ".[dev]"

test:
	.venv/bin/pytest -q

run:
	.venv/bin/uvicorn links.api:app --reload

trail:
	git log --oneline --graph --decorate --all

clean:
	rm -rf .venv *.db .pytest_cache
