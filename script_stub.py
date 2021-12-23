from __future__ import annotations
from typing import Iterator, NoReturn, Annotated

class ProcessEntry():
    def __init__(self, name: str, pid: int):
        self.name = name 
        self.pid = pid

    def __str__(self) -> str:
        return "{} - {}".format(self.name, self.pid)

    def getProcessMaps(self) -> ProcessMap:
        pass


class Processes():
    def __init__(self, procList: list[ProcessEntry] = []):
        pass
    
    def add(self, entry: ProcessEntry) -> None:
        pass

    def findByName(self, name: str, offset = 0) -> ProcessEntry or None:
        pass

    def __iter__(self) -> Iterator[ProcessEntry]:
        pass

    def __str__(self) -> str:
        pass

class ProcessMapEntry():
    def __init__(self, pid: int, name: str, start:int, end:int, offset: int, prot: int):
        pass
    def __str__(self) -> str:
        pass


class ProcessMap():
    def __init__(self, maps: list[ProcessMapEntry] = []):
        pass

    def add(self, entry: ProcessMapEntry):
        pass
 
    def find(self, name = '', prot = -1) -> ProcessMapEntry or None:
        pass

    def __iter__(self) -> Iterator[ProcessMapEntry]:
        pass

    def __str__(self) -> str:
        pass



def connect(name = "", host = "", port = 0) -> None:
    pass

def firmware() -> int:
    """
    Returns PS4 firmware as a number. Ex: 505
    """
    pass

def plist() -> Processes:
    """
    Lists current PS4 firmware as a number. Ex: 505
    """
    pass

def pmap(pid: int = -100000) -> ProcessMap or None:
    pass

def pread(readable, offset = 0, length=0) -> bytes:
    return b''

def pwrite(readable, offset = 0, buffer = b'') -> None:
    pass

def quit() -> NoReturn:
    pass

connected: bool = True 
"""
Keeps track of whether you are connected to a server or not
"""