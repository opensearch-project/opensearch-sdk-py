#
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#

import io
import struct
from enum import Enum
from typing import Any, Callable, Optional, Union

from opensearch_sdk_py.transport.time_unit import TimeUnit
from opensearch_sdk_py.transport.time_value import TimeValue
from opensearch_sdk_py.transport.version import Version


class StreamInput:
    def __init__(self, input: Union[bytearray, bytes]) -> None:
        self.raw = input
        self.data = io.BytesIO(input)

    def read_byte(self) -> int:
        return int.from_bytes(self.data.read(1), byteorder="big", signed=True)

    def read_bytes(self, len: int) -> bytes:
        return self.data.read(len)

    def read_int(self) -> int:
        return int.from_bytes(self.data.read(4), byteorder="big", signed=True)

    def read_short(self) -> int:
        return int.from_bytes(self.data.read(2), byteorder="big", signed=True)

    def read_float(self) -> float:
        return float(struct.unpack(">f", self.read_bytes(4))[0])

    def read_double(self) -> float:
        return float(struct.unpack(">d", self.read_bytes(8))[0])

    def read_boolean(self) -> bool:
        value = self.read_byte()
        if value == 0:
            return False
        elif value == 1:
            return True
        else:
            raise Exception(f"Invalid boolean ({value})")

    def read_optional_boolean(self) -> Optional[bool]:
        value = self.read_byte()
        if value == 2:
            return None
        elif value == 0:
            return False
        elif value == 1:
            return True
        else:
            raise Exception(f"Invalid boolean ({value})")

    # Reads an int stored in variable-length format.  Reads between one and
    # five bytes. Smaller values take fewer bytes. Negative numbers
    # will always use all 5 bytes and are therefore better serialized
    # using read_int().
    def read_v_int(self) -> int:
        b = self.read_byte()
        i = b & 0x7F
        if (b & 0x80) == 0:
            return i
        b = self.read_byte()
        i |= (b & 0x7F) << 7
        if (b & 0x80) == 0:
            return i
        b = self.read_byte()
        i |= (b & 0x7F) << 14
        if (b & 0x80) == 0:
            return i
        b = self.read_byte()
        i |= (b & 0x7F) << 21
        if (b & 0x80) == 0:
            return i
        b = self.read_byte()
        if (b & 0x80) != 0:
            raise Exception(f"Invalid vInt (({b} & 0x7f) << 28) | {i}")
        return i | ((b & 0x7F) << 28)

    # reads the OpenSearch Version from the input stream
    def read_version(self) -> Version:
        return Version(self.read_v_int() ^ Version.MASK)

    # reads an optional int
    def read_optional_int(self) -> Optional[int]:
        if self.read_boolean():
            return self.read_int()
        else:
            return None

    def read_long(self) -> int:
        return int.from_bytes(self.data.read(8), byteorder="big", signed=True)

    # reads a long stored in variable-length format
    def read_v_long(self) -> int:
        b = self.read_byte()
        i = b & 0x7F
        if (b & 0x80) == 0:
            return i
        b = self.read_byte()
        i |= (b & 0x7F) << 7
        if (b & 0x80) == 0:
            return i
        b = self.read_byte()
        i |= (b & 0x7F) << 14
        if (b & 0x80) == 0:
            return i
        b = self.read_byte()
        i |= (b & 0x7F) << 21
        if (b & 0x80) == 0:
            return i
        b = self.read_byte()
        i |= (b & 0x7F) << 28
        if (b & 0x80) == 0:
            return i
        b = self.read_byte()
        i |= (b & 0x7F) << 35
        if (b & 0x80) == 0:
            return i
        b = self.read_byte()
        i |= (b & 0x7F) << 42
        if (b & 0x80) == 0:
            return i
        b = self.read_byte()
        i |= (b & 0x7F) << 49
        if (b & 0x80) == 0:
            return i
        b = self.read_byte()
        i |= (b & 0x7F) << 56
        if (b & 0x80) == 0:
            return i
        b = self.read_byte()
        if b != 0 and b != 1:
            # raise IOException("Invalid vlong (" + Integer.toHexString(b) + " << 63) | " + Long.toHexString(i))
            raise Exception(f"Invalid vlong ({b} << 63) | {i}")
        i |= ((b)) << 63
        return i

    # zig-zag encoding cf. https://developers.google.com/protocol-buffers/docs/encoding?hl=en
    def read_z_long(self) -> int:
        z = self.read_v_long()
        return (z >> 1) * (-1 if (z & 1) else 1)

    def read_optional_v_long(self) -> Optional[int]:
        return self.read_v_long() if self.read_boolean() else None

    def read_optional_long(self) -> Optional[int]:
        return self.read_long() if self.read_boolean() else None

    def read_optional_string(self) -> Optional[str]:
        return self.read_string() if self.read_boolean() else None

    def read_array_size(self) -> int:
        array_size = self.read_v_int()
        if array_size > 2**31:
            raise Exception(f"array length must be <= to {2**31} but was: {array_size}")
        return array_size

    def read_string(self) -> str:
        return str(self.read_bytes(self.read_array_size()), "utf-8")

    def read_string_array(self) -> list[str]:
        size = self.read_array_size()
        if size == 0:
            return []

        result = []
        for i in range(size):
            result.append(self.read_string())

        return result

    def read_optional_string_array(self) -> Optional[list[str]]:
        if self.read_boolean():
            return self.read_string_array()
        else:
            return None

    def read_string_to_string_dict(self) -> dict[str, str]:
        size = self.read_v_int()
        if size == 0:
            return {}

        result = dict()
        for i in range(size):
            key = self.read_string()
            value = self.read_string()
            result[key] = value

        return result

    def read_string_to_string_array_dict(self) -> dict[str, list[str]]:
        size = self.read_v_int()
        if size == 0:
            return {}

        result = dict()
        for i in range(size):
            key = self.read_string()
            value = self.read_string_array()
            result[key] = value

        return result

    def read_string_to_string_set_dict(self) -> dict[str, set[str]]:
        size = self.read_v_int()
        if size == 0:
            return {}

        result = dict()
        for i in range(size):
            key = self.read_string()
            value = set()
            for v in self.read_string_array():
                value.add(v)
            result[key] = value

        return result

    def read_generic_value(self) -> Any:
        type: int = self.read_byte()
        if type == -1:
            return None
        reader: dict[int, Callable] = {
            0: self.read_string,
            1: self.read_int,
            2: self.read_long,
            # 3: self.read_float,
            # 4: self.read_double,
            5: self.read_boolean,
            6: self.read_byte_array,
            7: self.read_array_list,
            # 8: self.read_array,
            # 9: self.read_linked_hash_map,
            # 10: self.read_hash_map,
            11: self.read_byte,
            # 12: self.read_date,
            # 13: self.read_zoned_date_time,
            # 14: self.read_bytes_reference,
            # 15: self.read_text,
            16: self.read_short,
            # 17: self.read_int_array,
            # 18: self.read_long_array,
            # 19: self.read_float_array,
            # 20: self.read_double_array,
            # 21: self.read_bytes_ref,
            # no 22
            # 23: self.read_zoned_date_time,
            # 24: self.read_collection,
            # 25: self.read_collection,
            # 26: self.read_big_integer,
        }
        try:
            return reader[type]()
        except KeyError:
            raise Exception(f"Type {type} is not implemented")

    def read_array_list(self) -> list[Any]:
        result: list[Any] = list()
        for i in range(self.read_v_int()):
            result.append(self.read_generic_value())
        return result

    def read_byte_array(self) -> bytes:
        size: int = self.read_array_size()
        return self.read_bytes(size) if size > 0 else b""

    def read_enum(self, enum: Enum) -> Any:
        return enum(self.read_v_int())  # type:ignore

    def read_time_value(self) -> TimeValue:
        duration = self.read_z_long()
        unit = self.read_enum(TimeUnit)
        return TimeValue(duration, unit)
