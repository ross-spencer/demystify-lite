.DEFAULT_GOAL := help

.PHONY: clean package package-deps package-source package-upload package-wheel tar-source

pre-commit:     											## Run all pre-commit checks
	pre-commit run --all-files

help:                                                       ## Print this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
