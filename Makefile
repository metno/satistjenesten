test:
	nosetests

behave:
	behave

cover:
	nosetests --with-coverage --cover-package=satistjenesten --cover-html
