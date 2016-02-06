from .scoping import *


class XenData:
    __slots__ = ('value', )
    
    def __init__(self, value):
        self.value = value
        
    def __eq__(self, other):
        if self.value == other.value:
            return Atom('#t')
        return Atom('#f')
        
    def __lt__(self, other):
        if type(self) == type(other):
            return Atom('#t') if self.value < other.value else Atom('#f')
        raise TypeError
        
    def __gt__(self, other):
        if type(self) == type(other):
            return Atom('#t') if self.value > other.value else Atom('#f')
        raise TypeError
        
    def __index__(self):
        return self.value
        
    def __len__(self):
        return len(self.value)
        
    def __repr__(self):
        return '{0}(value={1})'.format(self.__class__.__name__, repr(self.value))


class Atom(XenData):
    def __str__(self):
        return self.value


class Number(XenData):
    def __add__(self, other):
        return Number(self.value + other.value)
        
    def __mul__(self, other):
        return Number(self.value * other.value)
        
    def __sub__(self, other):
        return Number(self.value - other.value)
       
    def __truediv__(self, other):
        return Number(self.value / other.value)
    
    def __str__(self):
        return str(self.value)
        
        
class String(XenData):
    def __add__(self, other):
        return String(self.value + other.value)
        
    def __str__(self):
        return repr(self.value)


class List(XenData):
    def __add__(self, other):
        return List(self.value + other.value)
        
    def __getitem__(self, i):
        return self.value[i]
        
    def __str__(self):
        return '({})'.format(' '.join(str(i) for i in self.value))


class QExpr(XenData):
    def __str__(self):
        return '\'({})'.format(' '.join(str(i) for i in self.value))


class QuotedList(XenData):
    def __add__(self, other):
        return QuotedList(self.value + other.value)
    
    def __getitem__(self, i):
        return self.value[i]
    
    def __str__(self):
        return '\'({})'.format(' '.join(str(i) for i in self.value))


class LazyList(XenData):
    def __add__(self, other):
        return LazyList(self.value + other.value)
    
    def __getitem__(self, i):
        return self.value[i]
    
    def __str__(self):
        return '[{}]'.format(' '.join(str(i) for i in self.value))


class DictExpr(XenData):
    def __str__(self):
        return '{{{}}}'.format(' '.join(':' + key + ' ' + str(self.value[key]) for key in self.value.keys()))


class Dict(XenData):
    def __getitem__(self, key):
        return self.value[key]
    
    def __setitem__(self, key, value):
        self.value[key] = value
    
    def __str__(self):
        return '{{{}}}'.format(' '.join(':' + key + ' ' + str(self.value[key]) for key in self.value.keys()))


class Class(XenData):
    def create(self, args, scope):
        obj = Object(self)
        self.value['constructor']([obj] + args, scope)
        return obj


class Object(XenData):
    def __init__(self, class_):
        self.value = {}
        self.class_ = class_
    
    def __getitem__(self, key):
        try:
            return self.value[key]
        except:
            return self.class_.value[key]
    
    def __setitem__(self, key, value):
        self.value[key] = value
    
    def __str__(self):
        return '<{}>'.format(' '.join(':' + key + ' ' + str(self.value[key]) for key in self.value.keys()))
