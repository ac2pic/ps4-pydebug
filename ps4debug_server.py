import socket
import struct
from base_server import BaseServer, ProcessEntry, ProcessMap, ProcessMapEntry, Processes, ServerException
CMD_PACKET_SIZE = 12
CMD_PACKET_MAGIC = 0xFFAABBCC
CMD_STATUS = {
    "SUCCESS": 0x80000000
}
ProcessListEntrySize = 36
ProcessMapEntrySize = 32 + 8 * 3 + 2

CMD = {
    "CMD_PROC_LIST": 0xBDAA0001,
    "CMD_PROC_READ": 0xBDAA0002,
    "CMD_PROC_WRITE": 0xBDAA0003,
    "CMD_PROC_MAPS": 0xBDAA0004,
    # CMD_PROC_INSTALL: 0xBDAA0005,
    # CMD_PROC_CALL: 0xBDAA0006,
    # CMD_PROC_ALLOC: 0xBDAA000B,
    # CMD_PROC_FREE: 0xBDAA000C,
    # // extended
    # CMD_GET_DBG_BASE_VERSION: 0xBD000001,
    # CMD_GET_PS4_FW: 0xBD000500,
    # CMD_GET_DBG_EXT_VERSION: 0xBD000501,
}

def createCmdPacket(cmdNumber, length = 0):
    packet = bytearray(CMD_PACKET_SIZE)
    struct.pack_into("<I", packet, 0, CMD_PACKET_MAGIC)
    struct.pack_into("<I", packet, 4, cmdNumber)
    struct.pack_into("<I", packet, 8, length)
    return packet 


def readCString(buffer, encoding = 'ascii'):
    termIndex = 0
    while termIndex < len(buffer) and buffer[termIndex] != 0:
        termIndex += 1
    return buffer[0:termIndex].decode(encoding)

class PS4DebugServer(BaseServer):
    def __init__(self):
        BaseServer.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pass

    def checkSuccess(self):
        status = int.from_bytes(self.socket.recv(4, socket.MSG_WAITALL), "little")
        if status != CMD_STATUS["SUCCESS"]:
            raise ServerException('Check failed {}'.format(hex(status)))

    def sendCMDPacket(self, cmdNumber, length, fieldBuffer = None, checkForSuccess = True):
        packet = createCmdPacket(cmdNumber, length)
        self.socket.sendall(packet)
        if fieldBuffer != None:
            self.socket.sendall(fieldBuffer)
        if checkForSuccess:
            self.checkSuccess()

    def connect(self, host, port):
        self.socket.connect((host, port))
        self.is_connected = True

    def getProcessList(self):
        self.sendCMDPacket(CMD["CMD_PROC_LIST"], 0)
        procCount = int.from_bytes(self.socket.recv(4, socket.MSG_WAITALL), "little")
        procListBuffer = self.socket.recv(procCount * ProcessListEntrySize, socket.MSG_WAITALL)
        procList = []
        for i in range(procCount):
            offset = i * ProcessListEntrySize
            procName = readCString(procListBuffer[offset:offset+32], "ascii")
            procPid = struct.unpack_from("<I", procListBuffer, offset+32)[0]
            procList.append(ProcessEntry(procName, procPid))
        return Processes(procList)

    def getProcessMaps(self, pid):
        if pid > 0xFFFFFFFF:
            raise ValueError('{} is too large'.format(pid))
        fieldBuffer = pid.to_bytes(4, byteorder='little')
        self.sendCMDPacket(CMD["CMD_PROC_MAPS"], 4, fieldBuffer)
        numOfEntries = int.from_bytes(self.socket.recv(4, socket.MSG_WAITALL), "little")
        procMapBuffer = self.socket.recv(numOfEntries * ProcessMapEntrySize, socket.MSG_WAITALL)
        procMap = []
        for i in range(numOfEntries):
            offset = i * ProcessMapEntrySize
            name = readCString(procMapBuffer[offset:offset+32])
            start = struct.unpack_from("<Q", procMapBuffer, offset + 32)[0]
            end = struct.unpack_from("<Q", procMapBuffer, offset + 40)[0]
            off = struct.unpack_from("<Q", procMapBuffer, offset + 48)[0]
            prot = struct.unpack_from("<H", procMapBuffer, offset + 56)[0]
            procMap.append(ProcessMapEntry(pid, name, start, end, off, prot))
        return ProcessMap(procMap)

    def readMemory(self, pid, start, length):
        fieldBuffer = pid.to_bytes(4, byteorder='little')
        fieldBuffer += start.to_bytes(8, byteorder='little')
        fieldBuffer += length.to_bytes(4, byteorder='little')
        self.sendCMDPacket(CMD["CMD_PROC_READ"], 16, fieldBuffer)
        return self.socket.recv(length, socket.MSG_WAITALL)

    def writeMemory(self, pid, start, buffer = b''):
        if len(buffer) == 0:
            return
        fieldBuffer = pid.to_bytes(4, byteorder='little')
        fieldBuffer += start.to_bytes(8, byteorder='little')
        fieldBuffer += len(buffer).to_bytes(4, byteorder='little')
        self.sendCMDPacket(CMD["CMD_PROC_WRITE"], 16, fieldBuffer)
        self.socket.sendall(buffer)
        self.checkSuccess()