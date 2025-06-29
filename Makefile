pull-testgroup:
	git clone https://github.com/Beer-Bears/scaffold-testgroup codebase

test:
	poetry run pytest
