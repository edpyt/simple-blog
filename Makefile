dev:
	poetry install
	uvicorn src.main:app --reload

test:
	poetry install --with test
	pytest tests/

docker-dev:
	docker-compose -f 'docker-compose.dev.yml' up --build

docker-test:
	docker-compose -f 'docker-compose.test.yml' up --build
