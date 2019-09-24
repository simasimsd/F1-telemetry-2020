# F1-telemetry-2019

reimplementation of https://github.com/simasimsd/F1-telemetry-2018 for F1 2019 Game

https://forums.codemasters.com/topic/38920-f1-2019-udp-specification/

Work in progress

## How to test F1 telemetry
If you want to test it without running the game, you can replay a previously
recorded session captured with wireshark or tcpdump and use send-pcap.py to send
the UDP packets.

A sample file can be found here:
http://nx.fastnetserv.cloud/index.php/s/B5dtZ4W9zZRLK6r

### Usage
Configure the following parameters inside send-pcap.py
```
  src_ip = ""
  dst_ip = ""
  infile = "f12019-test.pcap"
```

After that run it with "python send-pcap.py"
