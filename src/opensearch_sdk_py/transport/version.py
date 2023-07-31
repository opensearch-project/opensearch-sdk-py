class Version:
    MASK = 0x08000000

    def __init__(self, id: int):
        self.data = id
        self.id = id ^ Version.MASK
        id &= 0xF7FFFFFF
        self.major = int((id / 1000000) % 100)
        self.minor = int((id / 10000) % 100)
        self.revision = int((id / 100) % 100)
        self.build = int(id % 100)

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.revision}.{self.build}"
            
    def __bytes__(self):
        return self.data.to_bytes(4, byteorder='big')
