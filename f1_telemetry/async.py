import asyncio
import logging
import time
from datetime import datetime
from decimal import Decimal

from elasticsearch import Elasticsearch

from model.f1_2020_struct import *


class F1UdpReceiver(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        es = Elasticsearch("http://elasticsearch:9200")
        header = PacketHeader.from_buffer_copy(data[0:24])
        if int(header.packetId) == 1:
            packet = PacketSessionData_V1.from_buffer_copy(data[0:251])
            data = {
                "session_ts": header.sessionTime,
                "@timestamp": datetime.utcnow().isoformat(),
                "session_UUID": str(header.sessionUID),
                "frame_id": header.frameIdentifier,
                "track": TrackIDs[packet.trackId],
                "type": SessionsType[packet.sessionType],
                "weather": Weather[packet.weather],
                "car_type": Formula[packet.formula],
                "track_temp": packet.trackTemperature,
                "air_temp": packet.airTemperature,
                "total_laps": packet.totalLaps,
                "track_length": packet.trackLength,
            }
            data["name"] = f"{data['track']} - {data['type']} - {data['weather']} - {datetime.utcnow().isoformat()}"
            es.index(index="f1", body=data, request_timeout=30)

        elif int(header.packetId) == 2:
            packet = PacketLapData_V1.from_buffer_copy(data[0:1190])
            data = {
                "session_ts": header.sessionTime,
                "@timestamp": datetime.utcnow().isoformat(),
                "packet_id": header.packetId,
                "session_UUID": str(header.sessionUID),
                "session_time": header.sessionTime,
                "frame_id": header.frameIdentifier,
                "player_index": header.playerCarIndex,
                "lap_uuid": f"{header.sessionUID}-{header.playerCarIndex}-{header.frameIdentifier}",
                "last_lap_time": Decimal(packet.lapData[header.playerCarIndex].lastLapTime),
                "current_lap_time": Decimal(packet.lapData[header.playerCarIndex].currentLapTime),
                "best_lap_time": Decimal(packet.lapData[header.playerCarIndex].bestLapTime),
                "s1": Decimal(packet.lapData[header.playerCarIndex].sector1TimeInMS),
                "s2": Decimal(packet.lapData[header.playerCarIndex].sector2TimeInMS),
                "lap_distance": Decimal(packet.lapData[header.playerCarIndex].lapDistance),
                "total_distance": Decimal(packet.lapData[header.playerCarIndex].totalDistance),
                "car_position": packet.lapData[header.playerCarIndex].carPosition,
                "current_lap_num": packet.lapData[header.playerCarIndex].currentLapNum,
                "pit_status": packet.lapData[header.playerCarIndex].pitStatus,
                "sector": packet.lapData[header.playerCarIndex].sector,
                "lap_invalid": packet.lapData[header.playerCarIndex].currentLapInvalid,
                "penalities": packet.lapData[header.playerCarIndex].penalties,
                "grid_pos": packet.lapData[header.playerCarIndex].gridPosition,
                "driver_status": packet.lapData[header.playerCarIndex].driverStatus,
                "result_status": packet.lapData[header.playerCarIndex].resultStatus
            }
            es.index(index="f1", body=data, request_timeout=30)

        elif int(header.packetId) == 6:
            packet = PacketCarTelemetryData_V1.from_buffer_copy(data[0:1307])
            data = {
                "session_ts": header.sessionTime,
                "@timestamp": datetime.utcnow().isoformat(),
                "packet_id": header.packetId,
                "session_UUID": str(header.sessionUID),
                "session_time": header.sessionTime,
                "frame_id": header.frameIdentifier,
                "player_index": header.playerCarIndex,
                "speed": packet.carTelemetryData[header.playerCarIndex].speed,
                "throttle": packet.carTelemetryData[header.playerCarIndex].throttle,
                "steering": packet.carTelemetryData[header.playerCarIndex].steer,
                "brake": packet.carTelemetryData[header.playerCarIndex].brake,
                "clutch": packet.carTelemetryData[header.playerCarIndex].clutch,
                "gear": packet.carTelemetryData[header.playerCarIndex].gear,
                "engine_RPM": packet.carTelemetryData[header.playerCarIndex].engineRPM,
                "DRS_enabled": packet.carTelemetryData[header.playerCarIndex].drs,
                "dev_lights": packet.carTelemetryData[header.playerCarIndex].revLightsPercent,
                "FL_brake_T": packet.carTelemetryData[header.playerCarIndex].brakesTemperature[0],
                "FR_brake_T": packet.carTelemetryData[header.playerCarIndex].brakesTemperature[1],
                "RL_brake_T": packet.carTelemetryData[header.playerCarIndex].brakesTemperature[2],
                "RR_brake_T": packet.carTelemetryData[header.playerCarIndex].brakesTemperature[3],
                "FL_tyre_surface_T": packet.carTelemetryData[header.playerCarIndex].tyresSurfaceTemperature[0],
                "FR_tyre_surface_T": packet.carTelemetryData[header.playerCarIndex].tyresSurfaceTemperature[1],
                "RL_tyre_surface_T": packet.carTelemetryData[header.playerCarIndex].tyresSurfaceTemperature[2],
                "RR_tyre_surface_T": packet.carTelemetryData[header.playerCarIndex].tyresSurfaceTemperature[3],
                "FL_tyre_inner_T": packet.carTelemetryData[header.playerCarIndex].tyresInnerTemperature[0],
                "FR_tyre_inner_T": packet.carTelemetryData[header.playerCarIndex].tyresInnerTemperature[1],
                "RL_tyre_inner_T": packet.carTelemetryData[header.playerCarIndex].tyresInnerTemperature[2],
                "RR_tyre_inner_T": packet.carTelemetryData[header.playerCarIndex].tyresInnerTemperature[3],
                "engine_T": packet.carTelemetryData[header.playerCarIndex].engineTemperature,
                "FL_tyre_pressure": packet.carTelemetryData[header.playerCarIndex].tyresPressure[0],
                "FR_tyre_pressure": packet.carTelemetryData[header.playerCarIndex].tyresPressure[1],
                "RL_tyre_pressure": packet.carTelemetryData[header.playerCarIndex].tyresPressure[2],
                "RR_tyre_pressure": packet.carTelemetryData[header.playerCarIndex].tyresPressure[3],
                "FL_diving_surface": packet.carTelemetryData[header.playerCarIndex].surfaceType[0],
                "FR_tyre_surface": packet.carTelemetryData[header.playerCarIndex].surfaceType[1],
                "RL_tyre_surface": packet.carTelemetryData[header.playerCarIndex].surfaceType[2],
                "RR_tyre_surface": packet.carTelemetryData[header.playerCarIndex].surfaceType[3]
            }
            es.index(index="f1", body=data, request_timeout=30)

        elif int(header.packetId) == 8:
            packet = PacketFinalClassificationData_V1.from_buffer_copy(data[0:839])
            data = {
                "session_ts": header.sessionTime,
                "@timestamp": datetime.utcnow().isoformat(),
                "packet_id": header.packetId,
                "session_UUID": str(header.sessionUID),
                "session_time": header.sessionTime,
                "frame_id": header.frameIdentifier,
                "player_index": header.playerCarIndex,
                "position": packet.classificationData[header.playerCarIndex].position,
                "num_laps": packet.classificationData[header.playerCarIndex].numLaps,
                "grid_position": packet.classificationData[header.playerCarIndex].gridPosition,
                "points": packet.classificationData[header.playerCarIndex].points,
                "num_pit_stops": packet.classificationData[header.playerCarIndex].numPitStops,
                "result_status": packet.classificationData[header.playerCarIndex].resultStatus,
                "best_lap_time": packet.classificationData[header.playerCarIndex].bestLapTime,
                "total_race_time": packet.classificationData[header.playerCarIndex].totalRaceTime,
                "penalties_time": packet.classificationData[header.playerCarIndex].penaltiesTime,
                "num_penalties": packet.classificationData[header.playerCarIndex].numPenalties,
                "num_tyre_stints": packet.classificationData[header.playerCarIndex].numTyreStints,
                "tyre_stints_actual": packet.classificationData[header.playerCarIndex].tyreStintsActual,
                "tyre_stints_visual": packet.classificationData[header.playerCarIndex].tyreStintsVisual,
            }
            es.index(index="f1", body=data, request_timeout=30)


if __name__ == "__main__":
    # logging
    logging.basicConfig(level=logging.INFO)
    logging.info("Server started on 20777")

    # Server loop
    loop = asyncio.get_event_loop()
    t = loop.create_datagram_endpoint(F1UdpReceiver, local_addr=('0.0.0.0', 20777))
    loop.run_until_complete(t)
    loop.run_forever()

