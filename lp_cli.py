#!/usr/bin/env python

"""
Logplex instrumentation.

Usage:
  lplex init <language> [<token>]
  lplex start <event>
  lplex stop <event>
  lplex log <event> <value>
  lplex -h | --help
  lplex --debug

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import os
import json
from datetime import datetime, timedelta

LPLEX_STORE_PATH = os.environ.get('LPLEX_STORE_PATH', 'lplex.json')

from logplex import Logplex
from docopt import docopt

def dispatch_cli(args):
    if args.get('init'):
        init(args.get('<language>'), args.get('<token>'))

    if args.get('--debug'):
        print get_state()

    if args.get('log'):
        log(args.get('<event>'), args.get('<value>'))

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
        with open(LPLEX_STORE_PATH, 'r') as f:
            return json.loads(f.read())
    except IOError:
        with open(LPLEX_STORE_PATH, 'w') as f:
            f.write(json.dumps(dict()))
        return get_state()

def set_state(state):
    """Writes the given environment state to disk."""
    with open(LPLEX_STORE_PATH, 'w') as f:
        f.write(json.dumps(state))

def get_logplex(state):
    """Returns a Logplex Client based on the environment."""
    return Logplex(token=state.get('token'))

def format_entry(state, event, value=None):
    """Formats entries based on the environment."""
    lang = state.get('language')
    return 'measure.{lang}.{event}={value}'.format(lang=lang, event=event, value=value)

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


def init(language, token=None):
    """Intializes the environment and configures logplex."""
    state = get_state()
    state['language'] = language
    state['token'] = token

    set_state(state)

def start(event):
    """Starts a new time measurement, logs it."""
    state = get_state()
    now = to_timestamp()

    if 'starts' not in state:
        state['starts'] = {}

    state['starts'][event] = now

    set_state(state)

    log('{}.start'.format(event), now)

def stop(event):
    """Stop a given time measurement, measures the delta, logs it."""
    state = get_state()

    now = datetime.utcnow()
    try:
        then = from_timestamp(state['starts'][event])
        delta = (now - then).total_seconds()
    except KeyError:
        # Stopping an event that never started.
        delta = None

    log('{}.end'.format(event), now)
    if delta:
        log('{}.duration'.format(event), delta)


def log(event, value):
    """Logs a given event and value."""
    state = get_state()
    logplex = get_logplex(state)
    entry = format_entry(state, event, value)
    logplex.puts(entry)

def main():
    arguments = docopt(__doc__, version='Logplex')
    try:
        dispatch_cli(arguments)
    except Exception:
        exit()

if __name__ == '__main__':
    main()
