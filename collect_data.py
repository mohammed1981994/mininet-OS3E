from mininet.net import Mininet
from mininet.node import RemoteController, Controller
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from Topology import OS3ETopo

def collect_data(net):
    with open("network_data.csv", "w") as f:
        f.write("time,source,destination,bandwidth,latency,packet_loss\n")
        for i in range(3 * 60):  # جمع البيانات كل دقيقة لمدة 3 ساعات
            for src in net.hosts:
                for dst in net.hosts:
                    if src != dst:
                        result = net.ping([src, dst], timeout=1)
                        bandwidth = net.iperf([src, dst], seconds=5)
                        latency = result[0]
                        packet_loss = result[1]
                        f.write(f"{time.time()},{src},{dst},{bandwidth},{latency},{packet_loss}\n")
            time.sleep(60)

def setup_network():
    net = Mininet(topo=OS3ETopo(), controller=Controller, link=TCLink)
    c0 = net.addController(name='c0')

    net.build()
    c0.start()
    for switch in net.switches:
        switch.start([c0])

    collect_data(net)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    setup_network()
