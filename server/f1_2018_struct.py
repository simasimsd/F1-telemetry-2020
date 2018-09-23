import ctypes


class Header(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for the header of a F1 2018 UDP packet
    """
    _pack_ = 1
    _fields_ = [
        ('m_packetFormat', ctypes.c_ushort),   # 2018
        ('m_packetVersion', ctypes.c_ubyte),   # Version of this packet type, all start from 1
        ('m_packetId', ctypes.c_ubyte),        # Identifier for the packet type, see below
        ('m_sessionUID', ctypes.c_ulonglong),  # Unique identifier for the session
        ('m_sessionTime', ctypes.c_float),     # Session timestamp
        ('m_frameIdentifier', ctypes.c_uint),  # Identifier for the frame the data was retrieved on
        ('m_playerCarIndex', ctypes.c_ubyte)   # Index of player's car in the array
    ]


class CarMotionData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for a single car motion data of a F1 2018 UDP packet

     The motion packet gives physics data for all the cars being driven. There is additional data for the car being
     driven with the goal of being able to drive a motion platform setup.

     Frequency: Rate as specified in menus
    """
    _pack_ = 1
    _fields_ = [
        ('m_worldPositionX', ctypes.c_float),      # World space X position
        ('m_worldPositionY', ctypes.c_float),      # World space Y position
        ('m_worldPositionZ', ctypes.c_float),      # World space Z position
        ('m_worldVelocityX', ctypes.c_float),      # Velocity in world space X
        ('m_worldVelocityY', ctypes.c_float),      # Velocity in world space Y
        ('m_worldVelocityZ', ctypes.c_float),      # Velocity in world space Z
        ('m_worldForwardDirX', ctypes.c_ushort),   # World space forward X direction (normalised)
        ('m_worldForwardDirY', ctypes.c_ushort),   # World space forward Y direction (normalised)
        ('m_worldForwardDirZ', ctypes.c_ushort),   # World space forward Z direction (normalised)
        ('m_worldRightDirX', ctypes.c_ushort),     # World space right X direction (normalised)
        ('m_worldRightDirY', ctypes.c_ushort),     # World space right Y direction (normalised)
        ('m_worldRightDirZ', ctypes.c_ushort),     # World space right Z direction (normalised)
        ('m_gForceLateral', ctypes.c_float),       # Lateral G-Force component
        ('m_gForceLongitudinal', ctypes.c_float),  # Longitudinal G-Force component
        ('m_gForceVertical', ctypes.c_float),      # Vertical G-Force component
        ('m_yaw', ctypes.c_float),                 # Yaw angle in radians
        ('m_pitch', ctypes.c_float),               # Pitch angle in radians
        ('m_roll', ctypes.c_float)                 # Roll angle in radians
    ]


class PacketMotionData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for the car data portion of a F1 2018 UDP packet
    """
    _pack_ = 1
    _fields_ = [
        ('cars_motion_data', CarMotionData * 20),          # Data for all cars on track
        ('m_suspensionPosition', ctypes.c_float * 4),      # Note: All wheel arrays have the following order:
        ('m_suspensionVelocity', ctypes.c_float * 4),      # RL, RR, FL, FR
        ('m_suspensionAcceleration', ctypes.c_float * 4),  # RL, RR, FL, FR
        ('m_wheelSpeed', ctypes.c_float * 4),              # Speed of each wheel
        ('m_wheelSlip', ctypes.c_float * 4),               # Slip ratio for each wheel
        ('m_localVelocityX', ctypes.c_float),              # Velocity in local space
        ('m_localVelocityY', ctypes.c_float),              # Velocity in local space
        ('m_localVelocityZ', ctypes.c_float),              # Velocity in local space
        ('m_angularVelocityX', ctypes.c_float),            # Angular velocity x-component
        ('m_angularVelocityY', ctypes.c_float),            # Angular velocity y-component
        ('m_angularVelocityZ', ctypes.c_float),            # Angular velocity z-component
        ('m_angularAccelerationX', ctypes.c_float),        # Angular velocity x-component
        ('m_angularAccelerationY', ctypes.c_float),        # Angular velocity y-component
        ('m_angularAccelerationZ', ctypes.c_float),        # Angular velocity z-component
        ('m_frontWheelsAngle', ctypes.c_float)             # Current front wheels angle in radians
    ]


class MarshalZone(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for the car data portion of a F1 2018 UDP packet
    """
    _pack_ = 1
    _fields_ = [
        ('m_zoneStart', ctypes.c_float),  # Fraction (0..1) of way through the lap the marshal zone starts
        ('m_zoneFlag', ctypes.c_byte)     # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red
    ]


class PacketSessionData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for the car data portion of a F1 2018 UDP packet
    """
    _pack_ = 1
    _fields_ = [
        ('m_weather', ctypes.c_ubyte),              # Weather - 0 = clear, 1 = light cloud, 2 = overcast
                                                    # 3 = light rain, 4 = heavy rain, 5 = storm
        ('m_trackTemperature', ctypes.c_byte),      # Track temp. in degrees celsius
        ('m_airTemperature', ctypes.c_byte),        # Air temp. in degrees celsius
        ('m_totalLaps', ctypes.c_ubyte),            # Total number of laps in this race
        ('m_trackLength', ctypes.c_ushort),         # Track length in metres
        ('m_sessionType', ctypes.c_ubyte),          # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P,  5 = Q1, 6 = Q2
                                                    # 7 = Q3, 8 = Short Q, 9 = OSQ, 10 = R, 11 = R2, 12 = Time Trial
        ('m_trackId', ctypes.c_byte),               # -1 for unknown, 0-21 for tracks, see appendix
        ('m_era', ctypes.c_ubyte),                  # Era, 0 = modern, 1 = classic
        ('m_sessionTimeLeft', ctypes.c_ushort),     # Time left in session in seconds
        ('m_sessionDuration', ctypes.c_ushort),     # Session duration in seconds
        ('m_pitSpeedLimit', ctypes.c_ubyte),        # Pit speed limit in kilometres per hour
        ('m_gamePaused', ctypes.c_ubyte),           # Whether the game is paused
        ('m_isSpectating', ctypes.c_ubyte),         # Whether the player is spectating
        ('m_spectatorCarIndex', ctypes.c_ubyte),    # Index of the car being spectated
        ('m_sliProNativeSupport', ctypes.c_ubyte),  # SLI Pro support, 0 = inactive, 1 = active
        ('m_numMarshalZones', ctypes.c_ubyte),      # Number of marshal zones to follow
        ('m_marshalZones', MarshalZone * 21),       # List of marshal zones – max 21List of marshal zones – max 21
        ('m_safetyCarStatus', ctypes.c_ubyte),      # 0 = no safety car, 1 = full safety car, 2 = virtual safety car
        ('m_networkGame', ctypes.c_ubyte),          # 0 = offline, 1 = online
    ]


class LapData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for the car data portion of a F1 2018 UDP packet
    """
    _pack_ = 1
    _fields_ = [
        ('m_lastLapTime', ctypes.c_float),        # Last lap time in seconds
        ('m_currentLapTime', ctypes.c_float),     # Current time around the lap in seconds
        ('m_bestLapTime', ctypes.c_float),        # Best lap time of the session in seconds
        ('m_sector1Time', ctypes.c_float),        # Sector 1 time in seconds
        ('m_sector2Time', ctypes.c_float),        # Sector 2 time in seconds
        ('m_lapDistance', ctypes.c_float),        # Distance vehicle is around current lap in metres – could
                                                  # be negative if line hasn’t been crossed yet
        ('m_totalDistance', ctypes.c_float),      # Total distance travelled in session in metres – could
                                                  # be negative if line hasn’t been crossed yet
        ('m_safetyCarDelta', ctypes.c_float),     # Delta in seconds for safety car
        ('m_carPosition', ctypes.c_ubyte),        # Car race position
        ('m_currentLapNum', ctypes.c_ubyte),      # Current lap number
        ('m_pitStatus', ctypes.c_ubyte),          # 0 = none, 1 = pitting, 2 = in pit area
        ('m_sector', ctypes.c_ubyte),             # 0 = sector1, 1 = sector2, 2 = sector3
        ('m_currentLapInvalid', ctypes.c_ubyte),  # Current lap invalid - 0 = valid, 1 = invalid
        ('m_penalties', ctypes.c_ubyte),          # Accumulated time penalties in seconds to be added
        ('m_gridPosition', ctypes.c_ubyte),       # Grid position the vehicle started the race in
        ('m_driverStatus', ctypes.c_ubyte),       # Grid position the vehicle started the race in
        ('m_resultStatus', ctypes.c_ubyte)        #
    ]


class PacketLapData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for the car data portion of a F1 2018 UDP packet
    """
    _pack_ = 1
    _fields_ = [
        ('laps_data', LapData * 20)
    ]


class PacketEventData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for a single car motion data of a F1 2018 UDP packet
    """
    _pack_ = 1
    _fields_ = [
        ('m_eventStringCode', ctypes.c_char * 4),
    ]


class ParticipantData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for a single car motion data of a F1 2018 UDP packet
    """
    _pack_ = 1
    _fields_ = [
        ('m_aiControlled', ctypes.c_ubyte),
        ('m_driverId', ctypes.c_ubyte),
        ('m_teamId', ctypes.c_ubyte),
        ('m_raceNumber', ctypes.c_ubyte),
        ('m_nationality', ctypes.c_ubyte),
        ('m_name', ctypes.c_char * 48)
    ]


class PacketParticipantsData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for a single car motion data of a F1 2018 UDP packet
    """
    _pack_ = 1
    _fields_ = [
        ('m_numCars', ctypes.c_ubyte),
        ('participants_data', ParticipantData * 20),
    ]


class CarSetupData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for a single car motion data of a F1 2018 UDP packet
    """
    _pack_ = 1
    _fields_ = [
        ('m_frontWing', ctypes.c_ubyte),
        ('m_rearWing', ctypes.c_ubyte),
        ('m_onThrottle', ctypes.c_ubyte),
        ('m_offThrottle', ctypes.c_ubyte),
        ('m_frontCamber', ctypes.c_float),
        ('m_rearCamber', ctypes.c_float),
        ('m_frontToe', ctypes.c_float),
        ('m_rearToe', ctypes.c_ubyte),
        ('m_frontSuspension', ctypes.c_ubyte),
        ('m_rearSuspension', ctypes.c_ubyte),
        ('m_frontAntiRollBar', ctypes.c_ubyte),
        ('m_rearAntiRollBar', ctypes.c_ubyte),
        ('m_frontSuspensionHeight', ctypes.c_ubyte),
        ('m_rearSuspensionHeight', ctypes.c_ubyte),
        ('m_brakePressure', ctypes.c_ubyte),
        ('m_brakeBias', ctypes.c_ubyte),
        ('m_frontTyrePressure', ctypes.c_float),
        ('m_rearTyrePressure', ctypes.c_float),
        ('m_ballast', ctypes.c_ubyte),
        ('m_fuelLoad', ctypes.c_float),
    ]


class PacketCarSetupData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for a single car motion data of a F1 2018 UDP packet
    """
    _pack_ = 1
    _fields_ = [
        ('m_numCars', ctypes.c_ubyte),
        ('cars_setup_data', CarSetupData * 20),
    ]


class CarTelemetryData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for a single car motion data of a F1 2018 UDP packet
    """
    _pack_ = 1
    _fields_ = [
        ('m_speed', ctypes.c_ushort),
        ('m_throttle', ctypes.c_ubyte),
        ('m_steer', ctypes.c_byte),
        ('m_brake', ctypes.c_ubyte),
        ('m_clutch', ctypes.c_ubyte),
        ('m_gear', ctypes.c_byte),
        ('m_engineRPM', ctypes.c_ushort),
        ('m_drs', ctypes.c_ubyte),
        ('m_revLightsPercent', ctypes.c_ubyte),
        ('m_brakesTemperature', ctypes.c_ushort * 4),
        ('m_tyresSurfaceTemperature', ctypes.c_ushort * 4),
        ('m_tyresInnerTemperature', ctypes.c_ushort * 4),
        ('m_engineTemperature', ctypes.c_ushort),
        ('m_tyresPressure', ctypes.c_float * 4),
    ]


class PacketCarTelemetryData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for a single car motion data of a F1 2018 UDP packet
    """
    _pack_ = 1
    _fields_ = [
        ('cars_telemetry_data', CarTelemetryData * 20),
        ('m_buttonStatus', ctypes.c_uint)
    ]


class CarStatusData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for a single car motion data of a F1 2018 UDP packet
    """
    _pack_ = 1
    _fields_ = [
        ('m_tractionControl', ctypes.c_ubyte),
        ('m_antiLockBrakes', ctypes.c_ubyte),
        ('m_fuelMix', ctypes.c_ubyte),
        ('m_frontBrakeBias', ctypes.c_ubyte),
        ('m_pitLimiterStatus', ctypes.c_ubyte),
        ('m_fuelInTank', ctypes.c_float),
        ('m_fuelCapacity', ctypes.c_float),
        ('m_maxRPM', ctypes.c_ushort),
        ('m_idleRPM', ctypes.c_ushort),
        ('m_maxGears', ctypes.c_ubyte),
        ('m_drsAllowed', ctypes.c_ubyte),
        ('m_tyresWear', ctypes.c_ubyte * 4),
        ('m_tyreCompound', ctypes.c_ubyte),
        ('m_tyresDamage', ctypes.c_ubyte * 4),
        ('m_frontLeftWingDamage', ctypes.c_ubyte),
        ('m_frontRightWingDamage', ctypes.c_ubyte),
        ('m_rearWingDamage', ctypes.c_ubyte),
        ('m_engineDamage', ctypes.c_ubyte),
        ('m_gearBoxDamage', ctypes.c_ubyte),
        ('m_exhaustDamage', ctypes.c_ubyte),
        ('m_vehicleFiaFlags', ctypes.c_byte),
        ('m_ersStoreEnergy', ctypes.c_float),
        ('m_ersDeployMode', ctypes.c_ubyte),
        ('m_ersHarvestedThisLapMGUK', ctypes.c_float),
        ('m_ersHarvestedThisLapMGUH', ctypes.c_float),
        ('m_ersDeployedThisLap', ctypes.c_float),
    ]


class PacketCarStatusData(ctypes.LittleEndianStructure):
    """
    Ctypes data structure for a single car motion data of a F1 2018 UDP packet
    """
    _pack_ = 1
    _fields_ = [
        ('cars_status_data', CarStatusData * 20)
    ]