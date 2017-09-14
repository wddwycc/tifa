simulate:
	rm tifa.yaml
	rm -rf test
	@python -m tifa init --name test
	@python -m tifa gen
