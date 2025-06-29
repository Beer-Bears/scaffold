ifeq ($(shell test -e '.env' && echo -n yes),yes)
	include .env
endif

BLUE := \033[34m
GREEN := \033[32m
YELLOW := \033[33m
RESET := \033[0m

HELP_FUN = \
    %help; \
    printf "\n${BLUE}Usage:${RESET}\n  make ${YELLOW}<target>${RESET}\n\n"; \
    while(<>) { \
        if(/^([a-zA-Z0-9_-]+):.*\#\#(?:@([a-zA-Z0-9_-]+))?\s(.*)$$/) { \
            push(@{$$help{$$2 // 'Other'}}, [$$1, $$3]); \
        } \
    }; \
    printf "${BLUE}Targets:${RESET}\n"; \
    for (sort keys %help) { \
        printf "${GREEN}%s:${RESET}\n", $$_; \
        printf "  %-20s %s\n", $$_->[0], $$_->[1] for @{$$help{$$_}}; \
        print "\n"; \
    }

args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
	MESSAGE = "No such command (or you pass two or many targets to ). List of possible commands: make help"
else
	MESSAGE = "Done"
endif

.PHONY: pull-testgroup
pull-testgroup:
	git clone https://github.com/Beer-Bears/scaffold-testgroup codebase

.PHONY: test
test:
	poetry run pytest

.PHONY: app-up
app-up:
	docker-compose up --build

.PHONY: app-down
app-down: ##@App Down all docker com
	docker-compose down

.PHONY: pre-commit-install
pre-commit-install: ##@Utils Install pre-commit from pre-commit-config.yaml
	poetry install && poetry run pre-commit install

.PHONY: pre-commit-run
pre-commit-run: ##@Utils Run pre-commit on all files
	poetry run pre-commit run --all-files

.PHONY: pre-commit-clean
pre-commit-clean: ##@Utils Clean all installed pre-commit
	poetry run pre-commit clean

help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

%::
	echo $(MESSAGE)