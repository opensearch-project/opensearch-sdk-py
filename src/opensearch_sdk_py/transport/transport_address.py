import ipaddress

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput

class TransportAddress(ipaddress.IPv4Address):
    def __init__(self, address: any='0.0.0.0', port:int=0, host_name=None):
        self.address = ipaddress.IPv4Address(address)
        self.host_name = host_name if host_name else str(self.address)
        self.port = port

    def read_from(self, input: StreamInput):
        addr_bytes = input.read_byte()
        if (addr_bytes != 4):
            raise Exception(f"Invalid address byte size")
        self.address = ipaddress.IPv4Address(input.read_int())
        self.host_name = input.read_string()
        self.port = input.read_int()

    def write_to(self, output: StreamOutput):
        output.write_byte(4)
        output.write_int(int(self.address))
        output.write_string(self.host_name)
        output.write_int(self.port)
