from construct3 import *#uint8, this, Adapter, Raw, int16, Struct, Enum, Sequence
byte = uint8

# b = BitStruct('a' / uint8, 'b'/uint8,'c'/uint8,'d'/uint8,'e'/uint8,'f'/uint8,'g'/uint8,'h'/uint8)
# print(b)
# r = b.pack(dict(a=True,b=True,c=False,d=True,e=False,f=False,g=True,h=True))
# print(b.unpack(r))


class VariableArrayPacker(Adapter):
    __slots__ = ()

    def __init__(self, lengthpkr, itempkr):
        underlying = Sequence(lengthpkr, Array(this[0], itempkr))
        Adapter.__init__(self, underlying)

    def decode(self, obj, ctx):
        return obj[1]

    def encode(self, obj, ctx):
        return [len(obj), obj]
#
# int_list_packer = VariableArrayPacker(uint8,uint8)
# x = int_list_packer.pack([1,2,3,4])
# print(x)
# print(int_list_packer.unpack(x))
#
#
# print(LengthPrefixed(uint8).pack(b'hello'))


_packers = {}


def registered_packer(opcode, *args):
    packer = Struct(*args)
    _packers[opcode] = packer
    return packer


some_packer = registered_packer(1, "name" / PascalString(uint8), "day_no" / uint8)

from construct3.macros import Switch

ex = dict(op_id=1, body=dict(name="james", day_no=1))

message_packer = Struct("op_id" / uint8, "body" / Switch(this.op_id, _packers))

p = message_packer.pack(ex)
print(message_packer.unpack(p).body.name)


#
# ipaddr = byte[4]
# print(ipaddr.unpack("ABCD".encode()))               # [65, 66, 67, 68]
#
# ipaddr = Adapter(byte[4],
#     decode = lambda arr, _: ".".join(map(str, arr)),
#     encode = lambda ipstr, _: [int(x) for x in ipstr.split(".")]
# )
# print(ipaddr.unpack("ABCD".encode()))              # 65.66.67.68
# print(repr(ipaddr.pack("127.0.0.1")))     # '\x7f\x00\x00\x01'
#
# mac_addr = Adapter(byte[6],
#     decode = lambda arr, _: "-".join(map("%02x".__mod__, arr)),
#     encode = lambda macstr, _: macstr.replace("-", "").decode("hex")
# )
#
# ethernet_header = Struct(
#     "destination" / mac_addr,
#     "source" / mac_addr,
#     "type" / int16
# )
#
# print(ethernet_header.unpack(b"123456ABCDEF\x86\xDD"))
#
# ethernet_header = Struct(
#     "destination" / mac_addr,
#     "source" / mac_addr,
#     "type" / Enum(int16,
#         IPv4 = 0x0800,
#         ARP = 0x0806,
#         RARP = 0x8035,
#         X25 = 0x0805,
#         IPX = 0x8137,
#         IPv6 = 0x86DD,
#     )
# )
#
# print( ethernet_header.unpack("123456ABCDEF\x86\xDD"))
#
# prefixed_string = byte >> Raw(this[0])
# print(prefixed_string.unpack("\x05helloXXX"))
#
#
#
#
#
