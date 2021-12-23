from script_stub import *
if not connect("ps4debug", "10.0.0.4", 744):
    print("Failed to connect")
    quit()

ebootProc = None
while ebootProc == None:
    ebootProc = plist().findByName('eboot.bin')
ebootProc.getProcessMaps().find('')