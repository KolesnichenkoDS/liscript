from .datatypes import *
from .scoping import *

def evaluate(expr, scope):
    if isinstance(expr, Atom):
        return scope[expr.value]
    if isinstance(expr, Property):
        o = scope[expr.value[0]]
        for s in expr.value[1:]:
            o = o[s]
        return o
    if isinstance(expr, List):
        return (evaluate(expr.value[0], scope))([evaluate(e, scope) for e in expr.value[1:]], scope)
    if isinstance(expr, QExpr):
        return QuotedList([evaluate(e, scope) for e in expr.value])
    if isinstance(expr, DictExpr):
        return Dict(dict((key, evaluate(expr.value[key], scope)) for key in expr.value.keys()))
    return expr
