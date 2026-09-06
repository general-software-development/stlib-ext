.PHONY: complexipy help

help:
	$(info Run `make complexipy` for complexipy reports.)
	$(info )
	$(info This requires `uv` installed to work.)
	$(info )
	@:

complexipy:
	uv run complexipy --suggest-refactors
