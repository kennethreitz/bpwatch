Logplex-Instrument
==================

This is a simple

You should be able to just stick it in a directory and go:

    $ git clone git@github.com:kennethreitz/logplex-instrument.git
    $ cd logplex-instrument
    $ make
    $ ./lp

You can then move `lp` and `lp.zip` wherever you like (e.g. a buildpack).


Usage
-----

Configure logplex with the disired prefix and token:

    $ lp init python secretlogplextoken

Log something:

    $ lp log life 42

Start a timer:

    $ lp start dance

End a timer:

    $ $ lp stop dance

Logplex output of all above:

    2013-07-16T07:44:15+00:00 app[python-logplex]: measure.python.life=42
    2013-07-16T07:44:21+00:00 app[python-logplex]: measure.python.dance.start=2013-07-16T07:44:21.550399+00:00
    2013-07-16T07:44:24+00:00 app[python-logplex]: measure.python.dance.end=2013-07-16 07:44:24.246280
    2013-07-16T07:44:24+00:00 app[python-logplex]: measure.python.dance.duration=2.695881