PKG=binpacking

default:
	pip install -e ../${PKG} --no-binary :all:

install:
	pip install ../${PKG}

pypi:
	rm dist/*
	python setup.py sdist
	twine upload dist/*

readme:
	pandoc --from markdown_github --to rst README.md > _README.rst
	sed -e "s/^\:\:/\.\. code\:\: bash/g" _README.rst > README.rst
	rm _README.rst
