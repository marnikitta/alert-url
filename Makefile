host := alerturl
package := alerturl
deploy_files := alerturl poetry.toml README.md poetry.lock pyproject.toml

all: build

build: .venv

lint: .venv
	poetry run mypy --check-untyped-defs --ignore-missing-imports $(package)
	poetry run flake8 --ignore E501,W503,E203,E126 $(package)
	poetry run black --line-length 120 $(package)

.venv: poetry.lock
	poetry install

push: lint
	ssh -T $(host) "mkdir -p ~/alerturl"
	rsync --delete --verbose --archive --compress --rsh=ssh $(deploy_files) $(host):~/alerturl

deploy: push
	ssh -T $(host) "systemctl --user restart alerturl.service"

FORCE:

.PHONY: all build lint push deploy
