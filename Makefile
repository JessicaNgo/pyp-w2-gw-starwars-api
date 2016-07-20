.PHONY: test test-cov

TAG="\n\n\033[0;32m\#\#\# "
END=" \#\#\# \033[0m\n"

test:
	@echo $(TAG)Running tests$(END)
	PYTHONPATH=. py.test -v tests

test-cov:
	@echo $(TAG)Running tests with coverage$(END)
	PYTHONPATH=. py.test --cov=starwars_api tests

coverage:
	@echo $(TAG)Coverage report$(END)
	@PYTHONPATH=. coverage run --source=starwars_api $(shell which py.test) ./tests -q --tb=no >/dev/null; true
	@coverage report
