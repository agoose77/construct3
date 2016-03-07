from construct3.packers import Adapter, noop, Raw, PackerError, _contextify, UnnamedPackerMixin, Sequence
from construct3.lib import this
from construct3.lib.containers import Container
from construct3.lib.config import Config

try:
    from io import BytesIO

except ImportError:
    from cStringIO import StringIO as BytesIO

import six


class ValidationError(PackerError):
    pass


class PaddingError(PackerError):
    pass


class SymmetricAdapter(Adapter):
    __slots__ = ()

    def codec(self, obj, ctx):
        raise NotImplementedError()

    def encode(self, obj, ctx):
        return self.codec(obj, ctx)

    decode = encode


class OneOf(SymmetricAdapter):
    __slots__ = ["values"]

    def __init__(self, pkr, values):
        SymmetricAdapter.__init__(self, pkr)
        self.values = values

    def codec(self, obj, ctx):
        if obj not in self.values:
            raise ValidationError("%r must be in %r" % (obj, self.values))

        return obj


class NoneOf(SymmetricAdapter):
    __slots__ = ["values"]

    def __init__(self, pkr, values):
        SymmetricAdapter.__init__(self, pkr)
        self.values = values

    def codec(self, obj, ctx):
        if obj in self.values:
            raise ValidationError("%r must not be in %r" % (obj, self.values))
        return obj


class Computed(SymmetricAdapter):
    __slots__ = ["expr"]

    def __init__(self, expr):
        SymmetricAdapter.__init__(self, noop)
        self.expr = _contextify(expr)

    def codec(self, obj, ctx):
        return self.expr(ctx)


class Mapping(Adapter):
    __slots__ = ["pkr", "enc_mapping", "enc_default", "dec_mapping", "dec_default"]

    def __init__(self, pkr, dec_mapping, enc_mapping, dec_default = NotImplemented, enc_default = NotImplemented):
        Adapter.__init__(self, pkr)
        self.enc_mapping = enc_mapping
        self.enc_default = enc_default
        self.dec_mapping = dec_mapping
        self.dec_default = dec_default

    def encode(self, obj, ctx):
        if obj in self.enc_mapping:
            return self.enc_mapping[obj]
        if self.enc_default is NotImplemented:
            raise KeyError("%r is unknown and a default value is not given" % (obj,))
        return self.enc_default

    def decode(self, obj, ctx):
        if obj in self.dec_mapping:
            return self.dec_mapping[obj]
        if self.dec_default is NotImplemented:
            raise KeyError("%r is unknown and a default value is not given" % (obj,))
        return self.dec_default

#class Stamp(Adapter):
#    __slots__ = ["value"]
#    def __init__(self, value):
#        Adapter.__init__(self, Raw(len(value)))
#        self.value = contextify(value)
#    def decode(self, obj, ctx):
#        if obj != self.value:
#            raise ValidationError("%r must be %r" % (obj, self.value))
#        return obj
#    def encode(self, obj, ctx):
#        return self.value


class LengthPrefixed(Adapter):
    __slots__ = ()

    def __init__(self, lengthpkr):
        underlying = Sequence(lengthpkr, Raw(this[0]))
        Adapter.__init__(self, underlying)

    def decode(self, obj, ctx):
        return obj[1]

    def encode(self, obj, ctx):
        return [len(obj), obj]


class StringAdapter(Adapter):
    __slots__ = ["encoding"]

    def __init__(self, underlying, encoding):
        Adapter.__init__(self, underlying)
        self.encoding = encoding

    def decode(self, obj, ctx):
        return obj.decode(self.encoding)

    def encode(self, obj, ctx):
        return obj.encode(self.encoding)


class Padding(UnnamedPackerMixin, Adapter):

    def __init__(self, length, padchar = six.b("\x00"), strict = False):
        self.length = _contextify(length)
        self.padchar = padchar
        self.strict = strict
        Adapter.__init__(self, Raw(self.length))

    def __repr__(self):
        return "Padding(%r)" % (self.length)

    def encode(self, obj, ctx):
        return self.padchar * self.length(ctx)

    def decode(self, obj, ctx):
        if self.strict and obj != self.padchar * self.length(ctx):
            raise PaddingError("Wrong padding pattern %r" % (obj,))
        return None


class Flags(Adapter):
    __slots__ = ["flags"]

    def __init__(self, underlying, **flags):
        Adapter.__init__(self, underlying)
        self.flags = flags

    def _encode(self, obj, context):
        num = 0
        for name, value in self.flags.items():
            if obj.get(name, None):
                num |= value
        return num

    def _decode(self, obj, context):
        return Container((name, bool(obj & mask)) for name, mask in self.flags.items())


class Tunnel(Adapter):
    __slots__ = ["top"]

    def __init__(self, bottom, top):
        Adapter.__init__(self, bottom)
        self.top = top

    def _decode(self, obj, context):
        return self.top._unpack(BytesIO(obj), context, Config())

    def _encode(self, obj, context):
        stream2 = BytesIO()
        self.top._pack(obj, stream2, context, Config())
        return stream2.getvalue()










