from __future__ import annotations
from typing import ByteString, Final, Optional
from struct import Struct

from ndr.structures import NDRType


class UnidimensionalConformantVaryingArray(NDRType):

    _MAXIMUM_COUNT_STRUCT: Final[Struct] = Struct('<I')
    _DATA_OFFSET_STRUCT: Final[Struct] = Struct('<I')
    _ACTUAL_COUNT_STRUCT: Final[Struct] = Struct('<I')

    def __init__(self, representation: bytes = b'', offset: int = 0, maximum_count: Optional[int] = None):
        self.representation: bytes = representation
        self.offset: int = offset
        self._maximum_count: Optional[int] = maximum_count

    @property
    def actual_count(self) -> int:
        return len(self.representation)

    @property
    def maximum_count(self) -> int:
        return self._maximum_count if self._maximum_count is not None else self.actual_count

    @maximum_count.setter
    def maximum_count(self, value: int):
        self._maximum_count = value

    @classmethod
    def from_bytes(cls, data: ByteString, base_offset: int = 0) -> UnidimensionalConformantVaryingArray:
        data = memoryview(data)[base_offset:]
        offset = 0

        maximum_count: int = cls._MAXIMUM_COUNT_STRUCT.unpack_from(buffer=data, offset=offset)[0]
        offset += cls._MAXIMUM_COUNT_STRUCT.size

        data_offset: int = cls._DATA_OFFSET_STRUCT.unpack_from(buffer=data, offset=offset)[0]
        offset += cls._DATA_OFFSET_STRUCT.size

        actual_count: int = cls._ACTUAL_COUNT_STRUCT.unpack_from(buffer=data, offset=offset)[0]
        offset += cls._ACTUAL_COUNT_STRUCT.size

        representation = bytes(data[offset:offset+actual_count])

        return cls(maximum_count=maximum_count, offset=data_offset, representation=representation)

    def __bytes__(self) -> bytes:
        return b''.join([
            self._MAXIMUM_COUNT_STRUCT.pack(self.maximum_count),
            self._DATA_OFFSET_STRUCT.pack(self.offset),
            self._ACTUAL_COUNT_STRUCT.pack(self.actual_count),
            self.representation
        ])

    def __len__(self) -> int:
        return sum([
            self._MAXIMUM_COUNT_STRUCT.size,
            self._DATA_OFFSET_STRUCT.size,
            self._ACTUAL_COUNT_STRUCT.size,
            len(self.representation)
        ])
