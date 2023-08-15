# https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/transport/TcpHeader.java

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.version import Version
from opensearch_sdk_py.transport.transport_status import TransportStatus

class TcpHeader:
    MARKER_BYTES_SIZE = 2
    MESSAGE_LENGTH_SIZE = 4
    REQUEST_ID_SIZE = 8
    STATUS_SIZE = 1
    VERSION_ID_SIZE = 4
    VARIABLE_HEADER_SIZE = 4
    BYTES_REQUIRED_FOR_MESSAGE_SIZE = MARKER_BYTES_SIZE + MESSAGE_LENGTH_SIZE
    VERSION_POSITION = MARKER_BYTES_SIZE + MESSAGE_LENGTH_SIZE + REQUEST_ID_SIZE + STATUS_SIZE
    VARIABLE_HEADER_SIZE_POSITION = VERSION_POSITION + VERSION_ID_SIZE
    PRE_76_HEADER_SIZE = VERSION_POSITION + VERSION_ID_SIZE
    BYTES_REQUIRED_FOR_VERSION = PRE_76_HEADER_SIZE
    HEADER_SIZE = PRE_76_HEADER_SIZE + VARIABLE_HEADER_SIZE


    def __init__(self, data: StreamInput):
        self.raw = data.raw
        self.prefix = data.read_bytes(2)
        self.size = data.read_int()
        self.request_id = data.read_long()
        self.status = data.read_byte()
        self.version = Version(data.read_int())
        self.variable_header_size = data.read_int()
        # print(f"remaining: {data.read_bytes(self.variable_header_size)}")

    def __str__(self):
        return f"{self.prefix}, message={self.size} byte(s), request_id={self.request_id}, status={self.status}, version={self.version}"

    def __bytes__(self):
        return self.raw
        # frame = bytearray()
        # for b in self.prefix:
        #     frame.append(b)
        # size = 20
        # for b in size.to_bytes(4, byteorder='big'):
        #     frame.append(b)
        # for b in self.request_id.to_bytes(8, byteorder='big'):
        #     frame.append(b)
        # frame.append(self.status)
        # for b in bytes(self.version):
        #     frame.append(b)
        # frame.append(0)
        # return bytes(frame)

    def is_request(self) -> bool:
        return (self.status & TransportStatus.STATUS_REQRES) == 0

    def is_error(self) -> bool:
        return (self.status & TransportStatus.STATUS_ERROR) != 0

    def is_compress(self) -> bool:
        return (self.status & TransportStatus.STATUS_COMPRESS) != 0

    def is_handshake(self) -> bool:
        return (self.status & TransportStatus.STATUS_HANDSHAKE) != 0

    # public static void writeHeader(
    #     StreamOutput output,
    #     long requestId,
    #     byte status,
    #     Version version,
    #     int contentSize,
    #     int variableHeaderSize
    # ) throws IOException {
    #     output.writeBytes(PREFIX);
    #     // write the size, the size indicates the remaining message size, not including the size int
    #     output.writeInt(contentSize + REQUEST_ID_SIZE + STATUS_SIZE + VERSION_ID_SIZE + VARIABLE_HEADER_SIZE);
    #     output.writeLong(requestId);
    #     output.writeByte(status);
    #     output.writeInt(version.id);
    #     assert variableHeaderSize != -1 : "Variable header size not set";
    #     output.writeInt(variableHeaderSize);
    # }