from __future__ import annotations
from dataclasses import dataclass, field
from typing import Union, ClassVar, ByteString
from struct import unpack_from, pack

from ndr.structures import NDRType


@dataclass
class Pointer(NDRType):
    representation: Union[NDRType, memoryview]
    referent_id: int = field(default_factory=lambda: next(NDRType._referent_id_iterator))
    structure_size: ClassVar[int] = 4

    @classmethod
    def from_bytes(cls, data: ByteString, base_offset: int = 0) -> Pointer:
        data = memoryview(data)[base_offset:]
        offset = 0

        referent_id: int = unpack_from('<I', buffer=data, offset=offset)[0]
        offset += 4
        if referent_id == 0:
            return NullPointer()

        return cls(
            referent_id=referent_id,
            representation=data[offset:]
        )

    def __bytes__(self) -> bytes:
        return pack('<I', self.referent_id) + bytes(self.representation)


# TODO: I want this to be a singleton...
class NullPointer(Pointer):
    def __init__(self):
        self.representation = memoryview(b'')
        self.referent_id = 0
