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
        elif theader == 4:
            #print("ID: ", theader)
            for participantdata in packet.m_participants:
                print(theader, "Active Cars: ", packet.m_numActiveCars,
                      "AI Car?: ", participantdata.m_aiControlled,
                      "Driver: ", participantdata.m_driverId,
                      "Team: ", participantdata.m_teamId,
                      "Race Number: ", participantdata.m_raceNumber,
                      "Nationality: ", participantdata.m_nationality,
                      "Player Name", participantdata.m_name)
        elif theader == 5:
            for setupdata in packet.m_carSetups:
                print(theader, "Front Wing: ", setupdata.m_frontWing,
                      "Rear Wing: ", setupdata.m_rearWing,
                      "Differential on throttle: ", setupdata.m_onThrottle,
                      "Differential off throttle: ", setupdata.m_offThrottle,
                      "Front camber: ", setupdata.m_frontCamber,
                      "Rear camber: ", setupdata.m_rearCamber,
                      "Front toe: ", setupdata.m_frontToe,
                      "Rear toe: ", setupdata.m_rearToe,
                      "Front suspension: ", setupdata.m_frontSuspension,
                      "Rear suspension: ", setupdata.m_rearSuspension,
                      "Front bar: ", setupdata.m_frontAntiRollBar,
                      "Rear bar: ", setupdata.m_rearAntiRollBar,
                      "Front height: ", setupdata.m_frontSuspensionHeight,
                      "Rear height: ", setupdata.m_rearSuspensionHeight,
                      "Brake pressure (%): ", setupdata.m_brakePressure,
                      "Brake bias (%): ", setupdata.m_brakeBias,
                      "Front Tyre (PSI): ", setupdata.m_frontTyrePressure,
                      "Rear tyre (PSI): ", setupdata.m_rearTyrePressure,
                      "Ballast: ", setupdata.m_ballast,
                      "Fuel Load: ", setupdata.m_fuelLoad)
