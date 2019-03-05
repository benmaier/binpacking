default:
	pip install -e ../binpacking --no-binary :all:

install:
	pip install ../binpacking

pypi:
	rm dist/*
	python setup.py sdist
	twine upload dist/*
