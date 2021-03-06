from script_stub import *

def trackPatch(readable, address, length, buffer):
    print('Before patch', pread(readable, address, length))
    pwrite(readable, address, buffer)
    print('After patch', pread(readable, address, length))

procList = plist()
# libSceSaveData patches
libSceSaveData_offsets =  [
    0x32998,
    0x31699,
]

shellUi = procList.findByName("SceShellUI")

libSceSaveData = pmap(shellUi.pid).find("libSceSaveData.sprx")
if libSceSaveData == None:
    print("Can not find libSceSaveData in SceShellUI")
    quit()
for offset in libSceSaveData_offsets:
    trackPatch(libSceSaveData, offset, 10, b'\x00')

trackPatch(libSceSaveData, 0x01119, 1, b'\x1F')

shellCore = procList.findByName("SceShellCore")
if shellCore == None:
    print("Could not find SceShellCore")
    quit()  

processMaps = pmap(shellCore.pid)
shellCoreExec = processMaps.find("executable", prot=0b0101) # PROT_READ + PROT_EXEC
if shellCoreExec == None:
    print("Could not find executable for SceShellCore")
    quit()

# sce_sdmemory patches
memory_checks = [
    [0xD42843, 13]
]


for [address, length] in memory_checks:
    trackPatch(shellCoreExec, address, length, b'\x00')

shellCorePatches = {
    "verify_keystone": 0x7E4DC0, #verify keystone patch
    "foreign_save": 0x68BA0, #transfer mount permission patch eg mount foreign saves with write permission
    "psn_check": 0xC54F0, #patch psn check to load saves saves foreign to current account
    "psn_check2": 0x6A349, # ^
    "unk1": 0x686AE, # something something patches... 
    "unk2": 0x67FCA, # don't even remember doing this
    "unk3": 0x67798, #nevah jump
    "unk4": 0x679D5, #always jump
}

trackPatch(shellCoreExec, shellCorePatches["verify_keystone"], 10, b'\x48\x31\xC0\xC3')
trackPatch(shellCoreExec, shellCorePatches["foreign_save"], 10, b'\x31\xC0\xC3')
trackPatch(shellCoreExec, shellCorePatches["psn_check"], 10, b'\x31\xC0\xC3')
trackPatch(shellCoreExec, shellCorePatches["psn_check2"], 10, b'\x90' * 2)
trackPatch(shellCoreExec, shellCorePatches["unk1"], 10, b'\x90' * 6)
trackPatch(shellCoreExec, shellCorePatches["unk2"], 10, b'\x90' * 6)
trackPatch(shellCoreExec, shellCorePatches["unk3"], 10, b'\x90' * 2)
trackPatch(shellCoreExec, shellCorePatches["unk4"], 10, b'\x90\xE9')
