simulate:
	rm tifa.yaml
	rm -rf test
	@python -m tifa init --name sample
	@python -m tifa gen
