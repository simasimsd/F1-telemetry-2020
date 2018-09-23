from server.server import *

if __name__ == '__main__':
    for packet in get_telemetry():
        print(packet)
