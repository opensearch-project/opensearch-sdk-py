class Version:
    MASK = 0x08000000
    CURRENT = 3000099
    CURRENT_ID = CURRENT ^ MASK

    def __init__(self, id: int=0):
        # OpenSearch flips 25th bit to sort higher than legacy versions
        self.id = id ^ Version.MASK
        self.__build_string()

    def from_bytes(self, data: bytes):
        # If we have data bytes use directly for id without bit-flip
        self.id = int.from_bytes(data, "big")             
        self.__build_string()

    def __build_string(self):
        # String parsing strips 25th bit
        id = self.id & 0xF7FFFFFF
        self.major = int((id / 1000000) % 100)
        self.minor = int((id / 10000) % 100)
        self.revision = int((id / 100) % 100)
        self.build = int(id % 100)

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.revision}.{self.build}"
            
    def __bytes__(self):
        return self.id.to_bytes(4, byteorder='big')
