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

    measure.python.dance.start=2013-07-16T12:14:15.422563+00:00
    measure.python.dance.end=2013-07-16T12:14:20.618738+00:00
    measure.python.dance.duration=5.196175
    measure.python.dance.level=5
    measure.python.dance.build_id=cf66e9b2-95a6-464d-966f-8f99f421d8fd
    measure.python.dance.buildpack_version=v34
    

Configuration
-------------

By default, `bpwatch` stores its data in `bpwatch.json`. This is configurable with the `BPWATCH_STORE_PATH` environment variable.

    $ export BPWATCH_STORE_PATH=/tmp/somefile

By default, `bpwatch` requires that its distro (`bpwatch.zip`) is next to the executable. This is configurable with the `BPWATCH_DISTRO_PATH` environment variable.

    $ export BPWATCH_DISTRO_PATH=/tmp/bpwatch.zip

