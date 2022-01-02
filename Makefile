build:
	docker-compose -f docker-compose.local.yml build

up:
	docker-compose -f docker-compose.local.yml up --remove-orphans --quiet-pull

down:
	docker-compose -f docker-compose.local.yml down --remove-orphans

run-tests:
	docker-compose -f docker-compose.local.yml run --rm django pytest

check:
	pre-commit run --all-files
