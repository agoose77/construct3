from construct3 import uint8, this, Adapter, Raw, int16, Struct, Enum, Sequence
byte = uint8

ipaddr = Sequence(byte, byte, byte, byte)
print(ipaddr.unpack("ABCD".encode()))               # [65, 66, 67, 68]
print(ipaddr.pack([65, 66, 67, 68]))       # ABCD

ipaddr = byte >> byte >> byte >> byte
print(ipaddr.unpack(b"ABCD"))               # [65, 66, 67, 68]
print(ipaddr)
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
