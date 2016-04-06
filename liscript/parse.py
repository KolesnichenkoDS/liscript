import operator
import pyparsec.combinators as pyparsec

from pyparsec import State, ParseError

from .datatypes import *

parse_atom = pyparsec.regex(r'[a-zA-Z+*-/=!<>%&|#]+').to(Atom)

parse_int = (pyparsec.string('-') | pyparsec.string('')) >> pyparsec.regex(r'[0-9]+').map(operator.add).to(int)

parse_float = (pyparsec.string('-') | pyparsec.string('')) >> pyparsec.regex(r'[0-9]*\.[0-9]+').map(operator.add).to(float)

parse_number = (parse_float | parse_int).to(Number)

parse_string = pyparsec.regex(r'\"(\\.|[^"])*\"').to(eval).to(String)

parse_val = pyparsec.oneof(
    parse_number,
    pyparsec.lazy(lambda: parse_property),
    parse_atom,
    parse_string,
    pyparsec.lazy(lambda: parse_list),
    pyparsec.lazy(lambda: parse_quoted),
    pyparsec.lazy(lambda: parse_lazylist),
    pyparsec.lazy(lambda: parse_dict),
    pyparsec.lazy(lambda: parse_key),
)

spaces0 = pyparsec.regex(r'[\s\n\t]*')
spaces  = pyparsec.regex(r'[\s\n\t]+')

parse_list = pyparsec.seq(
    pyparsec.string('('),
    spaces0,
    parse_val.to(lambda x: [x]),
    pyparsec.repeat(spaces >> parse_val).map(operator.add),
    pyparsec.ignore(pyparsec.string(')'))
).to(List)

parse_quoted = (pyparsec.string('\'') >> parse_list).to(lambda l: QExpr(l.value)) | (pyparsec.string('\'(') >> spaces0 >> pyparsec.string(')')).to(lambda _: QuotedList([]))

parse_lazylist = pyparsec.seq(
    pyparsec.ignore(pyparsec.string('[') >> spaces0),
    parse_val.to(lambda x: [x]),
    pyparsec.repeat(spaces >> parse_val).map(operator.add),
    pyparsec.ignore(pyparsec.string(']'))
).to(LazyList) | (pyparsec.string('[') >> spaces0 >> pyparsec.string(']')).to(lambda _: LazyList([]))

parse_key = (pyparsec.string(':') >> parse_atom).to(lambda a: Getter(a.value))

def check_property_length(p):
    if len(p) < 2:
        raise ValueError
    return p

parse_property = pyparsec.seq(
    parse_atom,
    pyparsec.repeat(
        pyparsec.ignore(pyparsec.string(':')) >> parse_atom
    ).map(lambda x, y: [x] + y)
).to(check_property_length).to(lambda l: Property([i.value for i in l]))

parse_key_value = pyparsec.seq(
    pyparsec.string(':'),
    parse_atom.to(lambda atom: atom.value),
    pyparsec.ignore(spaces),
    parse_val.map(lambda a, b: (a, b))
)

parse_dict = pyparsec.seq(
    pyparsec.string('{'),
    parse_key_value.to(lambda x: [x]),
    pyparsec.repeat(pyparsec.ignore(spaces0) >> parse_key_value).map(operator.add),
    pyparsec.ignore(pyparsec.string('}'))
).to(dict).to(DictExpr)

parse_comment = pyparsec.regex(r';[^\n]*\n?')

def parse(s):
    p = (State([], s) >> pyparsec.repeat(pyparsec.ignore(spaces0) >> (parse_val | pyparsec.ignore(parse_comment)))) >> pyparsec.ignore(spaces0)
    if p.state != '':
        raise ParseError(repr(p.state))
    return p.value
