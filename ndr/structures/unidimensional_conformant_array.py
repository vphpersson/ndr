from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, Tuple, Union, ByteString
from struct import Struct, unpack_from

from ndr.structures import NDRType


@dataclass
class UnidimensionalConformantArray(NDRType):
    STRUCTURE_SIZE: ClassVar[int] = 4

    _MAXIMUM_COUNT_STRUCT: ClassVar[Struct] = Struct('<I')

    representation: Tuple[Union[NDRType, bytes], ...]

    @classmethod
    def from_bytes(cls, data: ByteString, base_offset: int = 0, size_per_element: int = 1) -> UnidimensionalConformantArray:
        data = memoryview(data)[base_offset:]
        offset = 0

        maximum_count: int = cls._MAXIMUM_COUNT_STRUCT.unpack_from(buffer=data, offset=offset)[0]
        return cls(
            representation=tuple(
                bytes(unpack_from(size_per_element * 'B', buffer=data, offset=offset+i*size_per_element))
                for i in range(maximum_count)
            )
        )

    def __bytes__(self) -> bytes:
        return b''.join([
            self._MAXIMUM_COUNT_STRUCT.pack(len(self.representation)),
            b''.join(
                (bytes([element]) if isinstance(element, int) else bytes(element))
                for element in self.representation
            )
        ])

    def __len__(self) -> int:
        return len(self.__bytes__())
