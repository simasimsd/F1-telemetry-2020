from f1_telemetry.server import get_telemetry
import time

if __name__ == '__main__':
    print("Server started on 20777")
    for packet, theader, mad, player in get_telemetry():
        #print(theader, packet)
        if theader == 0:
            print(theader, packet.m_wheelSpeed[0], packet.m_wheelSpeed[1],
                  packet.m_wheelSpeed[2], packet.m_wheelSpeed[3])

        elif theader == 1:
            print(theader, "Track: ", packet.m_trackId,
                  "Car Type: ", packet.m_formula,
                  "Safety Car: ", packet.m_safetyCarStatus,
                  "Weather:", packet.m_weather,
                  "Track Temp: ", packet.m_trackTemperature,
                  "Air Temp: ", packet.m_airTemperature,
                  "Total Laps: ", packet.m_totalLaps, time.time())

        elif theader == 2:
            #print(dir(mad)
            for lapdata in packet.m_lapsData:
                #print(dir(lapdata))
                print(theader, "Driver: ", player, "Last LapTime:", lapdata.m_lastLapTime,
                      "Current LapTime: ", lapdata.m_currentLapTime,
                      "Best LapTime: ", lapdata.m_bestLapTime,
                      "T1 Time: ", lapdata.m_sector1Time,
                      "T2 Time: ", lapdata.m_sector2Time,
                      "Sector: ", lapdata.m_sector,
                      "Car position: ", lapdata.m_carPosition,
                      "Current Lap Numb: ", lapdata.m_currentLapNum,
                      "Lap Distance: ", lapdata.m_lapDistance,
                      "Total Lap Distance: ", lapdata.m_totalDistance)

        #elif theader == 3:
            #print(dir(packet.m_eventStringCode))
            #print(theader, "Event ID: ", packet.m_eventStringCode._type_)
        #elif theader == 4:
            #print(theader, "Active Cars: ", packet.m_numActiveCars)
            #print(theader, "Test Teams:", packet.m_aiControlled,
            #      packet.m_driverId,
            #      packet.m_teamId, packet.m_raceNumber,
            #      packet.m_nationality, packet.m_name,
            #      packet.m_yourTelemetry)
        #elif theader == 5:
        #    print(packet)
