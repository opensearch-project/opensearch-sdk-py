from stream_input import StreamInput
from stream_output import StreamOutput

class TransportAddress:
    def __init__(self):
        super().__init__(self)

    def read_from(self, input: StreamInput):
        # final int len = in.readByte();
        # final byte[] a = new byte[len]; // 4 bytes (IPv4) or 16 bytes (IPv6)
        # in.readFully(a);
        # String host = in.readString(); // the host string was serialized so we can ignore the passed in version
        # final InetAddress inetAddress = InetAddress.getByAddress(host, a);
        # int port = in.readInt();
        # this.address = new InetSocketAddress(inetAddress, port);
        pass

    def write_to(self, output: StreamOutput):
        # byte[] bytes = address.getAddress().getAddress();  // 4 bytes (IPv4) or 16 bytes (IPv6)
        # out.writeByte((byte) bytes.length); // 1 byte
        # out.write(bytes, 0, bytes.length);
        # out.writeString(address.getHostString());
        # // don't serialize scope ids over the network!!!!
        # // these only make sense with respect to the local machine, and will only formulate
        # // the address incorrectly remotely.
        # out.writeInt(address.getPort());
        pass
