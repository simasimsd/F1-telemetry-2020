from f1_telemetry.server import get_telemetry
#from f1_telemetry.f1_2019_struct import *
import time

if __name__ == '__main__':
    print("Server started on 20777")
    for packet, theader, madonna in get_telemetry():
        #print(theader, packet)
        if theader == 1:
            print(theader, "Track: ", packet.m_trackId,
                  "Car Type: ", packet.m_formula,
                  "Safety Car: ", packet.m_safetyCarStatus,
                  "Weather:", packet.m_weather,
                  "Track Temp: ", packet.m_trackTemperature,
                  "Air Temp: ", packet.m_airTemperature,
                  "Total Laps: ", packet.m_totalLaps, time.time())

        elif theader == 2:
            print("Header ID: ", theader)
            #print(dir(madonna))
            #print(dir(packet.m_lapsData))
            #print(packet.m_lapsData.__dict__)
            #print(theader, "Test Lap:", #packet.m_lastLapTime,
                  #packet.m_currentLapTime,
                  #packet.m_bestLapTime, packet.m_sector1Time,
                  #packet.m_sector2Time, packet.m_lapDistance,
                  #packet.m_totalDistance,
            #      packet.m_lapsData)
        elif theader == 3:
            print(dir(packet.m_eventStringCode))
            print(theader, "Event ID: ", packet.m_eventStringCode._type_)
        elif theader == 4:
            print(theader, "Active Cars: ", packet.m_numActiveCars)
            #print(theader, "Test Teams:", packet.m_aiControlled,
            #      packet.m_driverId,
            #      packet.m_teamId, packet.m_raceNumber,
            #      packet.m_nationality, packet.m_name,
            #      packet.m_yourTelemetry)
        #elif theader == 5:
        #    print(packet)
