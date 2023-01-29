import struct

CIS_HEADER = b"MSTARSEMIUSFDCIS"
# 16 bytes of header
# 1 + 15 bytes of id len + id
CIS_FORMAT_ID = "B15s"
CIS_FORMAT_SPARE = "H"
CIS_FORMAT_PAGE_BYTES = "H"
CIS_FORMAT_BLOCK_PAGES = "H"
CIS_FORMAT_BLOCKS = "H"
CIS_FORMAT_SECTOR_BYTES = "H"
CIS_FORMAT_PLANE_COUNT = "B"
CIS_FORMAT_WRAP_CONFIG = "B"
CIS_FORMAT_RIUREAD = "B"
# not sure about this but there is an extra zero in the binaries
CIS_FORMAT_TERMINATOR = "B"
CIS_FORMAT = "<16s" + \
             CIS_FORMAT_ID + \
             CIS_FORMAT_SPARE + \
             CIS_FORMAT_PAGE_BYTES + \
             CIS_FORMAT_BLOCK_PAGES + \
             CIS_FORMAT_BLOCKS + \
             CIS_FORMAT_SECTOR_BYTES + \
             CIS_FORMAT_PLANE_COUNT + \
             CIS_FORMAT_WRAP_CONFIG + \
             CIS_FORMAT_RIUREAD + \
             "BBBB" + \
             "3s" + \
             "3s" + \
             "B" + \
             "B" + \
             CIS_FORMAT_TERMINATOR
CIS_SIZE = struct.calcsize(CIS_FORMAT)


class CIS:
    __slots__ = ["header", "id_byte_count", "id", "spare_byte_count",
                 "page_byte_count", "block_page_count", "block_count",
                 "sector_byte_count", "plane_count", "wrap_config",
                 "riu_read", "clock_config", "uboot_pba", "bl0_pba",
                 "bl1_pba", "hash_pba0", "hash_pba1", "read_mode", "write_mode", "terminator"]

    DEFAULT_SPARE_SIZE = 64
    DEFAULT_PAGE_SIZE = 2048
    DEFAULT_BLOCK_PAGES = 64
    DEFAULT_SECTOR_SIZE = 512
    DEFAULT_BLOCKS = 1024
    DEFAULT_CLOCK_CONFIG = 0x36

    def __init__(self):
        self.header = CIS_HEADER
        self.id_byte_count = 5
        self.id = b"\xee\xee\x01\x00\x06"
        self.spare_byte_count = CIS.DEFAULT_SPARE_SIZE
        self.page_byte_count = CIS.DEFAULT_PAGE_SIZE
        self.block_page_count = CIS.DEFAULT_BLOCK_PAGES
        self.block_count = CIS.DEFAULT_BLOCKS
        self.sector_byte_count = CIS.DEFAULT_SECTOR_SIZE
        self.plane_count = 0
        self.wrap_config = 0
        self.riu_read = 0
        self.clock_config = CIS.DEFAULT_CLOCK_CONFIG
        self.uboot_pba = 0
        self.bl0_pba = 0
        self.bl1_pba = 0
        self.hash_pba0 = b"\x00"
        self.hash_pba1 = b"\x00"
        self.read_mode = 0
        self.write_mode = 0
        self.terminator = 0

    def set_id(self, manuf, part):
        self.id = b"\xee\xee\x01\x00\x06"
        self.id_byte_count = len(self.id)

    def dump(self):
        print("Header: %s" % self.header.decode())
        print("ID: %s (%d bytes)" % (self.id[:self.id_byte_count].hex(), self.id_byte_count))
        print("Spare byte count: %d" % self.spare_byte_count)
        print("Page byte count: %d" % self.page_byte_count)
        block_sz = self.page_byte_count * self.block_page_count
        print("Block size: %d bytes (%d pages)" % (block_sz, self.block_page_count))
        device_sz = self.block_count * block_sz
        print("Device capacity: %d bytes (%d blocks)" % (device_sz, self.block_count))
        print("Sector byte count: %d" % self.sector_byte_count)
        print("Plane count: %d" % self.plane_count)

        # Fields I need to work out the meaning of
        print("Wrap config: 0x%x" % self.wrap_config)
        print("RIU read: 0x%x" % self.riu_read)
        print("clock config: 0x%x" % self.clock_config)
        print("uboot pba: 0x%x" % self.uboot_pba)
        print("bl0 pba: 0x%x" % self.bl0_pba)
        print("bl1 pba: 0x%x" % self.bl1_pba)

    def pack(self):
        return struct.pack(CIS_FORMAT,
                           self.header,
                           self.id_byte_count,
                           self.id,
                           self.spare_byte_count,
                           self.page_byte_count,
                           self.block_page_count,
                           self.block_count,
                           self.sector_byte_count,
                           self.plane_count,
                           self.wrap_config,
                           self.riu_read,
                           self.clock_config,
                           self.uboot_pba,
                           self.bl0_pba,
                           self.bl1_pba,
                           self.hash_pba0,
                           self.hash_pba1,
                           self.read_mode,
                           self.write_mode,
                           self.terminator).ljust(self.page_byte_count, b'\xff')


def unpack(data):
    unpacked = struct.unpack(CIS_FORMAT, data[:CIS_SIZE])
    res = CIS()

    for i, val in enumerate(CIS.__slots__):
        res.__setattr__(val, unpacked[i])

    return res
