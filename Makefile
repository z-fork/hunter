VENV = venv

PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

PIP_MIRROR = http://mirrors.aliyun.com/pypi/simple/

PIP_INSTALL = $(PIP) install

deps:
	@$(PIP_INSTALL) -i $(PIP_MIRROR) --trusted-host mirrors.aliyun.com -r requirements.txt

venv:
	@virtualenv $(VENV) --prompt '<venv:hunter>'
	@$(PIP_INSTALL) -i $(PIP_MIRROR) -U pip setuptools
