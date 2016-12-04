PYTHON := python3
VERSION ?= $(shell $(PYTHON) setup.py --version)
SDIST := dist/teamplayer-rotation-$(VERSION).tar.gz
WHEEL := dist/teamplayer_rotation-$(VERSION)-py3-none-any.whl
SRC := setup.py $(shell find src/teamplayer_rotation -type f -print)

all: $(SDIST) $(WHEEL)

clean:
	$(RM) -rf build dist library_index
	find . -name '*.py[co]' -delete

test:
	$(PYTHON) ./runtests.py --failfast

$(SDIST): $(SRC)
	$(PYTHON) setup.py sdist

$(WHEEL): $(SRC)
	$(PYTHON) setup.py bdist_wheel


.PHONY: all clean test
