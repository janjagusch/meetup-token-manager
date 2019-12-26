## deleting all Python garbage
clean:
	@echo "Cleaning up ..."
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +

## testing for missing __init__.py
test_missing_init: clean
	@echo "Testing for missing __init__.py ..."
	@poetry run python bin/test_missing_init

## tox testing
test_tox: test_missing_init
	@echo "Tox testing ..."
	@poetry run tox

## black formatting
format_black: test_missing_init
	@echo "Black formatting ..."
	@poetry run black .

## formatting
format: format_black

## black linting
lint_black: test_missing_init
	@echo "Black linting ..."
	@poetry run black --check .

## pylint linting
lint_pylint: test_missing_init
	@echo "Pylint linting ..."
	@poetry run pylint meetup
	@poetry run pylint $$(find tests/ -iname "*.py")

## linting
lint: lint_black lint_pylint

## installing Jupyter kernel
jupyter_install_kernel:
	@echo "Installing Jupyter kernel ..."
	@bin/install_kernel

# uninstalling Jupyter kernel
jupyter_uninstall_kernel:
	@echo "Uninstalling Jupyter kernel ..."
	@bin/uninstall_kernel
