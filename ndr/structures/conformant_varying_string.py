from __future__ import annotations
from typing import Final, Optional
from struct import unpack as struct_unpack, pack as struct_pack

from ndr.structures import NDRType


# TODO: The string encoding should be whatever the data representation format label says, no?
class ConformantVaryingString(NDRType):

    STRUCTURE_SIZE: Final[int] = 12

    def __init__(self, representation: str = '', offset: int = 0, maximum_count: Optional[int] = None):
        self.representation: str = representation
        self.offset: int = offset
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
    def from_bytes(cls, data: bytes) -> ConformantVaryingString:
        actual_count: int = struct_unpack('<I', data[8:12])[0]

        # TODO: I don't know why the elements are of size 2 -- figure out?
        # TODO: `str.rstrip` is not right -- only one null character should be removed!
        return cls(
            representation=data[12:12+2*actual_count].decode(encoding='utf-16-le').rstrip('\x00'),
            offset=struct_unpack('<I', data[4:8])[0],
            maximum_count=struct_unpack('<I', data[:4])[0]
        )

    def __bytes__(self) -> bytes:
        return b''.join([
            struct_pack('<I', self.maximum_count),
            struct_pack('<I', self.offset),
            struct_pack('<I', self.actual_count),
            self.representation.encode(encoding='utf-16-le') + 2 * b'\x00'
        ])

    def __len__(self) -> int:
        return len(self.__bytes__())