from f1_telemetry.server import get_telemetry

if __name__ == '__main__':
    for packet in get_telemetry():
        print(packet)
