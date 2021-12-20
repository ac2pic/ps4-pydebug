class BaseServer():
    def __init__(self):
        self.is_connected = False
        pass

    def connect(self):
        raise 'Not Implemented'

    def getProcessMaps(self):
        raise 'Not Implemented'
    
    def getProcessList(self):
        raise 'Not Implemented'

    def readBytes(self, address = 0, size = 0):
        raise 'Not Implemented'

# Types

class Processes():
    def __init__(self, procList = []):
        self.procList = procList
    
    def add(self, entry):
        self.procList.append(entry)

    def __str__(self):
        return '\n'.join([str(entry) for entry in self.procList])

class ProcessEntry():
    def __init__(self, name, pid):
        self.name = name 
        self.pid = pid

    def __str__(self) -> str:
        return "{} - {}".format(self.name, self.pid)

class ProcessMap():
    def __init__(self, maps = []):
        self.maps = maps

    def add(self, entry):
        self.maps.append(entry)

    def __str__(self):
        return '\n'.join([str(entry) for entry in self.maps])

class ProcessMapEntry():
    def __init__(self, name, start, end, offset, prot):
        self.name = name 
        self.start = start
        self.end = end 
        self.offset = offset
        self.prot = prot

    def __str__(self) -> str:
        return "{} - start={} end={} offset={} prot={}".format(self.name, hex(self.start), hex(self.end), hex(self.offset), self.prot)

# Exceptions

class ServerException(Exception):
    pass

