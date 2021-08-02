from __future__ import annotations
from dataclasses import dataclass, InitVar
from typing import ClassVar, Optional, ByteString
from struct import unpack_from, pack

from ndr.structures import NDRType


# TODO: The string encoding should be whatever the data representation format label says, no?
@dataclass
class ConformantVaryingString(NDRType):
    STRUCTURE_SIZE: ClassVar[int] = 12

    maximum_count: InitVar[int]
    offset: int
    representation: str

    def __post_init__(self, maximum_count: Optional[int]):
        self._maximum_count: Optional[int] = maximum_count

    @property
    def actual_count(self) -> int:
        # Length of string plus a null byte
        return len(self.representation) + 1

    @property
    def maximum_count(self) -> int:
        return self._maximum_count if self._maximum_count is not None else self.actual_count

    @maximum_count.setter
    def maximum_count(self, value: int):
        self._maximum_count = value

    @classmethod
    def from_bytes(cls, data: ByteString, base_offset: int = 0) -> ConformantVaryingString:
        data = memoryview(data)[base_offset:]
        offset = 0

        maximum_count: int = unpack_from('<I', buffer=data, offset=offset)[0]
        offset += 4

        string_offset: int = unpack_from('<I', buffer=data, offset=offset)[0]
        offset += 4

        actual_count: int = unpack_from('<I', buffer=data, offset=offset)[0]
        offset += 4

        # TODO: `str.rstrip` is not right -- only one null character should be removed!
        representation: str = bytes(data[offset:offset+2*actual_count]).decode(encoding='utf-16-le').rstrip('\x00')

        return cls(maximum_count=maximum_count, offset=string_offset, representation=representation)

    def __bytes__(self) -> bytes:
        return b''.join([
            pack('<I', self.maximum_count),
            pack('<I', self.offset),
            pack('<I', self.actual_count),
            self.representation.encode(encoding='utf-16-le') + 2 * b'\x00'
        ])

    def __len__(self) -> int:
        return len(self.__bytes__())
