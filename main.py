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
                      "Front tyre (PSI): ", setupdata.m_frontTyrePressure,
                      "Rear tyre (PSI): ", setupdata.m_rearTyrePressure,
                      "Ballast: ", setupdata.m_ballast,
                      "Fuel Load: ", setupdata.m_fuelLoad)

        elif theader == 6:
            for cartelemetrydata in packet.m_carTelemetryData:
                print(theader, "Speed (kph): ", cartelemetrydata.m_speed,
                      "Throttle (%): ", cartelemetrydata.m_throttle,
                      "Steering (%): ", cartelemetrydata.m_steer,
                      "Brake (%): ", cartelemetrydata.m_brake,
                      "Clutch (%): ", cartelemetrydata.m_clutch,
                      "Gear: ", cartelemetrydata.m_gear,
                      "Engine RPM: ", cartelemetrydata.m_engineRPM,
                      "DRS enabled: ", cartelemetrydata.m_drs,
                      "Rev lights (%): ", cartelemetrydata.m_revLightsPercent,
                      "Brake T (C): ", cartelemetrydata.m_brakesTemperature,
                      "FL tyre surface T (C): ", cartelemetrydata.m_tyresSurfaceTemperature[0],
                      "FR Tyre surface T (C): ", cartelemetrydata.m_tyresSurfaceTemperature[1],
                      "RL Tyre surface T (C): ", cartelemetrydata.m_tyresSurfaceTemperature[2],
                      "RR Tyre surface T (C): ", cartelemetrydata.m_tyresSurfaceTemperature[3],
                      "FL tyre inner T (C): ", cartelemetrydata.m_tyresInnerTemperature[0],
                      "FR tyre inner T (C): ", cartelemetrydata.m_tyresInnerTemperature[1],
                      "RL tyre inner T (C): ", cartelemetrydata.m_tyresInnerTemperature[2],
                      "RR tyre inner T (C): ", cartelemetrydata.m_tyresInnerTemperature[3],
                      "Engine T (C): ", cartelemetrydata.m_engineTemperature,
                      "FL Tyre pressure (PSI): ", cartelemetrydata.m_tyresPressure[0],
                      "FR tyre pressure (PSI): ", cartelemetrydata.m_tyresPressure[1],
                      "RL tyre pressure (PSI): ", cartelemetrydata.m_tyresPressure[2],
                      "RR tyre  pressure (PSI): ", cartelemetrydata.m_tyresPressure[3],
                      "FL Driving surface: ", cartelemetrydata.m_surfaceType[0],
                      "FR tyre surface: ", cartelemetrydata.m_surfaceType[1],
                      "RL tyre surface: ", cartelemetrydata.m_surfaceType[2],
                      "RR tyre surface: ", cartelemetrydata.m_surfaceType[3])
        elif theader == 7:
            for carstatusdata in packet.m_carStatusData:
                print(theader,
                      "Traction: ", carstatusdata.m_tractionControl,
                      "ABS: ", carstatusdata.m_antiLockBrakes,
                      "Fuel mix: ", carstatusdata.m_fuelMix,
                      "Front brake bias (%): ", carstatusdata.m_frontBrakeBias,
                      "Pit limiter: ", carstatusdata.m_pitLimiterStatus,
                      "Fuel mass: ", carstatusdata.m_fuelInTank,
                      "Fuel capacity: ", carstatusdata.m_fuelCapacity,
                      "Remaining Fuel: ", carstatusdata.m_fuelRemainingLaps,
                      "Cars idle RPM: ", carstatusdata.m_idleRPM,
                      "Number of Gears: ", carstatusdata.m_maxGears,
                      "DRS Allowed?: ", carstatusdata.m_drsAllowed,
                      "FL tyre wear (%): ", carstatusdata.m_tyresWear[0],
                      "FR tyre wear (%): ", carstatusdata.m_tyresWear[1],
                      "RL tyre wear (%): ", carstatusdata.m_tyresWear[2],
                      "RR tyre wear (%): ", carstatusdata.m_tyresWear[3],
                      "Tyre compound: ", carstatusdata.m_actualTyreCompound,
                      "Tyre visual compound: ", carstatusdata.m_tyreVisualCompound,
                      "FL tyre damage (%): ", carstatusdata.m_tyresDamage[0],
                      "FR tyre damage (%): ", carstatusdata.m_tyresDamage[1],
                      "RL tyre damage (%): ", carstatusdata.m_tyresDamage[2],
                      "RR tyre damage (%): ", carstatusdata.m_tyresDamage[3],
                      "Front Left wing damage (%): ", carstatusdata.m_frontLeftWingDamage,
                      "Front Right wing damage (%): ", carstatusdata.m_frontRightWingDamage,
                      "Rear Left  damage (%): ", carstatusdata.m_rearWingDamage,
                      "Rear Right damage (%): ", carstatusdata.m_engineDamage,
                      "Gearbox damage (%): ", carstatusdata.m_gearBoxDamage,
                      "Flags: ", carstatusdata.m_vehicleFiaFlags,
                      "ERS Energy (Joules): ", carstatusdata.m_ersStoreEnergy,
                      "ERS Mode: ", carstatusdata.m_ersDeployMode,
                      "ERS harvested MGU-K: ", carstatusdata.m_ersHarvestedThisLapMGUK,
                      "ERS harvested MGU-H: ", carstatusdata. m_ersHarvestedThisLapMGUH,
                      "ERS Deployed: ", carstatusdata.m_ersDeployedThisLap)
