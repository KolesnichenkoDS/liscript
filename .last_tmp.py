import os

from evaluation import *
from parse import *
from scoping import *
from stdlib import *

gscope = Scope({}, builtins)
gscope['global'] = gscope

os.chdir('/sdcard/com.hipipal.qpyplus/projects3/Xen2/')

while True:
    try:
        exprs = parse(input('> '))
        res = builtins['none']
        for expr in exprs:
            res = evaluate(expr, gscope)
        print('  ->', res)
    except Exception as e:
        print('  ~> {0}: {1}'.format(e.__class__.__name__, e))