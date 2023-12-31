# for using local runs you need to export variables in shell
dev-local:
	poetry install
	uvicorn src.main:app --reload

test-local:
	poetry install --with test
	pytest tests/

dev:
	docker-compose -f 'docker-compose.dev.yml' up --build

test:
	docker-compose -f 'docker-compose.test.yml' --env-file /dev/null run --build test
