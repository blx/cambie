from argparse import ArgumentParser
from collections import namedtuple
from itertools import chain

from .prelude import items, juxt, thread, partial as p

Command = namedtuple('Command', ['action', 'args', 'deps'])
Command.__new__.__defaults__ =  (              (),     ())

def with_deps(f, deps=None):
    """baby ur a **star"""
    return lambda env, *a, **kw: f(*chain(juxt(*deps)(env) if deps else (),
                                          *a),
                                   **kw)

def with_cmd_args(f, args=None):
    return lambda ns, env: f(env=env,
                             **{k: getattr(ns, k)
                                for k in args or ()})

def load_cmds(argparser, cmds):
    _cmds = argparser.add_subparsers()

    for name, cmd in items(cmds):
        cmd_parser = _cmds.add_parser(name)
        for a in cmd.args:
            cmd_parser.add_argument(a)

        cmd_parser.set_defaults(func=thread(cmd.action,
                                            p(with_deps,     deps=cmd.deps),
                                            p(with_cmd_args, args=cmd.args)))

def argh(program_name, commands):
    argparser = ArgumentParser(prog=program_name)
    load_cmds(argparser, commands)

    def _run(env):
        args_ns = argparser.parse_args()
        args_ns.func(args_ns, env=env)

    return _run
