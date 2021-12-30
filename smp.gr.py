from script_stub import *
ip = "10.0.0.5"
port = 744
print('Trying to connect to {}:{}'.format(ip, port))
if not connect("ps4debug", ip, port):
    print('Could not connect')
    quit()

fw = firmware()
if fw == 0:
    quit()
print("Doing save mounter patches for {}".format(fw))
exec("patches/sm/{}".format(fw))