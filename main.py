from f1_telemetry.server import get_telemetry
from f1_telemetry.telemetry_saver import csv_saver, getlist


def catch_and_save():
    motion = open('motion.csv', 'a')
    session = open('session.csv', 'a')
    lap_data = open('lap_data.csv', 'a')
    event = open('event.csv', 'a')
    participants = open('participants.csv', 'a')
    setup = open('setup.csv', 'a')
    telemetry = open('telemetry.csv', 'a')
    status = open('status.csv', 'a')

    files_dict = {
                    0 : motion,
                    1 : session,
                    2 : lap_data,
                    3 : event,
                    4 : participants,
                    5 : setup,
                    6 : telemetry,
                    7 : status,
                    }

    for packet_id, packet in get_telemetry():
        packet_lst = getlist(packet)
        csv_saver(files_dict[packet_id], packet_lst)

    for file_ in files_dict.values():
        file_.close()


if __name__ == '__main__':
    catch_and_save()
