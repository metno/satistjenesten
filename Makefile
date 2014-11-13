unittest:
	nosetests

behave:
	behave

cover:
	nosetests --with-coverage --cover-package=satistjenesten --cover-html

test: unittest behave

clean:
	rm -rf cover
	rm -rf docs/_build
