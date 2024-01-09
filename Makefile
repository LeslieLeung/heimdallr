pre-commit:
	poetry run pre-commit run

run:
	python -m uvicorn main:app --host 0.0.0.0 --port 9000 --reload