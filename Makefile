VENV = venv

PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

PIP_MIRROR = http://mirrors.aliyun.com/pypi/simple/

PIP_INSTALL = $(PIP) install

deps-after:
	@$(PIP_INSTALL) -i $(PIP_MIRROR) -r requirements-after.txt

deps:
	@$(PIP_INSTALL) -i $(PIP_MIRROR) -r requirements.txt

venv:
	@virtualenv $(VENV) --prompt '<venv:hunter>'
	@$(PIP_INSTALL) -i $(PIP_MIRROR) -U pip setuptools
