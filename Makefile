.PHONY: clean test package install_poetry

clean:
	cd apps/inspector && $(MAKE) clean
	cd apps/recorder && $(MAKE) clean
	cd apps/reporter && $(MAKE) clean

test:
	cd apps/inspector && $(MAKE) test
	cd apps/recorder && $(MAKE) test
	cd apps/reporter && $(MAKE) test

package:
	cd apps/inspector && $(MAKE) package
	cd apps/recorder && $(MAKE) package
	cd apps/reporter && $(MAKE) package

install_poetry:
	( \
		echo 'Installing poetry...' && \
		curl -sSL https://install.python-poetry.org | POETRY_HOME=${HOME}/.poetry python3 - \
	)

build: clean install_poetry test package
