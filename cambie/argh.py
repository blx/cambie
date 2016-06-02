"""
argh

Provides a CLI argument-parsing and dependency injection layer over Python's
argparse lib.

Sample usage:

    from argh import Command, Argh

    def do_something_fn(db):
        print 'do stuff with the db'

    def _db(env):
        return get_db_handle_maybe_using_env_vars()

    commands = {
        'do_something': Command(do_something_fn,
                                deps = {'db': _db},
                                args = ['positional',
                                        '--optional',
                                        ['positional/optional with argparse opts',
                                         {'metavar': 'whatever'}]]),
        'another_thing': Command(another_thing)
    }

    cli = Argh('program_name_shown_in_help_text', commands)

    # Run the CLI.
    # (env is passed to each dependency function during DI)
    cli(env)
"""

from argparse import ArgumentParser
from collections import namedtuple
from itertools import chain

from .prelude import items, thread, partial as p, merge

__all__ = ('Command', 'Argh')

Command = namedtuple('Command', ['action', 'args', 'deps'])
Command.__new__.__defaults__ =  (              (),     ())

def with_deps(f, deps=None):
    """Returns `f` decorated so as to receive keyword arguments of k=f(env)
    for each (k, f) in deps."""
    # baby ur a **star
    return lambda env, *a, **kw: f(*a,
                                   **merge(not deps or {k: dep(env) for k, dep in items(deps)},
                                           kw))

def with_cmd_args(f, args=None):
    """Returns `f` decorated so as to receive keyword arguments for each CLI arg"""
    return lambda ns, env: f(env=env,
                             **{k: getattr(ns, k)
                                for k in args or ()})

def load_cmds(argparser, cmds):
    _cmds = argparser.add_subparsers()

    for name, cmd in items(cmds):
        cmd_parser = _cmds.add_parser(name)
        for i, a in enumerate(cmd.args):
            if isinstance(a, basestring):
                cmd_parser.add_argument(a)
            else:
                # Allow cmd.args to contain pairs of [arg name, opts]
                cmd_parser.add_argument(a[0], **a[1])
                cmd.args[i] = a[0]

        cmd_parser.set_defaults(func=thread(cmd.action,
                                            p(with_deps,     deps=cmd.deps),
                                            p(with_cmd_args, args=cmd.args)))

def Argh(program_name, commands):
    argparser = ArgumentParser(prog=program_name)
    load_cmds(argparser, commands)

    def _run(env):
        args_ns = argparser.parse_args()
        args_ns.func(args_ns, env=env)

    return _run
