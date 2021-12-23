from script_stub import *

connect("ps4debug", "10.0.0.4", 744)
if not connected:
    quit()

fw = firmware()
if fw == 0:
    quit()
print("Doing save mounter patches for {}".format(fw))
exec("patches/sm/{}".format(fw))