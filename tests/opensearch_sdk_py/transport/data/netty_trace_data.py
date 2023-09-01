import re

#
# Read netty-formatted log data.
#
#          +-------------------------------------------------+
#          |  0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f |
# +--------+-------------------------------------------------+----------------+
# |00000000| 45 53 00 00 00 31 00 00 00 00 00 00 00 08 08 08 |ES...1..........|
# |00000010| 20 0b 83 00 00 00 1a 00 00 00 16 69 6e 74 65 72 | ..........inter|
# |00000020| 6e 61 6c 3a 74 63 70 2f 68 61 6e 64 73 68 61 6b |nal:tcp/handshak|
# |00000030| 65 00 04 a3 8e b7 41                            |e.....A         |
# +--------+-------------------------------------------------+----------------+
class NettyTraceData:
    class InvalidTraceDataFormat(Exception):
        pass

    def __init__(self, data = None):
        self.data = data

    def load_from(self, filename: str):
        with open(filename, "r+") as f:
            self.__read_separator(f.readline(), 2)
            self.__read_header(f.readline())
            self.__read_separator(f.readline(), 4)
            line = f.readline()
            self.data = bytearray()
            while line:
                match = self.__read_data_line(line)
                if match:
                    data = match.groupdict()['data']
                    self.data.extend(bytearray.fromhex(data))
                line = f.readline()

    def __read_separator(self, line: str, plus_count = 2):
        pattern = ''.join(['[\+][\-]+' for x in range(plus_count - 1)]) + '[\+]'
        return self.__read_line(line, pattern)
    
    def __read_header(self, line: str):
        pattern = '\|  0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f \|'
        return self.__read_line(line, pattern)
    
    def __read_data_line(self, line: str):
        if line[0] == '|':
            pattern = '\|(?P<offset>.[0-9a-fA-F]+)\| (?P<data>.[0-9a-fA-F\ ]+) \|(?P<text>..+)\|'
            return self.__read_line(line, pattern)
        else:
            self.__read_separator(line, 4)
            return None

    def __read_line(self, line: str, pattern: str):
        line = line.strip()
        match = re.fullmatch(pattern, line)
        if not match:
            raise NettyTraceData.InvalidTraceDataFormat(line)
        return match

    @classmethod
    def load(self, filename: str):
        data = NettyTraceData()
        data.load_from(filename)
        return data

