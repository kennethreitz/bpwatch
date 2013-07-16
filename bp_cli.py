#!/usr/bin/env python

"""
Logplex instrumentation.

Usage:
  bpwatch init <token>
  bpwatch build <language> <release> <build_id>
  bpwatch start <event>
  bpwatch stop <event>
  bpwatch -h | --help
  bpwatch --debug

Options:
  -h --help     Show this screen.
  --version     Show version.
"""


import os
import json
from datetime import datetime, timedelta

BPWATCH_STORE_PATH = os.environ.get('BPWATCH_STORE_PATH', 'bpwatch.json')

from logplex import Logplex
from docopt import docopt

def dispatch_cli(args):
    if args.get('init'):
        init(args.get('<token>'))

    if args.get('build'):
        build(args.get('<language>'), args.get('<release>'), args.get('<build_id>'))

    if args.get('--debug'):
        print get_state()

    if args.get('start'):
        start(args.get('<event>'))

    if args.get('stop'):
        stop(args.get('<event>'))


def get_state():
    """Returns a dictionary of the environment state, to be used for
    intial configuration and measuring timedeltas out-of-band.
    If the DB hasn't been created, it will be.
    """
    try:
        with open(BPWATCH_STORE_PATH, 'r') as f:
            return json.loads(f.read())
    except IOError:
        with open(BPWATCH_STORE_PATH, 'w') as f:
            f.write(json.dumps(dict()))
        return get_state()

def set_state(state):
    """Writes the given environment state to disk."""
    with open(BPWATCH_STORE_PATH, 'w') as f:
        f.write(json.dumps(state))

def get_logplex(state):
    """Returns a Logplex Client based on the environment."""
    return Logplex(token=state.get('token'))

def to_timestamp(dt=None):
    """Given a datetime object, returns the expected timestamp.
    If none is provided, datetime.utcnow() is used.
    """
    if dt is None:
        dt = datetime.utcnow()
    return '{}+00:00'.format(dt.isoformat())

def from_timestamp(ts):
    """Given a timepstamp string, returns a datetime."""
    ts = ts.split('+', 1)[0]
    dt_s, _, us= ts.partition(".")
    dt= datetime.strptime(dt_s, "%Y-%m-%dT%H:%M:%S")
    us= int(us.rstrip("Z"), 10)
    return dt + timedelta(microseconds=us)


def init(token=None):
    """Intializes the environment and configures logplex."""
    state = get_state()
    state['token'] = token

    set_state(state)

def build(language, release, build_id):
    state = get_state()
    state['language'] = language
    state['release'] = release
    state['build'] = build_id

    set_state(state)

def start(event, logit=False):
    """Starts a new time measurement"""
    state = get_state()
    now = to_timestamp()

    if 'starts' not in state:
        state['starts'] = {}

    state['starts'][event] = now

    set_state(state)

def stop(event):
    """Stop a given time measurement, measures the delta, logs it."""
    state = get_state()

    now = datetime.utcnow()

    then_ts = state['starts'][event]
    then = from_timestamp(then_ts)
    delta = (now - then).total_seconds()

    points = [
        ('start', then_ts),
        ('end', to_timestamp(now)),
        ('duration', delta),
        ('level', 5),
        ('build_id', state['build']),
        ('buildpack_version', state['release']),
    ]

    to_send = []
    for k, v in points:
        to_send.append('measure.{lang}.{event}.{aspect}={value}'.format(
            lang=state['language'],
            event=event,
            aspect=k,
            value=v
        ))

    logplex = get_logplex(state)
    payload = ' '.join(to_send)
    logplex.puts(payload)


def main():
    arguments = docopt(__doc__, version='Logplex')
    try:
        dispatch_cli(arguments)
    except Exception:
        exit()


if __name__ == '__main__':
    main()
