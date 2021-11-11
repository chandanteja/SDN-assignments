#!/usr/bin/python3
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, OVSSwitch, DefaultController, RemoteController
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class MyTopology(Topo):
    def build(self, **_opts):
        #Adding Switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        #Adding Hosts
        h1 = self.addHost('h1', ip = "10.0.1.1/24")
        h2 = self.addHost('h2', ip = "10.0.2.1/24")

        application = self.addHost('application', ip = "10.0.3.1/24")

        h3 = self.addHost('h3', ip = "10.0.5.1/24")
        h5 = self.addHost('h5', ip = "10.0.6.1/24")

        #Links between switches
        self.addLink(s1,s3)
        self.addLink(s2,s3)
        #Link between switch1

        self.addLink(s3,h1)
        self.addLink(s3,h2)

        self.addLink(s1,appn)
        self.addLink(s2,appn)

        self.addLink(s1,h3)
#        self.addLink(s1,h4)

        self.addLink(s2,h5)
#        self.addLink(s2,h6)

            
def Experiment():
    topo = MyTopology()
    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController(
            name,
            ip="172.16.128.190"
        ),
        switch = OVSSwitch,
        autoSetMacs = True,
        autoStaticArp =True,
        waitConnected = True,
        )
    net.start()
    for h in net.hosts:
        iface = h.defaultIntf()
        h.setDefaultRoute(iface)
    
    CLI(net)
    
if __name__ =='__main__':
    setLogLevel('info')
    Experiment()


