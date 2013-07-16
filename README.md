BP-Watch
========

This is a simple CLI for instrumenting buildpacks with Logplex.

You should be able to just stick it in a directory and go:

    $ git clone https://github.com/kennethreitz/bpwatch.git && cd bpwatch
    $ make
    $ ./bpwatch

You can then move `bpwatch` and `bpwatch.zip` wherever you like.


Usage
-----

Configure logplex with the disired prefix and token:

    $ bpwatch init secretlogplextoken
    $ bpwatch build python v34 $REQUEST_ID

Start a timer:

    $ bpwatch start dance

End a timer:

    $ bpwatch stop dance

Logplex output of all above:

    2013-07-16T07:44:15+00:00 app[python-logplex]: measure.python.life=42
    2013-07-16T07:44:21+00:00 app[python-logplex]: measure.python.dance.start=2013-07-16T07:44:21.550399+00:00
    2013-07-16T07:44:24+00:00 app[python-logplex]: measure.python.dance.end=2013-07-16 07:44:24.246280
    2013-07-16T07:44:24+00:00 app[python-logplex]: measure.python.dance.duration=2.695881

Configuration
-------------

By default, `bpwatch` stores its data in `bpwatch.json`. This is configurable with the `BPWATCH_STORE_PATH` environment variable.

    $ export BPWATCH_STORE_PATH=/tmp/somefile

By default, `bpwatch` requires that its distro (`bpwatch.zip`) is next to the executable. This is configurable with the `BPWATCH_DISTRO_PATH` environment variable.

    $ export BPWATCH_DISTRO_PATH=/tmp/bpwatch.zip

