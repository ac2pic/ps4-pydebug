
# Types

class BaseServer():
    def __init__(self):
        self.is_connected = False
        pass

    def connect(self) -> bool:
        raise 'Not Implemented'

    def getFirmware(self):
        raise 'Not Implemented'

    def getProcessMaps(self, pid: int):
        raise 'Not Implemented'
    
    def getProcessList(self):
        raise 'Not Implemented'

    def readMemory(self, readable = None, address = 0, size = 0):
        raise 'Not Implemented'
    
    def writeMemory(self, writable = None, address = 0, buffer = b''):
        raise 'Not Implemented'



class ProcessEntry():
    def __init__(self, name: str, pid: int, server: BaseServer):
        self.name = name 
        self.pid = pid
        self.server = server

    def getProcessMaps(self):
        return self.server.getProcessMaps(self.pid)

    def __str__(self) -> str:
        return "{} - {}".format(self.name, self.pid)


class Processes():
    def __init__(self, procList = []):
        self.procList = procList
    
    def add(self, entry):
        self.procList.append(entry)

    def findByName(self, name, offset = 0) -> ProcessEntry or None:
        encounterTracker = 0
        for process in self:
            if process.name == name:
                if encounterTracker == offset:
                    return process
                else:
                    encounterTracker += 1
        return None

    def __iter__(self):
        return iter(self.procList)

    def __str__(self):
        return '\n'.join([str(entry) for entry in self.procList])

class ProcessMapEntry():
    def __init__(self, pid, name, start, end, offset, prot):
        self.pid = pid
        self.name = name 
        self.start = start
        self.end = end 
        self.offset = offset
        self.prot = prot
    def __str__(self) -> str:
        return "{} - start={} end={} offset={} prot={}".format(self.name, hex(self.start), hex(self.end), hex(self.offset), self.prot)


class ProcessMap():
    def __init__(self, maps = []):
        self.maps = maps

    def add(self, entry):
        self.maps.append(entry)
 
    def find(self, name = '', prot = -1) -> ProcessMapEntry or None:
        foundMaps = []
        foundMap = None
        for procMap in self:
            if procMap.name == name:
                foundMaps.append(procMap)
        if prot > -1:
            for procMap in foundMaps:
                if (procMap.prot & prot) == prot:
                    foundMap = procMap
                    break
        else:
            foundMap = foundMaps[0] 
        return foundMap

    def __iter__(self):
        return iter(self.maps)

    def __str__(self):
        return '\n'.join([str(entry) for entry in self.maps])


# Exceptions

class ServerException(Exception):
    pass

class ExitException(Exception):
    pass