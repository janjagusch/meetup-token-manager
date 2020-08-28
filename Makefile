clean:
	@echo "Cleaning up ..."
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +

test_missing_init:
	@echo "Testing for missing __init__.py ..."
	@poetry run python bin/test_missing_init

test_tox: test_missing_init
	@echo "Tox testing ..."
	@poetry run tox

test: test_tox clean

VOLUME ?= "meetup-token-cache-test"
NAME ?= "meetup-token-cache-test-redis"
test_redis:
	@echo "Testing with redis Docker container ..."
	@make docker_redis
	@make test; EXIT_CODE=$$(echo $$?)
	@docker container stop $(NAME)
	@docker container rm $(NAME)
	@exit $(EXIT_CODE)

format_black: test_missing_init
	@echo "Black formatting ..."
	@poetry run black .

format: format_black clean

lint_black: test_missing_init
	@echo "Black linting ..."
	@poetry run black --check .

lint_pylint: test_missing_init
	@echo "Pylint linting ..."
	@poetry run pylint meetup

lint: lint_black lint_pylint clean

docker_redis_volume:
	@bin/docker_redis_volume $(VOLUME)

docker_redis: docker_redis_volume
	@docker run -d -p 6379:6379 -v $(VOLUME):/data --name=$(NAME) redis

jupyter_install_kernel:
	@bin/jupyter_install_kernel

jupyter_uninstall_kernel:
	@bin/jupyter_uninstall_kernel
