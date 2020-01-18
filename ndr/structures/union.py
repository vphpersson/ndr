from __future__ import annotations
from dataclasses import dataclass
from typing import Union
from struct import unpack as struct_unpack, pack as struct_pack

from ndr.structures import NDRType


@dataclass
class NDRUnion(NDRType):
    tag: int
    representation: Union[NDRType, bytes]

    @classmethod
    def from_bytes(cls, data: bytes) -> NDRUnion:
        return cls(tag=struct_unpack('<I', data[:4])[0], representation=data[4:])

    def __bytes__(self) -> bytes:
        return struct_pack('<I', self.tag) + bytes(self.representation)
