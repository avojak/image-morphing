python=python3

VERSION_FILE=VERSION
VERSION=`cat $(VERSION_FILE)`

.PHONY: lib web image

all: lib web image

lib:
	echo $(VERSION) > lib/VERSION
	cd lib/ && $(python) setup.py sdist

web:
	echo $(VERSION) > web/VERSION
	cd web/ && $(python) setup.py sdist

image:
	docker build . --tag avojak/image-morphing:$(VERSION)

clean:
	# Cleanup lib
	$(python) lib/setup.py clean
	rm -rf lib/build/ \
		lib/dist/ \
	  	lib/.eggs/ \
	  	lib/libmorphing.egg-info \
	  	lib/.pytest_cache/ \
	  	lib/tests/outputs/
	# Cleanup web
	$(python) web/setup.py clean
	rm -rf web/build/ \
		web/dist/ \
	  	web/.eggs/ \
	  	web/webmorphing.egg-info \
	  	web/.pytest_cache/
	# Other cleanup
	rm -rf .eggs/