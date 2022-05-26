import argparse
import ast
from base_server import BaseServer, ExitException, ServerException
from ps4debug_server import PS4DebugServer

def execute(code, predef_globals, session_locals):
    code_ast = ast.parse(code)
    nodes = ast.iter_child_nodes(code_ast)
    statements = list(nodes)
    if len(statements) == 0:
        return None
    
    # Filter for imports
    # Only used for types
    import_filter = lambda statement: not (isinstance(statement, ast.ImportFrom) or isinstance(statement, ast.Import))
    statements = list(filter(import_filter, statements))
    code_ast = ast.Module(body=statements, type_ignores=[])
    if not isinstance(statements[-1], ast.Expr):
        compiled_code = compile(code_ast, '<ast>', 'exec')
        return eval(compiled_code, predef_globals, session_locals)
    else:
        if len(statements) > 1:
            compiled_statements = compile(ast.Module(body=statements[:-1], type_ignores=[]), "<ast>", "exec")
            exec(compiled_statements, predef_globals, session_locals)
        compiled_line = compile(ast.Expression(statements[-1].value), "<ast>", "eval")
        return eval(compiled_line, predef_globals, session_locals)

server = None

backends = {
    "ps4debug": PS4DebugServer
}

def connect(name = "", host = "", port = 0):
    global server
    if server != None:
        sock_host, sock_port = server.socket.getpeername()
        if sock_host != host or sock_port != port:
            print("Must disconnect from server first!")
            return False
        return True
    if backends.get(name, None) == None:
        print("Invalid backend specified.")
        return False
    server = backends[name]()
    if not server.connect(host, port):
        server = None
        return False
    return True

def get_ps4_fw():
    if server == None:
        print("Not connected to a server")
        return 0
    return server.getFirmware()

def get_process_map(pid = -100000):
    if server == None:
        print("Not connected to a server")
        return None
    if pid == -100000:
        print("Must add pid")
        return None
    return server.getProcessMaps(pid)

def get_process_list():
    if server == None:
        print("Not connected to a server")
        return None
    return server.getProcessList()

def execute_custom_code(scriptPath = '', inheritLocals = True):
    # This is going to be fun trying to catch every single error
    # Should probably let execute catch errors... or not
    scriptLines = None
    with open('{}.gr.py'.format(scriptPath), 'r') as scriptFile:
        scriptLines = scriptFile.read()
    try:
        return execute(scriptLines, predef_globals, session_locals)
    except ServerException as e:
        print(e.args[0])
    except ExitException:
        pass
    return None

    
def read_process_memory(readable, offset = 0, length=0):
    return server.readMemory(readable.pid, readable.start + offset, length)

def write_process_memory(readable, offset = 0, buffer = b''):
    return server.writeMemory(readable.pid, readable.start + offset, buffer)

def exec_exit():
    raise ExitException


def execute_patches(patches):
    pass


def display(*args, **kwargs):
    print(*args, **kwargs)

predef_globals = {
    "__builtins__": {
        "hex": hex,
        "locals": locals,
    },
    "firmware": get_ps4_fw,
    "apply_patches": execute_patches,
    "quit": exec_exit,
    "connect": connect,
    "plist": get_process_list, 
    "pmap": get_process_map,
    "pread": read_process_memory,
    "pwrite": write_process_memory,
    "exec": execute_custom_code,
    "print": display,
}

session_locals = {
    "connected": False
}

parser = argparse.ArgumentParser(description='Do stuff')

parser.add_argument('-e', '--execute', help='Execute some instructions and exit.')

args = parser.parse_args()

if args.execute:
    result = execute(args.execute, predef_globals, session_locals)
    if result != None:
        print(result)
    exit(0)

while True:
    user_cmd = input("> ")
    try:
        result = execute(user_cmd, predef_globals, session_locals)
        if result != None:
            print(result)
    except ExitException:
        break
