help:  
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

mypy: ## type check
	mypy --check-untyped-defs src

test-pca-postgres-up: ## run test postgres
	docker run \
	--name test-pca-postgres \
	-e POSTGRES_USER=pca \
	-e POSTGRES_PASSWORD=pca \
	-e POSTGRES_DB=pca \
	-p 5432:5432 \
	-d postgres:12.5-alpine

test-pca-postgres-cli:
	docker exec -it test-pca-postgres psql -U pca -d pca