#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, OVSSwitch, RemoteController, DefaultController
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink

class CustomTopo(Topo):

    def build(self, **_opts):

        info("\n Creating Topology \n")
        info("\n Creating routers\n")

       
        r1 = self.addSwitch("r1", protocol="OpenFlow13")
        r2 = self.addSwitch("r2", protocol="OpenFlow13")
        r3 = self.addSwitch("r3", protocol="OpenFlow13")
        r4 = self.addSwitch("r4", protocol="OpenFlow13")

        #r1 connections
        
        s1 = self.addSwitch("s1", protocol="OpenFlow13")
        self.addLink(s1, r1, intfName2="r1-eth0")
        h12 = self.addHost(name="h12", ip="10.0.1.2/24")
        h13 = self.addHost(name="h13", ip="10.0.1.3/24")
        self.addLink(s1, h12)
        self.addLink(s1, h13)

        # r2 connections
        
        h22 = self.addHost(name="h22", ip="10.0.2.2/24")
        self.addLink(h22, r2, intfName2="r2-eth0")

        #r3 connections
        
        h32 = self.addHost(name="h32", ip="10.0.3.2/24")
        self.addLink(h32, r3, intfName2="r3-eth0")

        #r4 connections
       
        s2 = self.addSwitch("s2", protocol="OpenFlow13")
        self.addLink(s2, r4, intfName2="r4-eth0")
        h42 = self.addHost(name="h42", ip="10.0.4.2/24")
        h43 = self.addHost(name="h43", ip="10.0.4.3/24")
        self.addLink(s2, h42)
        self.addLink(s2, h43)
        
        #Connections b/w SDN devices

        self.addLink(
            r2,
            r4,
            intfName1="r2-eth1",
            intfName2="r4-eth1",
        )

        self.addLink(
            r1,
            r2,
            intfName1="r1-eth2",
            intfName2="r2-eth2",
        )

        self.addLink(
            r1,
            r3,
            intfName1="r1-eth1",
            intfName2="r3-eth1",
        )
        
        

def setup():
    topo = CustomTopo()
    net = Mininet(
        topo=topo,
        controller=DefaultController,
    #    controller=lambda name: RemoteController(
    #       name,
    #        ip="172.16.128.190"
    #        ),
        switch=OVSSwitch,
        autoSetMacs=True,
        autoStaticArp=True,
        waitConnected=True,
       link=TCLink,
        )

    
    net.start()
   
    for host in net.hosts:
        interface = host.defaultIntf()
        host.setDefaultRoute(interface)
    #net.pingAll()
    CLI(net)
    

if __name__ =='__main__':
    setLogLevel('info')
    setup()


