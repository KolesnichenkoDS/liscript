from functools import reduce
import math
import operator
import sys

from .datatypes import *
from .evaluation import *
from .parse import *
from .scoping import *

def binop(fn):
    return lambda args, scope: reduce(fn, args)

def pure(fn):
    return lambda args, scope: fn(*args) or Atom('none')

true, false = Atom('#t'), Atom('#f')

def let(args, scope):
    names = [i.value for i in args[0].value]
    values = args[1:]
    if len(names) != len(values):
        raise ValueError
    for n, v in zip(names, values):
        scope[n] = v
    return Atom('none')
    
def set_(args, scope):
    this = args[0]
    name = args[1].value[0].value
    value = args[2]
    this[name] = value
    return Atom('none')
    
def modify(args, scope):
    key = args[0].value[0].value
    scope[key] = evaluate(List((args[1] + args[0]).value), scope)
    return Atom('none')

def eval_list(lst, scope):
    return evaluate(List(lst.value), scope)

def replaceargs(d, e):
    if isinstance(e, Atom) and e.value in d.keys():
        return Quoted(d[e.value])
    if isinstance(e, List):
        return List([__replaceargs(d, i) for i in e.value])
    return e

def fn(args, closure):
    argslist, body = args[0], args[1:]
    def inner(innerargs, scope):
        if len(innerargs) != len(argslist.value):
            raise ValueError
        argsdict = {}
        for i in range(len(argslist.value)):
            argsdict[argslist.value[i].value] = innerargs[i]
        res = None
        innerscope = Scope(Scope(argsdict, closure), scope)
        for e in body:
            res = eval_list(e, innerscope)
        return res
    return inner

def def_(args, scope):
    name = args[0].value[0].value
    listargs = List(args[0].value[1:])
    scope[name] = fn([listargs] + args[1:], scope)
    return Atom('none')
    
def class_(args, scope):
    name = args[0].value[0].value
    data = args[1].value
    scope[name] = Class(data)

def do(args, scope):
    res = Atom('none')
    for arg in args:
        res = eval_list(arg, scope)
    return res
    
def chain(args, scope):
    obj = args[0]
    actions = args[1:]
    for action in actions:
        getter = evaluate(action[0], scope)
        args = [evaluate(e, scope) for e in action[1:]]
        obj = getter([obj], scope)([obj] + args, scope)
    return obj
    
def while_(args, scope):
    cond = args[0]
    body = args[1:]
    res = Atom('none')
    while eval_list(cond, scope).value == '#t':
        for expr in body:
            res = eval_list(expr, scope)
    return res
    
def for_(args, scope):
    name = args[0].value[0].value
    saved = None
    if name in scope.keys():
        saved = scope[name]
    lst = args[1].value
    body = args[2]
    res = Atom('none')
    for i in lst:
        scope[name] = i
        res = eval_list(body, scope)
    del scope[name]
    if saved is not None:
        scope[name] = saved
    return res

def filter_(args, scope):
    fn, lst = args[0], args[1]
    return QuotedList([i for i in lst if fn([i], scope).value == '#t'])
    
def require(args, scope):
    name = args[0].value[0].value
    module_scope = Scope({}, builtins)
    with open(name + '.li', 'r') as code:
        exprs = parse(code.read())
        for expr in exprs:
            evaluate(expr, module_scope)
    return module_scope
    
def if_(args, scope):
    if args[0].value == '#t':
        return eval_list(args[1], scope)
    res = Atom('none')
    for arg in args[2:]:
        res = eval_list(arg, scope)
    return res

def case(args, scope):
    for cond, body in zip(args[::2], args[1::2]):
        if eval_list(cond, scope).value == '#t':
            return eval_list(body, scope)
    return Atom('none')

builtins = {
    'id': pure(lambda x: x),
    '->': lambda args, scope: args[0],
    'let': let,
    'set': set_,
    'require': require,
    'class': class_,
    'new': lambda args, scope: args[0].create(args[1:], scope),
    'modify': modify,
    'fn': fn,
    'def': def_,
    
    '#t': Atom('#t'),
    '#f': Atom('#f'),
    'none': Atom('none'),
    'zero': Number(0),
    
    '+': binop(operator.add),
    '-': binop(operator.sub),
    '*': binop(operator.mul),
    '/': binop(operator.truediv),
    
    'sqrt': lambda args, scope: math.sqrt(args[0]),
    
    '>': binop(operator.gt),
    '<': binop(operator.lt),
    '=': binop(operator.eq),
    '!=': binop(operator.ne),
    
    # 'if': lambda args, scope: eval_list(args[1] if args[0].value == '#t' else args[2], scope),
    # 'unless': lambda args, scope: eval_list(args[1] if args[0].value != '#t' else args[2], scope),
    'if': if_,
    'case': case,
    'otherwise': LazyList([Atom('->'), Atom('#t')]),
    
    'and': binop(operator.and_),
    'or': binop(operator.or_),
    'xor': binop(operator.xor),
    
    'list': pure(lambda *args: QuotedList(args)),
    'head': lambda args, scope: args[0][0],
    'tail': pure(lambda lst: QuotedList(lst[1:])),
    'cons': pure(lambda elem, lst: QuotedList([elem]) + lst),
    'push': pure(lambda elem, lst: lst + QuotedList([elem])),
    '!!': lambda args, scope: args[0][args[1].value],
    'slice': pure(lambda lst, start=None, end=None: QuotedList(lst[start:end])),
    'length': lambda args, scope: Number(len(args[0])),
    'filter': filter_,
    
    'partial': lambda args, scope: lambda args2, scope: args[0](args[1:] + args2, scope),
    'compose': pure(lambda f, g: lambda args, scope: f([g(args, scope)], scope)),
    
    'eval': lambda args, scope: evaluate(args[0], scope),
    'eval-list': lambda args, scope: eval_list(args[0], scope),
    'do': do,
    'chain': chain,
    'while': while_,
    'for': for_,
    
    'say': pure(lambda s: print(s.value if isinstance(s, String) else s)),
    'read': lambda *_: String(input()),
    'exit': lambda *_: sys.exit(0)
}
