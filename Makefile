all: dep-logplex dep-docopt
self:
	rm -fr lp.zip
	curl -O https://github.com/kennethreitz/logplex-instrument/archive/lp.zip
dep-logplex:
	rm -fr logplex
	git clone git@github.com:kennethreitz/python-logplex.git --depth 1
	rm -fr python-logplex/.git
	mv python-logplex/logplex .
	rm -fr python-logplex
dep-docopt:
	curl -O https://raw.github.com/docopt/docopt/master/docopt.py
