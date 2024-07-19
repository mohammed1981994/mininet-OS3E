from mininet.net import Mininet
from mininet.node import RemoteController, Controller, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time
import json
import geo
import networkx as nx

def OS3EGraph():
    g = nx.Graph()
    paths = [
        ["Vancouver", "Seattle"],
        ["Seattle", "Missoula", "Minneapolis", "Chicago"],
        ["Seattle", "SaltLakeCity"],
        ["Seattle", "Portland", "Sunnyvale"],
        ["Sunnyvale", "SaltLakeCity"],
        ["Sunnyvale", "LosAngeles"],
        ["LosAngeles", "SaltLakeCity"],
        ["LosAngeles", "Tucson", "ElPaso"],
        ["SaltLakeCity", "Denver"],
        ["Denver", "Albuquerque", "ElPaso"],
        ["Denver", "KansasCity", "Chicago"],
        ["KansasCity", "Dallas", "Houston"],
        ["ElPaso", "Houston"],
        ["Houston", "Jackson", "Memphis", "Nashville"],
        ["Houston", "BatonRouge", "Jacksonville"],
        ["Chicago", "Indianapolis", "Louisville", "Nashville"],
        ["Nashville", "Atlanta"],
        ["Atlanta", "Jacksonville"],
        ["Jacksonville", "Miami"],
        ["Chicago", "Cleveland"],
        ["Cleveland", "Buffalo", "Boston", "NewYork", "Philadelphia", "Washington"],
        ["Cleveland", "Pittsburgh", "Ashburn", "Washington"],
        ["Washington", "Raleigh", "Atlanta"]
    ]
    
    for path in paths:
        for i in range(len(path) - 1):
            g.add_edge(path[i], path[i+1])
    
    return g

def collect_data(net):
    with open("network_data.csv", "w") as f:
        f.write("time,source,destination,bandwidth,latency,packet_loss\n")
        end_time = time.time() + 3 * 3600  # 3 ساعات من الآن
        while time.time() < end_time:
            for src in net.hosts:
                for dst in net.hosts:
                    if src != dst:
                        latency = net.ping([src, dst], timeout=1)
                        src.cmd('iperf -s &')
                        bandwidth = dst.cmd('iperf -c %s -t 5' % src.IP())
                        src.cmd('kill %iperf')
                        packet_loss = 0  # افتراض عدم فقدان الحزم
                        f.write(f"{time.time()},{src.IP()},{dst.IP()},{bandwidth.strip()},{latency},{packet_loss}\n")
            time.sleep(60)  # الانتظار لمدة دقيقة قبل إعادة القياس

def setup_network():
    topo = OS3EGraph()
    net = Mininet(controller=Controller, link=TCLink, switch=OVSSwitch)
    c0 = net.addController(name='c0')
    
    switches = {}
    for i, node in enumerate(topo.nodes, 1):
        switches[node] = net.addSwitch(f's{i}', dpid=f'{i:016x}')
    
    for src, dst in topo.edges:
        net.addLink(switches[src], switches[dst])
    
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
