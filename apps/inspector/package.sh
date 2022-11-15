set -e

export PATH="${HOME}/.poetry/bin:${PATH}"
export VENV_PATH=$(poetry env info -p)

poetry install --no-dev
mkdir build
cp -R ${VENV_PATH}/lib/python3.*/site-packages/* build/
cp -R inspector/ build/
