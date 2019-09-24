from scapy.all import *
global src_ip, dst_ip
src_ip = "192.168.1.145"
dst_ip = "192.168.1.108"
infile = "f12019-test.pcap"


def my_send(rd, count=40000):
    pkt_cnt = 0
    p_out = []

    for p in rd:
        pkt_cnt += 1
        np = p.payload
        np[IP].dst = dst_ip
        np[IP].src = src_ip
        del np[IP].chksum
        p_out.append(np)
        if pkt_cnt % count == 0:
            send(PacketList(p_out))
            p_out = []

    # Send remaining in final batch
    send(PacketList(p_out))
    print "Total packets sent %d" % pkt_cn

try:
    my_reader = PcapReader(infile)
    my_send(my_reader)
except IOError:
    print "Failed reading file %s contents" % infile
    sys.exit(1)

