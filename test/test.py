from Husky import loads, dumps
import types
import snappy as ziplib
import marshal
from hashlib import sha224
from math import sin
from snappy import compress

def foo(x):
    return dumps(x)

bar = lambda x:x

b = dumps(foo)
b = ziplib.compress(b)

print repr(b)
print len(b)

b = ziplib.decompress(b)
l = loads(b)

# l2 = types.FunctionType(l.func_code, loads.func_globals, l.func_closure, l.func_defaults)

# print [x for x in l.func_globals.iterkeys()]
# print [x for x in loads.func_globals.iterkeys()]
print l(b)

# print l.func_globals["tag"].func_globals
# print l2.func_globals["dispatches"]

# print __import__("Husky.iterable", {}, {}, -1)

d = l.func_globals["dumps"]