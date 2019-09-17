from f1_telemetry.server import get_telemetry

if __name__ == '__main__':
    print("Server started on 20777")
    for packet, data in get_telemetry():
        #print(packet)
        try:
            print(packet.m_trackId, packet.m_formula,
                  packet.m_safetyCarStatus, packet.m_weather,
                  packet.m_trackTemperature, packet.m_airTemperature,
                  packet.m_totalLaps)
            #print("Due:", packet.m_lastLapTime, packet.m_currentLapTime,
            #      packet.m_bestLapTime, packet.m_sector1Time,
            #      packet.m_sector2Time, packet.m_lapDistance,
            #      packet.m_totalDistance)
        except:
            continue
