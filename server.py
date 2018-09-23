import socket
from f1_2018_struct import *

UDP_IP = "127.0.0.1"
UDP_PORT = 20777


def get_telemetry():
    """
    Generator function which yields UDPPackets from the specified ip address and port

    :yield: A dict with all info send by F1 2018
    """
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    while True:
        data, _ = sock.recvfrom(1341)
        header = Header.from_buffer_copy(data[0:21])
        if int(header.m_packetId) == 0:
            pld = PacketMotionData.from_buffer_copy(data[21:1341])

        elif int(header.m_packetId) == 1:
            pld = PacketSessionData.from_buffer_copy(data[21:147])

        elif int(header.m_packetId) == 2:
            pld = PacketLapData.from_buffer_copy(data[21:841])

        elif int(header.m_packetId) == 3:
            pld = PacketEventData.from_buffer_copy(data[21:25])

        elif int(header.m_packetId) == 4:
            pld = PacketParticipantsData.from_buffer_copy(data[21:1082])

        elif int(header.m_packetId) == 5:
            pld = PacketCarSetupData.from_buffer_copy(data[21:841])

        elif int(header.m_packetId) == 6:
            pld = PacketCarTelemetryData.from_buffer_copy(data[21:1085])

        elif int(header.m_packetId) == 7:
            pld = PacketCarStatusData.from_buffer_copy(data[21:1061])
        yield pld


for packet in get_telemetry():
    print(packet)
