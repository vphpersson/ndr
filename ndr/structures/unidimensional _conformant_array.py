from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, Tuple, Union
from struct import unpack as struct_unpack, pack as struct_pack, error as struct_error, \
    unpack_from as struct_unpack_from

from ndr.structures import NDRType


@dataclass
class UnidimensionalConformantArray(NDRType):
    STRUCTURE_SIZE: ClassVar[int] = 4
    representation: Tuple[Union[NDRType, bytes], ...]

    @classmethod
    def from_bytes(cls, data: bytes, size_per_element: int = 1) -> UnidimensionalConformantArray:
        try:
            maximum_count: int = struct_unpack('<I', data[:4])[0]
            return cls(
                representation=tuple(
                    bytes(struct_unpack_from(size_per_element * 'B', buffer=data[4:], offset=i*size_per_element))
                    for i in range(maximum_count)
                )
            )
        except struct_error as e:
            raise ValueError from e

    def __bytes__(self) -> bytes:
        return b''.join([
            struct_pack('<I', len(self.representation)),
            b''.join(bytes(element) for element in self.representation)
        ])

    def __len__(self) -> int:
        return len(self.__bytes__())