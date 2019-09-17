from f1_telemetry.server import get_telemetry

if __name__ == '__main__':
    print("Server started on 20777")
    for packet in get_telemetry():
        #print(packet)
        try:
            print("Track: ", packet.m_trackId, "Car Type: ", packet.m_formula,
                  "Safety Car: ", packet.m_safetyCarStatus,
                  "Weather:", packet.m_weather,
                  "Track Temp: ", packet.m_trackTemperature,
                  "Air Temp: ", packet.m_airTemperature,
                  "Total Laps: ", packet.m_totalLaps)
            print("Test Lap:", packet.m_lastLapTime, packet.m_currentLapTime,
                  packet.m_bestLapTime, packet.m_sector1Time,
                  packet.m_sector2Time, packet.m_lapDistance,
                  packet.m_totalDistance)
            print("Test Teams:", packet.m_aiControlled, packet.m_driverId,
                  packet.m_teamId, packet.m_raceNumber,
                  packet.m_nationality, packet.m_name,
                  packet.m_yourTelemetry)
        except:
            continue
