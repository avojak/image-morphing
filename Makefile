python = python3

.PHONY: lib web image

all: lib web image

lib:
	cd lib/ && $(python) setup.py sdist

web:
	cd web/ && $(python) setup.py sdist

image:
	docker build . --tag avojak/image-morphing

clean:
	# Cleanup lib
	$(python) lib/setup.py clean
	rm -rf lib/build/ \
		lib/dist/ \
	  	lib/.eggs/ \
	  	lib/libmorphing.egg-info \
	  	lib/.pytest_cache/
	# Cleanup web
	$(python) web/setup.py clean
	rm -rf web/build/ \
		web/dist/ \
	  	web/.eggs/ \
	  	web/webmorphing.egg-info \
	  	web/.pytest_cache/
	# Other cleanup
	rm -rf .eggs/