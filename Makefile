PYTHONPATH=.

unittest:
	nosetests

behave:
	behave

wip:
	behave --tags=wip

cover:
	nosetests --with-coverage --cover-package=satistjenesten --cover-html

test: unittest behave

clean:
	rm -rf cover
	rm -rf docs/_build
