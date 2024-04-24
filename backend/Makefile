# Default Python interpreter - can be changed by user
PYTHON := python3

VENV := .venv/bin/

# Create .venv
venv:
	$(PYTHON) -m venv .venv

# This might not work on Windows
req: venv
	$(VENV)pip install -r requirements/basic.txt

run:
	$(VENV)uvicorn app.main:app --reload

clean:
	rm -rf .venv