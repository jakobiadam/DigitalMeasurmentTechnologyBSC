
import argparse
import socket
import select
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help = "save measurement data to this file", type = str, default = "")
    parser.add_argument("--ip", help = "proxy server ip address", type = str, default = '157.181.168.33')
    parser.add_argument("-p", "--port", help = "proxy server port", type = int, default = 9999)
    parser.add_argument("-w", "--timeout", help = "network blocking timeout", type = float, default = .1)
    parser.add_argument("-c", "--chunk", help = "chunk of bytes", type = int, default = 1024)
    parser.add_argument("-f", "--flush", help = "flush every newline", type = bool, default = True)
    args = parser.parse_args()

    try:
        f = open(args.output, 'wb') if args.output else sys.stdout.buffer
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.settimeout(args.timeout)
        server.connect((args.ip, args.port))
        while True:
            readable, _, exceptional = select.select([server], [], [server])
            if server in readable:
                data = server.recv(args.chunk)
                f.write(data)
                if args.flush and (b'\n' in data):
                    f.flush()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        if f != sys.stdout.buffer:
            f.close()

