import time
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.log import setLogLevel, info

def collect_data(net):
    with open("network_data.csv", "w") as f:
        f.write("time,source,destination,bandwidth,latency,packet_loss\n")
        for i in range(3 * 60):  # جمع البيانات كل دقيقة لمدة 3 ساعات
            for src in net.hosts:
                for dst in net.hosts:
                    if src != dst:
                        result = net.ping([src, dst], timeout=1)
                        # هنا يمكنك إضافة عمليات قياس عرض النطاق الترددي وفقدان الحزم
                        bandwidth = net.iperf([src, dst], seconds=5)
                        latency = result[0]
                        packet_loss = result[1]
                        f.write(f"{time.time()},{src},{dst},{bandwidth},{latency},{packet_loss}\n")
            time.sleep(60)

def setup_network():
    net = Mininet(controller=RemoteController, link=TCLink)
    c0 = net.addController(name='c0', controller=RemoteController, ip='127.0.0.1', port=6633)
    # إضافة المفاتيح والعقد (hosts) حسب الطوبولوجيا OS3E
    # net.addSwitch() and net.addHost() commands here

    net.build()
    net.start()
    collect_data(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    setup_network()
