import socket
import select
import time

RESET = b'r\n'
SOLDERING_IRON_OFF = b'p65535\n'
SOLDERING_IRON_ON = b'p36322\n'
PELTIER_OFF = b'h0\n'
PELTIER_HEAT = b'f48080\n'
PELTIER_COOL = b'h38941\n'

SERVER = '157.181.168.33'
PORT = 9999
TIMEOUT = .1

def _connect():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.settimeout(TIMEOUT)
    server.connect((SERVER, PORT))
    return server

def _write(server, msg):
    while True:
        _, writable, exceptional = select.select([], [server], [server])
        if server in writable:
            server.sendall(msg)
            break

def reset():
    """
    @summary: make sure soldering iron is off, peltier is off and timestamp count from 0
    """
    s = _connect()
    _write(s, RESET)
    # NOTE: make sure reset loop is over, when in the reset loop serial line is not properly read for the next instruction
    s.close()
    print ("Be a little patient...")
    time.sleep(3)
    s = _connect()
    _write(s, SOLDERING_IRON_OFF)
    s.close()
    
def soldering(state):
    """
    @summary: control soldering iron
    @param state: what to do. 0 means off, 1 means heating
    @type state: 0 or 1
    """
    assert state in [0, 1], "state parameter must be 0 or 1"
    msg = SOLDERING_IRON_ON if state else SOLDERING_IRON_OFF
    s = _connect()
    _write(s, msg)
    s.close()

def peltier(state):
    """
    @summary: control peltier unit
    @param state: what to do. 0 means off, 1 means heating, -1 means cooling
    @type state: 0 or 1, -1
    """
    assert state in [0, 1, -1], "state parameter must be 0, 1 or -1"
    if state == 1:
        msg = PELTIER_HEAT
    elif state == -1:
        msg = PELTIER_COOL
    else:
        msg = PELTIER_OFF
    s = _connect()
    _write(s, msg)
    s.close()
