.PHONY: clean venv test package

clean:
	rm -rf build

install:
	( \
			export PATH="${HOME}/.poetry/bin:${PATH}" && \
			poetry install \
	)

run:
	AWS_PROFILE=accounts-janitor poetry run python3 inspector/main.py

test: install
	( \
			export AWS_ACCESS_KEY_ID='testing' && \
			export AWS_SECRET_ACCESS_KEY='testing' && \
			export AWS_SESSION_TOKEN='testing' && \
			export AWS_SECURITY_TOKEN='testing' && \
			export PATH="${HOME}/.poetry/bin:${PATH}" && \
			poetry run pylint inspector \
	)

package: clean install test
	sh package.sh
