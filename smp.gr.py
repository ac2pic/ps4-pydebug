from script_stub import *

if not connect("ps4debug", "10.0.0.4", 744):
    print('Could not connect')
    quit()

fw = firmware()
if fw == 0:
    quit()
print("Doing save mounter patches for {}".format(fw))
exec("patches/sm/{}".format(fw))