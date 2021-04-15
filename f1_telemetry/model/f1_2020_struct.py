"""F1 2020 UDP Telemetry support package

This package is based on the CodeMasters Forum post documenting the F1 2020 packet format:

    https://forums.codemasters.com/topic/54423-f1%C2%AE-2020-udp-specification/

Compared to the definitions given there, the Python version has the following changes:

(1) In the 'PacketMotionData' structure, the comments for the three m_angularAcceleration{X,Y,Z} fields erroneously
    refer to 'velocity' rather than 'acceleration'. This was corrected.
(2) In the 'CarSetupData' structure, the comment of the m_rearAntiRollBar refer to rear instead of front. This was corrected.
(3) In the Driver IDs table, driver 34 has name "Wilheim Kaufmann".
    This is a typo; whenever this driver is encountered in the game, his name is given as "Wilhelm Kaufmann".
(4) In the 'CarStatusData' structure, tyreVisualCompound was renamed to visualTyreCompound.
"""

import ctypes
import enum
from typing import Dict

#########################################################
#                                                       #
#  __________  PackedLittleEndianStructure  __________  #
#                                                       #
#########################################################


class PackedLittleEndianStructure(ctypes.LittleEndianStructure):
    """The standard ctypes LittleEndianStructure, but tightly packed (no field padding), and with a proper repr() function.

    This is the base type for all structures in the telemetry data.
    """

    _pack_ = 1

    def __repr__(self):
        fstr_list = []
        for field in self._fields_:
            fname = field[0]
            value = getattr(self, fname)
            if isinstance(
                value, (PackedLittleEndianStructure, int, float, bytes)
            ):
                vstr = repr(value)
            elif isinstance(value, ctypes.Array):
                vstr = "[{}]".format(", ".join(repr(e) for e in value))
            else:
                raise RuntimeError(
                    "Bad value {!r} of type {!r}".format(value, type(value))
                )
            fstr = f"{fname}={vstr}"
            fstr_list.append(fstr)
        return "{}({})".format(self.__class__.__name__, ", ".join(fstr_list))


###########################################
#                                         #
#  __________  Packet Header  __________  #
#                                         #
###########################################


class PacketHeader(PackedLittleEndianStructure):
    """The header for each of the UDP telemetry packets."""

    _fields_ = [
        ("packetFormat", ctypes.c_uint16),
        ("gameMajorVersion", ctypes.c_uint8),
        ("gameMinorVersion", ctypes.c_uint8),
        ("packetVersion", ctypes.c_uint8),
        ("packetId", ctypes.c_uint8),
        ("sessionUID", ctypes.c_uint64),
        ("sessionTime", ctypes.c_float),
        ("frameIdentifier", ctypes.c_uint32),
        ("playerCarIndex", ctypes.c_uint8),
        ("secondaryPlayerCarIndex", ctypes.c_uint8),
    ]


@enum.unique
class PacketID(enum.IntEnum):
    """Value as specified in the PacketHeader.packetId header field, used to distinguish packet types."""

    _ignore_ = "long_description short_description"

    MOTION = 0
    SESSION = 1
    LAP_DATA = 2
    EVENT = 3
    PARTICIPANTS = 4
    CAR_SETUPS = 5
    CAR_TELEMETRY = 6
    CAR_STATUS = 7
    FINAL_CLASSIFICATION = 8
    LOBBY_INFO = 9

    long_description: Dict[enum.IntEnum, str]
    short_description: Dict[enum.IntEnum, str]


PacketID.short_description = {
    PacketID.MOTION: "Motion",
    PacketID.SESSION: "Session",
    PacketID.LAP_DATA: "Lap Data",
    PacketID.EVENT: "Event",
    PacketID.PARTICIPANTS: "Participants",
    PacketID.CAR_SETUPS: "Car Setups",
    PacketID.CAR_TELEMETRY: "Car Telemetry",
    PacketID.CAR_STATUS: "Car Status",
    PacketID.FINAL_CLASSIFICATION: "Final Classification",
    PacketID.LOBBY_INFO: "Lobby information",
}


PacketID.long_description = {
    PacketID.MOTION: "Contains all motion data for player's car – only sent while player is in control",
    PacketID.SESSION: "Data about the session – track, time left",
    PacketID.LAP_DATA: "Data about all the lap times of cars in the session",
    PacketID.EVENT: "Various notable events that happen during a session",
    PacketID.PARTICIPANTS: "List of participants in the session, mostly relevant for multiplayer",
    PacketID.CAR_SETUPS: "Packet detailing car setups for cars in the race",
    PacketID.CAR_TELEMETRY: "Telemetry data for all cars",
    PacketID.CAR_STATUS: "Status data for all cars such as damage",
    PacketID.FINAL_CLASSIFICATION: "Final classification confirmation at the end of a race",
    PacketID.LOBBY_INFO: "Information about players in a multiplayer lobby",
}

#########################################################
#                                                       #
#  __________  Packet ID 0 : MOTION PACKET  __________  #
#                                                       #
#########################################################


class CarMotionData_V1(PackedLittleEndianStructure):
    """This type is used for the 20-element 'carMotionData' array of the PacketMotionData_V1 type, defined below."""

    _fields_ = [
        ("worldPositionX", ctypes.c_float),
        ("worldPositionY", ctypes.c_float),
        ("worldPositionZ", ctypes.c_float),
        ("worldVelocityX", ctypes.c_float),
        ("worldVelocityY", ctypes.c_float),
        ("worldVelocityZ", ctypes.c_float),
        ("worldForwardDirX", ctypes.c_int16),
        ("worldForwardDirY", ctypes.c_int16),
        ("worldForwardDirZ", ctypes.c_int16),
        ("worldRightDirX", ctypes.c_int16),
        ("worldRightDirY", ctypes.c_int16),
        ("worldRightDirZ", ctypes.c_int16),
        ("gForceLateral", ctypes.c_float),
        ("gForceLongitudinal", ctypes.c_float),
        ("gForceVertical", ctypes.c_float),
        ("yaw", ctypes.c_float),
        ("pitch", ctypes.c_float),
        ("roll", ctypes.c_float),
    ]


class PacketMotionData_V1(PackedLittleEndianStructure):
    """The motion packet gives physics data for all the cars being driven.

    There is additional data for the car being driven with the goal of being able to drive a motion platform setup.

    N.B. For the normalised vectors below, to convert to float values divide by 32767.0f – 16-bit signed values are
    used to pack the data and on the assumption that direction values are always between -1.0f and 1.0f.

    Frequency: Rate as specified in menus
    Size: 1464 bytes
    Version: 1
    """

    _fields_ = [
        ("header", PacketHeader),
        ("carMotionData", CarMotionData_V1 * 22),
        # Extra player car ONLY data
        ("suspensionPosition", ctypes.c_float * 4),
        ("suspensionVelocity", ctypes.c_float * 4),
        ("suspensionAcceleration", ctypes.c_float * 4),
        ("wheelSpeed", ctypes.c_float * 4),
        ("wheelSlip", ctypes.c_float * 4),
        ("localVelocityX", ctypes.c_float),
        ("localVelocityY", ctypes.c_float),
        ("localVelocityZ", ctypes.c_float),
        ("angularVelocityX", ctypes.c_float),
        ("angularVelocityY", ctypes.c_float),
        ("angularVelocityZ", ctypes.c_float),
        ("angularAccelerationX", ctypes.c_float),
        ("angularAccelerationY", ctypes.c_float),
        ("angularAccelerationZ", ctypes.c_float),
        ("frontWheelsAngle", ctypes.c_float),
    ]


##########################################################
#                                                        #
#  __________  Packet ID 1 : SESSION PACKET  __________  #
#                                                        #
##########################################################


class MarshalZone_V1(PackedLittleEndianStructure):
    """This type is used for the 21-element 'marshalZones' array of the PacketSessionData_V1 type, defined below."""

    _fields_ = [("zoneStart", ctypes.c_float), ("zoneFlag", ctypes.c_int8)]


class WeatherForecastSample(PackedLittleEndianStructure):
    """This type is used for the 20-element 'weatherForecastSamples' array of the PacketSessionData_V1 type, defined below."""

    _fields_ = [
        ("sessionType", ctypes.c_uint8),
        ("timeOffset", ctypes.c_uint8),
        ("weather", ctypes.c_uint8),
        ("trackTemperature", ctypes.c_int8),
        ("airTemperature", ctypes.c_int8),
    ]


class PacketSessionData_V1(PackedLittleEndianStructure):
    """The session packet includes details about the current session in progress.

    Frequency: 2 per second
    Size: 251 bytes
    Version: 1
    """

    _fields_ = [
        ("header", PacketHeader),
        ("weather", ctypes.c_uint8),
        ("trackTemperature", ctypes.c_int8),
        ("airTemperature", ctypes.c_int8),
        ("totalLaps", ctypes.c_uint8),
        ("trackLength", ctypes.c_uint16),
        ("sessionType", ctypes.c_uint8),
        ("trackId", ctypes.c_int8),
        ("formula", ctypes.c_uint8),
        ("sessionTimeLeft", ctypes.c_uint16),
        ("sessionDuration", ctypes.c_uint16),
        ("pitSpeedLimit", ctypes.c_uint8),
        ("gamePaused", ctypes.c_uint8),
        ("isSpectating", ctypes.c_uint8),
        ("spectatorCarIndex", ctypes.c_uint8),
        ("sliProNativeSupport", ctypes.c_uint8),
        ("numMarshalZones", ctypes.c_uint8),
        ("marshalZones", MarshalZone_V1 * 21),
        ("safetyCarStatus", ctypes.c_uint8),
        ("networkGame", ctypes.c_uint8),
        ("numWeatherForecastSamples", ctypes.c_uint8),
        ("weatherForecastSamples", WeatherForecastSample * 20),
    ]


###########################################################
#                                                         #
#  __________  Packet ID 2 : LAP DATA PACKET  __________  #
#                                                         #
###########################################################


class LapData_V1(PackedLittleEndianStructure):
    """This type is used for the 22-element 'lapData' array of the PacketLapData_V1 type, defined below."""

    _fields_ = [
        ("lastLapTime", ctypes.c_float),
        ("currentLapTime", ctypes.c_float),
        ("sector1TimeInMS", ctypes.c_uint16),
        ("sector2TimeInMS", ctypes.c_uint16),
        ("bestLapTime", ctypes.c_float),
        ("bestLapNum", ctypes.c_uint8),
        ("bestLapSector1TimeInMS", ctypes.c_uint16),
        ("bestLapSector2TimeInMS", ctypes.c_uint16),
        ("bestLapSector3TimeInMS", ctypes.c_uint16),
        ("bestOverallSector1TimeInMS", ctypes.c_uint16),
        ("bestOverallSector1LapNum", ctypes.c_uint8),
        ("bestOverallSector2TimeInMS", ctypes.c_uint16),
        ("bestOverallSector2LapNum", ctypes.c_uint8),
        ("bestOverallSector3TimeInMS", ctypes.c_uint16),
        ("bestOverallSector3LapNum", ctypes.c_uint8),
        ("lapDistance", ctypes.c_float),
        ("totalDistance", ctypes.c_float),
        ("safetyCarDelta", ctypes.c_float),
        ("carPosition", ctypes.c_uint8),
        ("currentLapNum", ctypes.c_uint8),
        ("pitStatus", ctypes.c_uint8),
        ("sector", ctypes.c_uint8),
        ("currentLapInvalid", ctypes.c_uint8),
        ("penalties", ctypes.c_uint8),
        ("gridPosition", ctypes.c_uint8),
        ("driverStatus", ctypes.c_uint8),
        ("resultStatus", ctypes.c_uint8),
    ]


class PacketLapData_V1(PackedLittleEndianStructure):
    """The lap data packet gives details of all the cars in the session.

    Frequency: Rate as specified in menus
    Size: 1190 bytes
    Version: 1
    """

    _fields_ = [
        ("header", PacketHeader),  # Header
        ("lapData", LapData_V1 * 22),  # Lap data for all cars on track
    ]


########################################################
#                                                      #
#  __________  Packet ID 3 : EVENT PACKET  __________  #
#                                                      #
########################################################


class FastestLapData(PackedLittleEndianStructure):
    """Event data for fastest lap (FTLP)"""

    _fields_ = [
        ("vehicleIdx", ctypes.c_uint8),  # Vehicle index of car
        ("lapTime", ctypes.c_float),  # Lap time is in seconds
    ]


class PenaltyData(PackedLittleEndianStructure):
    """Event data for penalty (PENA)"""

    _fields_ = [
        ("penaltyType", ctypes.c_uint8),
        ("infringementType", ctypes.c_uint8),
        ("vehicleIdx", ctypes.c_uint8),
        ("otherVehicleIdx", ctypes.c_uint8),
        ("time", ctypes.c_uint8),
        ("lapNum", ctypes.c_uint8),
        ("placesGained", ctypes.c_uint8),
    ]


class RaceWinnerData(PackedLittleEndianStructure):
    """Event data for race winner (RCWN)"""

    _fields_ = [
        ("vehicleIdx", ctypes.c_uint8),
    ]


class RetirementData(PackedLittleEndianStructure):
    """Event data for retirement (RTMT)"""

    _fields_ = [
        ("vehicleIdx", ctypes.c_uint8),
    ]


class SpeedTrapData(PackedLittleEndianStructure):
    """Event data for speedtrap (SPTP)"""

    _fields_ = [("vehicleIdx", ctypes.c_uint8), ("speed", ctypes.c_float)]


class TeamMateInPitsData(PackedLittleEndianStructure):
    """Event data for teammate in pits (TMPT)"""

    _fields_ = [
        ("vehicleIdx", ctypes.c_uint8),
    ]


class EventDataDetails(ctypes.Union):
    """Union for the different event data types"""

    _fields_ = [
        ("fastestLap", FastestLapData),
        ("penalty", PenaltyData),
        ("raceWinner", RaceWinnerData),
        ("retirement", RetirementData),
        ("speedTrap", SpeedTrapData),
        ("teamMateInPits", TeamMateInPitsData),
    ]


class PacketEventData_V1(PackedLittleEndianStructure):
    """This packet gives details of events that happen during the course of a session.

    Frequency: When the event occurs
    Size: 35 bytes
    Version: 1
    """

    _fields_ = [
        ("header", PacketHeader),  # Header
        ("eventStringCode", ctypes.c_char * 4),
        (
            "eventDetails",
            EventDataDetails,
        ),
    ]

    def __repr__(self):
        event = self.eventStringCode.decode()

        if event in ["CHQF", "DRSD", "DRSE", "SEND", "SSTA"]:
            end = ")"
        else:
            if event == "FTLP":
                event_details = self.eventDetails.fastestLap
            elif event == "PENA":
                event_details = self.eventDetails.penalty
            elif event == "RCWN":
                event_details = self.eventDetails.raceWinner
            elif event == "RTMT":
                event_details = self.eventDetails.retirement
            elif event == "SPTP":
                event_details = self.eventDetails.speedTrap
            elif event == "TMPT":
                event_details = self.eventDetails.teamMateInPits
            else:
                raise RuntimeError(f"Bad event code {event}")

            end = f", eventDetails={event_details!r})"

        return f"{self.__class__.__name__}(header={self.header!r}, eventStringCode={self.eventStringCode!r}{end}"


@enum.unique
class EventStringCode(enum.Enum):
    """Value as specified in the PacketEventData_V1.eventStringCode header field, used to distinguish packet types."""

    _ignore_ = "long_description short_description"

    SSTA = b"SSTA"
    SEND = b"SEND"
    FTLP = b"FTLP"
    RTMT = b"RTMT"
    DRSE = b"DRSE"
    DRSD = b"DRSD"
    TMPT = b"TMPT"
    CHQF = b"CHQF"
    RCWN = b"RCWN"
    PENA = b"PENA"
    SPTP = b"SPTP"

    long_description: Dict[enum.Enum, str]
    short_description: Dict[enum.Enum, str]


EventStringCode.short_description = {
    EventStringCode.SSTA: "Session Started",
    EventStringCode.SEND: "Session Ended",
    EventStringCode.FTLP: "Fastest Lap",
    EventStringCode.RTMT: "Retirement",
    EventStringCode.DRSE: "DRS enabled",
    EventStringCode.DRSD: "DRS disabled",
    EventStringCode.TMPT: "Team mate in pits",
    EventStringCode.CHQF: "Chequered flag",
    EventStringCode.RCWN: "Race Winner",
    EventStringCode.PENA: "Penalty issued",
    EventStringCode.SPTP: "Speed trap triggered",
}


EventStringCode.long_description = {
    EventStringCode.SSTA: "Sent when the session starts",
    EventStringCode.SEND: "Sent when the session ends",
    EventStringCode.FTLP: "When a driver achieves the fastest lap",
    EventStringCode.RTMT: "When a driver retires",
    EventStringCode.DRSE: "Race control have enabled DRS",
    EventStringCode.DRSD: "Race control have disabled DRS",
    EventStringCode.TMPT: "Your team mate has entered the pits",
    EventStringCode.CHQF: "The chequered flag has been waved",
    EventStringCode.RCWN: "The race winner is announced",
    EventStringCode.PENA: "A penalty has been issued",
    EventStringCode.SPTP: "Speed trap has been triggered",
}

###############################################################
#                                                             #
#  __________  Packet ID 4 : PARTICIPANTS PACKET  __________  #
#                                                             #
###############################################################


class ParticipantData_V1(PackedLittleEndianStructure):
    """This type is used for the 22-element 'participants' array of the PacketParticipantsData_V1 type, defined below."""

    _fields_ = [
        ("aiControlled", ctypes.c_uint8),
        ("driverId", ctypes.c_uint8),
        ("teamId", ctypes.c_uint8),
        ("raceNumber", ctypes.c_uint8),
        ("nationality", ctypes.c_uint8),
        ("name", ctypes.c_char * 48),
        ("yourTelemetry", ctypes.c_uint8),
    ]


class PacketParticipantsData_V1(PackedLittleEndianStructure):
    """This is a list of participants in the race.

    If the vehicle is controlled by AI, then the name will be the driver name.
    If this is a multiplayer game, the names will be the Steam Id on PC, or the LAN name if appropriate.
    On Xbox One, the names will always be the driver name, on PS4 the name will be the LAN name if playing a LAN game,
    otherwise it will be the driver name.

    Frequency: Every 5 seconds
    Size: 1213 bytes
    Version: 1
    """

    _fields_ = [
        ("header", PacketHeader),
        ("numActiveCars", ctypes.c_uint8),
        ("participants", ParticipantData_V1 * 22),
    ]


#############################################################
#                                                           #
#  __________  Packet ID 5 : CAR SETUPS PACKET  __________  #
#                                                           #
#############################################################


class CarSetupData_V1(PackedLittleEndianStructure):
    """This type is used for the 22-element 'carSetups' array of the PacketCarSetupData_V1 type, defined below."""

    _fields_ = [
        ("frontWing", ctypes.c_uint8),
        ("rearWing", ctypes.c_uint8),
        ("onThrottle", ctypes.c_uint8),
        ("offThrottle", ctypes.c_uint8),
        ("frontCamber", ctypes.c_float),
        ("rearCamber", ctypes.c_float),
        ("frontToe", ctypes.c_float),
        ("rearToe", ctypes.c_float),
        ("frontSuspension", ctypes.c_uint8),
        ("rearSuspension", ctypes.c_uint8),
        ("frontAntiRollBar", ctypes.c_uint8),
        ("rearAntiRollBar", ctypes.c_uint8),
        ("frontSuspensionHeight", ctypes.c_uint8),
        ("rearSuspensionHeight", ctypes.c_uint8),
        ("brakePressure", ctypes.c_uint8),
        ("brakeBias", ctypes.c_uint8),
        ("rearLeftTyrePressure", ctypes.c_float),
        ("rearRightTyrePressure", ctypes.c_float),
        ("frontLeftTyrePressure", ctypes.c_float),
        ("frontRightTyrePressure", ctypes.c_float),
        ("ballast", ctypes.c_uint8),
        ("fuelLoad", ctypes.c_float),
    ]


class PacketCarSetupData_V1(PackedLittleEndianStructure):
    """This packet details the car setups for each vehicle in the session.

    Note that in multiplayer games, other player cars will appear as blank, you will only be able to see your car setup and AI cars.

    Frequency: 2 per second
    Size: 1102 bytes
    Version: 1
    """

    _fields_ = [("header", PacketHeader), ("carSetups", CarSetupData_V1 * 22)]


################################################################
#                                                              #
#  __________  Packet ID 6 : CAR TELEMETRY PACKET  __________  #
#                                                              #
################################################################


class CarTelemetryData_V1(PackedLittleEndianStructure):
    """This type is used for the 22-element 'carTelemetryData' array of the PacketCarTelemetryData_V1 type, defined below."""

    _fields_ = [
        ("speed", ctypes.c_uint16),
        ("throttle", ctypes.c_float),
        ("steer", ctypes.c_float),
        ("brake", ctypes.c_float),
        ("clutch", ctypes.c_uint8),
        ("gear", ctypes.c_int8),
        ("engineRPM", ctypes.c_uint16),
        ("drs", ctypes.c_uint8),
        ("revLightsPercent", ctypes.c_uint8),
        ("brakesTemperature", ctypes.c_uint16 * 4),
        ("tyresSurfaceTemperature", ctypes.c_uint8 * 4),
        ("tyresInnerTemperature", ctypes.c_uint8 * 4),
        ("engineTemperature", ctypes.c_uint16),
        ("tyresPressure", ctypes.c_float * 4),
        ("surfaceType", ctypes.c_uint8 * 4),
    ]


class PacketCarTelemetryData_V1(PackedLittleEndianStructure):
    """This packet details telemetry for all the cars in the race.

    It details various values that would be recorded on the car such as speed, throttle application, DRS etc.

    Frequency: Rate as specified in menus
    Size: 1307 bytes
    Version: 1
    """

    _fields_ = [
        ("header", PacketHeader),
        ("carTelemetryData", CarTelemetryData_V1 * 22),
        ("buttonStatus", ctypes.c_uint32),
        ("mfdPanelIndex", ctypes.c_uint8),
        ("mfdPanelIndexSecondaryPlayer", ctypes.c_uint8),
        ("suggestedGear", ctypes.c_int8),
    ]


#############################################################
#                                                           #
#  __________  Packet ID 7 : CAR STATUS PACKET  __________  #
#                                                           #
#############################################################


class CarStatusData_V1(PackedLittleEndianStructure):
    """This type is used for the 22-element 'carStatusData' array of the PacketCarStatusData_V1 type, defined below.

    There is some data in the Car Status packets that you may not want other players seeing if you are in a multiplayer game.
    This is controlled by the "Your Telemetry" setting in the Telemetry options. The options are:

        Restricted (Default) – other players viewing the UDP data will not see values for your car;
        Public – all other players can see all the data for your car.

    Note: You can always see the data for the car you are driving regardless of the setting.

    The following data items are set to zero if the player driving the car in question has their "Your Telemetry" set to "Restricted":

        fuelInTank
        fuelCapacity
        fuelMix
        fuelRemainingLaps
        frontBrakeBias
        frontLeftWingDamage
        frontRightWingDamage
        rearWingDamage
        engineDamage
        gearBoxDamage
        tyresWear (All four wheels)
        tyresDamage (All four wheels)
        ersDeployMode
        ersStoreEnergy
        ersDeployedThisLap
        ersHarvestedThisLapMGUK
        ersHarvestedThisLapMGUH
        tyresAgeLaps
    """

    _fields_ = [
        ("tractionControl", ctypes.c_uint8),
        ("antiLockBrakes", ctypes.c_uint8),
        ("fuelMix", ctypes.c_uint8),
        ("frontBrakeBias", ctypes.c_uint8),
        ("pitLimiterStatus", ctypes.c_uint8),
        ("fuelInTank", ctypes.c_float),
        ("fuelCapacity", ctypes.c_float),
        ("fuelRemainingLaps", ctypes.c_float),
        ("maxRPM", ctypes.c_uint16),
        ("idleRPM", ctypes.c_uint16),
        ("maxGears", ctypes.c_uint8),
        ("drsAllowed", ctypes.c_uint8),
        ("drsActivationDistance", ctypes.c_uint16),
        ("tyresWear", ctypes.c_uint8 * 4),
        ("actualTyreCompound", ctypes.c_uint8),
        ("visualTyreCompound", ctypes.c_uint8),
        ("tyresAgeLaps", ctypes.c_uint8),
        ("tyresDamage", ctypes.c_uint8 * 4),
        ("frontLeftWingDamage", ctypes.c_uint8),
        ("frontRightWingDamage", ctypes.c_uint8),
        ("rearWingDamage", ctypes.c_uint8),
        ("drsFault", ctypes.c_uint8),
        ("engineDamage", ctypes.c_uint8),
        ("gearBoxDamage", ctypes.c_uint8),
        ("vehicleFiaFlags", ctypes.c_int8),
        ("ersStoreEnergy", ctypes.c_float),
        ("ersDeployMode", ctypes.c_uint8),
        ("ersHarvestedThisLapMGUK", ctypes.c_float),
        ("ersHarvestedThisLapMGUH", ctypes.c_float),
        ("ersDeployedThisLap", ctypes.c_float),
    ]


class PacketCarStatusData_V1(PackedLittleEndianStructure):
    """This packet details car statuses for all the cars in the race.

    It includes values such as the damage readings on the car.

    Frequency: Rate as specified in menus
    Size: 1344 bytes
    Version: 1
    """

    _fields_ = [
        ("header", PacketHeader),  # Header
        ("carStatusData", CarStatusData_V1 * 22),
    ]


#############################################################
#                                                           #
#  ______  Packet ID 8 : FINAL CLASSIFICATION PACKET _____  #
#                                                           #
#############################################################


class FinalClassificationData_V1(PackedLittleEndianStructure):
    """
    This type is used for the 22-element 'classificationData' array of the PacketFinalClassificationData_V1 type, defined below.
    """

    _fields_ = [
        ("position", ctypes.c_uint8),
        ("numLaps", ctypes.c_uint8),
        ("gridPosition", ctypes.c_uint8),
        ("points", ctypes.c_uint8),
        ("numPitStops", ctypes.c_uint8),
        ("resultStatus", ctypes.c_uint8),
        ("bestLapTime", ctypes.c_float),
        ("totalRaceTime", ctypes.c_double),
        ("penaltiesTime", ctypes.c_uint8),
        ("numPenalties", ctypes.c_uint8),
        ("numTyreStints", ctypes.c_uint8),
        ("tyreStintsActual", ctypes.c_uint8 * 8),
        ("tyreStintsVisual", ctypes.c_uint8 * 8),
    ]


class PacketFinalClassificationData_V1(PackedLittleEndianStructure):
    """This packet details the final classification at the end of the race.

    This data will match with the post race results screen.

    Frequency: Once at the end of the race
    Size: 839 bytes
    Version: 1
    """

    _fields_ = [
        ("header", PacketHeader),  # Header
        (
            "numCars",
            ctypes.c_uint8,
        ),  # Number of cars in the final classification
        ("classificationData", FinalClassificationData_V1 * 22),
    ]


###############################################################
#                                                             #
#  ___________  Packet ID 9 : LOBBY INFO PACKET  ___________  #
#                                                             #
###############################################################


class LobbyInfoData_V1(PackedLittleEndianStructure):
    """This type is used for the 22-element 'lobbyPlayers' array of the PacketLobbyInfoData_V1 type, defined below."""

    _fields_ = [
        ("aiControlled", ctypes.c_uint8),
        ("teamId", ctypes.c_uint8),
        ("nationality", ctypes.c_uint8),
        ("name", ctypes.c_char * 48),
        ("readyStatus", ctypes.c_uint8),
    ]


class PacketLobbyInfoData_V1(PackedLittleEndianStructure):
    """This is a list of players in a multiplayer lobby.

    Frequency: Two every second when in the lobby
    Size: 1169 bytes
    Version: 1
    """

    _fields_ = [
        ("header", PacketHeader),  # Header
        ("numPlayers", ctypes.c_uint8),
        ("lobbyPlayers", LobbyInfoData_V1 * 22),
    ]


##################################
#                                #
#  Decode UDP telemetry packets  #
#                                #
##################################

# Map from (packetFormat, packetVersion, packetId) to a specific packet type.
HeaderFieldsToPacketType = {
    (2020, 1, 0): PacketMotionData_V1,
    (2020, 1, 1): PacketSessionData_V1,
    (2020, 1, 2): PacketLapData_V1,
    (2020, 1, 3): PacketEventData_V1,
    (2020, 1, 4): PacketParticipantsData_V1,
    (2020, 1, 5): PacketCarSetupData_V1,
    (2020, 1, 6): PacketCarTelemetryData_V1,
    (2020, 1, 7): PacketCarStatusData_V1,
    (2020, 1, 8): PacketFinalClassificationData_V1,
    (2020, 1, 9): PacketLobbyInfoData_V1,
}


class UnpackError(Exception):
    """Exception for packets that cannot be unpacked"""


def unpack_udp_packet(packet: bytes) -> PackedLittleEndianStructure:
    """Convert raw UDP packet to an appropriately-typed telemetry packet.

    Args:
        packet: the contents of the UDP packet to be unpacked.

    Returns:
        The decoded packet structure.

    Raises:
        UnpackError if a problem is detected.
    """
    actual_packet_size = len(packet)

    header_size = ctypes.sizeof(PacketHeader)

    if actual_packet_size < header_size:
        raise UnpackError(
            f"Bad telemetry packet: too short ({actual_packet_size} bytes)."
        )

    header = PacketHeader.from_buffer_copy(packet)
    key = (header.packetFormat, header.packetVersion, header.packetId)

    if key not in HeaderFieldsToPacketType:
        raise UnpackError(
            f"Bad telemetry packet: no match for key fields {key!r}."
        )

    packet_type = HeaderFieldsToPacketType[key]

    expected_packet_size = ctypes.sizeof(packet_type)

    if actual_packet_size != expected_packet_size:
        raise UnpackError(
            "Bad telemetry packet: bad size for {} packet; expected {} bytes but received {} bytes.".format(
                packet_type.__name__, expected_packet_size, actual_packet_size
            )
        )

    return packet_type.from_buffer_copy(packet)

SessionsType = {
    0: "unknown",
    1: "P1",
    2: "P2",
    3: "P3",
    4: "Short P",
    5: "Q1",
    6: "Q2",
    7: "Q3",
    8: "Short Q",
    9: "OSQ",
    10: "R",
    11: "R2",
    12: "Time Trial"
}

Weather = {
    0: "clear",
    1: "light cloud",
    2: "overcast",
    3: "light rain",
    4: "heavy rain",
    5: "storm"
}

Formula = {
    0: "F1 Modern",
    1: "F1 Classic",
    2: "F2",
}

TrackIDs = {
    0: "Melbourne",
    1: "Paul Ricard",
    2: "Shanghai",
    3: "Sakhir (Bahrain)",
    4: "Catalunya",
    5: "Monaco",
    6: "Montreal",
    7: "Silverstone",
    9: "Hungaroring",
    10: "Spa",
    11: "Monza",
    12: "Singapore",
    13: "Suzuka",
    14: "Abu Dhabi",
    15: "Texas",
    16: "Brazil",
    17: "Austria",
    18: "Sochi",
    19: "Mexico",
    20: "Baku (Azerbaijan)",
    21: "Sakhir Short",
    22: "Silverstone Short",
    23: "Texas Short",
    24: "Suzuka Short",
    25: "Hanoi",
    26: "Zandvoort",
}
