from struct import pack as struct_pack

UF2_MAGIC_START0 = 0x0A324655
UF2_MAGIC_START1 = 0x9E5D5157
UF2_MAGIC_END = 0x0AB16F30

familyid = 0xe48bff56
appstartaddr = 0x10000000

def convert_to_uf2(file_content):
    global familyid
    datapadding = b""
    while len(datapadding) < 512 - 256 - 32 - 4:
        datapadding += b"\x00\x00\x00\x00"
    n_blocks = (len(file_content) - 256) // 512
    outp = []

    for block_n in range(n_blocks):
        ptr = 256 * block_n
        chunk = file_content[ptr:ptr + 256]
        flags = 0x0
        if familyid: flags |= 0x2000
        hd = struct_pack(b"<IIIIIIII",
            UF2_MAGIC_START0, UF2_MAGIC_START1,
            flags, ptr + appstartaddr, 256, block_n, n_blocks, familyid)
        while len(chunk) < 256:
            chunk += b"\x00"
        block = hd + chunk + datapadding + struct_pack(b"<I", UF2_MAGIC_END)
        assert len(block) == 512
        outp.append(block)
    return b"".join(outp)        