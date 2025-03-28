.PHONY: docs tests

TESTS_PATH?=tests

docs:
	rm -rf docs/_build && $(MAKE) -C docs html

tests:
	PYTHONPATH=. pytest -s -vvvv -x $(TESTS_PATH)

