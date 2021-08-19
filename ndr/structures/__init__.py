from abc import ABC, abstractmethod
from typing import Final, Iterator


class NDRType(ABC):

    _referent_id_iterator: Final[Iterator[int]] = iter(range(1, 2**32 - 1))

    @abstractmethod
    def __bytes__(self) -> bytes:
        raise NotImplementedError

    def __len__(self) -> int:
        return len(self.__bytes__())
