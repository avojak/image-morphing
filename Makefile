python = python3

pylib:
	$(python) setup.py test sdist

image:
	docker build .

clean:
	$(python) setup.py clean; rm -rf build/ dist/