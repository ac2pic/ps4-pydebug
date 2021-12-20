import ast
from ps4debug_server import PS4DebugServer

def execute(code, predef_globals, session_locals):
    code_ast = ast.parse(code)
    nodes = ast.iter_child_nodes(code_ast)
    statements = list(nodes)
    if len(statements) == 0:
        return None

    if not isinstance(statements[-1], ast.Expr):
        compiled_code = compile(code_ast, '<ast>', 'exec')
        return eval(compiled_code, predef_globals, session_locals)
    else:
        if len(statements) > 1:
            compiled_statements = compile(ast.Module(body=statements[:-1], type_ignores=[]), "<ast>", "exec")
            exec(compiled_statements, predef_globals, session_locals)
        compiled_line = compile(ast.Expression(statements[-1].value), "<ast>", "eval")
        return eval(compiled_line, predef_globals, session_locals)

def quit():
    global should_exit
    should_exit = True


server = None

def connect(name = "", host = "", port = 0):
    global server
    if server != None:
        print("Must disconnect from server first!")
        return
    if name != "ps4debug":
        print("Invalid server specified.")
        return 
    server = PS4DebugServer()
    try:
        server.connect(host, port)
    except OSError as e:
        print(str(e))
        server = None

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

def execute_custom_code(scriptPath = ''):
    # This is going to be fun trying to catch every single error
    # Should probably let execute catch errors... or not
    scriptLines = None
    with open('{}.gr'.format(scriptPath), 'r') as scriptFile:
        scriptLines = scriptFile.read()
    return execute(scriptLines, predef_globals, session_locals)

predef_globals = {
    "__builtins__": {},
    "quit": quit,
    "connect": connect,
    "c": connect, # alias
    "processlist": get_process_list,
    "pls": get_process_list, # alias
    "pmap": get_process_map, # alias
    "exec": execute_custom_code, 
}

should_exit = False
session_locals = {}
while not should_exit:
    user_cmd = input("> ")
    result = execute(user_cmd, predef_globals, session_locals)
    if result != None:
        print(result)
