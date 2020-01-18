from __future__ import annotations
from dataclasses import dataclass, field
from typing import Union, ClassVar
from struct import unpack as struct_unpack, pack as struct_pack

from ndr.structures import NDRType


@dataclass
class Pointer(NDRType):
    representation: Union[NDRType, bytes]
    referent_id: int = field(default_factory=lambda: next(NDRType._referent_id_iterator))
    structure_size: ClassVar[int] = 4

    @classmethod
    def from_bytes(cls, data: bytes) -> Pointer:

        referent_id: int = struct_unpack('<I', data[:4])[0]
        if referent_id == 0:
            return NullPointer()

        return cls(
            referent_id=struct_unpack('<I', data[:4])[0],
            representation=data[4:]
        )

    def __bytes__(self) -> bytes:
        return struct_pack('<I', self.referent_id) + bytes(self.representation)


# TODO: I want this to be a singleton...
class NullPointer(Pointer):
    def __init__(self):
        self.representation = b''
        self.referent_id = 0
