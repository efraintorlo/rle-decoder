SHELL := /bin/bash
#---------------------------------------------------------------------
#
#  ____  _     _____               _                    _
# |  _ \| |   | ____|           __| | ___  ___ ___   __| | ___ _ __
# | |_) | |   |  _|    _____   / _` |/ _ \/ __/ _ \ / _` |/ _ \ '__|
# |  _ <| |___| |___  |_____| | (_| |  __/ (_| (_) | (_| |  __/ |
# |_| \_\_____|_____|          \__,_|\___|\___\___/ \__,_|\___|_|
#
#---------------------------------------------------------------------
#    Makefile to install and run the RLE - Decoder
#---------------------------------------------------------------------
#	Author:      Efrain Torres
#	GitHub:      https://github.com/efraintorlo/rle-decoder
#	Description: This Makefile is useful to:
#	              > Install the Virtual Environment
#	              > Test (pytest)
#---------------------------------------------------------------------

#-----------------------------------------------
# SETTINGS
#-----------------------------------------------
PYTHON ?= python3.12
PIP ?= pip3
VENV ?= venv
# ----------------------------------------------
.PHONY: help create-venv install install-dev test uninstall

default: help

# Check if the virtual environment is created
create-venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo -e "$(BOLD)Creating Virtual Environment: $(VENV)$(ENDC)" && \
		$(PYTHON) -m venv $(VENV) && \
		source $(VENV)/bin/activate && \
		$(PYTHON) -m pip install --upgrade pip; \
	elif [ -d "$(VENV)" ]; then \
		echo -e "$(BOLD)Virtual Environment: $(VENV)$(ENDC) $(GREENC)Already Created$(ENDC)"; \
	fi

install: create-venv
	source $(VENV)/bin/activate && \
	$(PYTHON) -m pip install -e .

install-system:
	$(PIP) install -e .

install-dev: create-venv
	source $(VENV)/bin/activate && \
	$(PYTHON) -m pip install -r requirements.txt

example:
	source $(VENV)/bin/activate && \
	rle-decoder metrics -s 600 500 -c '_lm26^b09I4L4M2M3N2O1N2N2O1N101N101O0O100000O1O100N2K6L3M3N2N2O2N1O3L5L3N2M`bb5' -m 'area,perimeter,centroid,bbox,contour'

test:
	source $(VENV)/bin/activate && \
	$(PYTHON) -m pytest -v tests

uninstall:
	rm -rf $(VENV)

# -----------------------------
# Some styles and colors to be
# used in Terminal outputs
# -----------------------------
REDC = \033[31m
BOLD = \033[1m
GREENC = \033[32m
UNDERLINE = \033[4m
ENDC = \033[0m
# -----------------------------

# --------------------------------------------------------------
help:
	@echo "------------------------------------------------------"
	@echo -e "                  $(UNDERLINE)$(REDC)$(BOLD) < RLE - Decoder >$(ENDC)"
	@echo -e "                   $(GREENC) Makefile Menu$(ENDC)"
	@echo "------------------------------------------------------"
	@echo "Please use 'make <target>' where target is one of:"
	@echo
	@echo -e "$(REDC)default$(ENDC)     > Default Action: '$(GREENC)help$(ENDC)'"
	@echo
	@echo -e "$(REDC)install$(ENDC)     > Create Virtual Env and Install Requirements"
	@echo
	@echo -e "$(REDC)test$(ENDC)        > Run the tests"
	@echo
	@echo -e "$(REDC)uninstall$(ENDC)   > Remove the Virtual Environment"
	@echo
	@echo -e "$(REDC)example$(ENDC)     > Run the RLE - Decoder with an example"
	@echo
	@echo "------------------------------------------------------"
# --------------------------------------------------------------
