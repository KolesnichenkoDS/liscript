import os
import sys

from .evaluation import *
from .parse import *
from .scoping import *
from .stdlib import *

gscope = Scope({}, builtins)
gscope['global'] = gscope

def repl():
    while True:
        try:
            exprs = parse(input('> '))
            res = builtins['none']
            for expr in exprs:
                res = evaluate(expr, gscope)
            print('  ->', res)
        except Exception as e:
            print('  ~> {0}: {1}'.format(e.__class__.__name__, e))

def compile():
    filename = sys.argv[1]
    with open(filename, 'r') as code:
        exprs = parse(code.read())
        for expr in exprs:
            evaluate(expr, gscope)
