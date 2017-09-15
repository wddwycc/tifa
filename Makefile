simulate:
	rm tifa.yaml
	rm -rf sample
	@python -m tifa init --name sample
	@python -m tifa gen -f
