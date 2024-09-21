help:  
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

server-dev: ## run dev server
	fastapi dev src/main.py
ruff: ## ruff check
	ruff check src/ tests/ && ruff format src/ tests/ 

mypy: ## type check
	mypy --check-untyped-defs src/ tests/

postgresql-up: ## run test postgresql
	docker run \
	--name test-pca-postgres \
	-e POSTGRES_USER=pca \
	-e POSTGRES_PASSWORD=pca \
	-e POSTGRES_DB=pca \
	-p 5432:5432 \
	-d postgres:12.5-alpine

postgresql-cli: ## exec test postgresql
	docker exec -it test-pca-postgres psql -U pca -d pca