pull-testgroup:
	git clone https://github.com/Beer-Bears/scaffold-testgroup codebase

test:
	poetry run pytest

up:
	docker-compose up --build

down:
	docker-compose down