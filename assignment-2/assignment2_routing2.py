#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, OVSSwitch, DefaultController
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

class CustomTopo(Topo):

    def build(self, **_opts):

        info("\n Creating Topology \n")
        #  Adding 4 routers
        info("\n Creating routers\n")
        # we are using the routing facility provided by linux.
        r1 = self.addNode("r1", cls=LinuxRouter, ip="10.0.1.1/24")
        r2 = self.addNode("r2", cls=LinuxRouter, ip="10.0.2.1/24")
        r3 = self.addNode("r3", cls=LinuxRouter, ip="10.0.3.1/24")
        r4 = self.addNode("r4", cls=LinuxRouter, ip="10.0.4.1/24")
        

        #router-r1 connections
        
        s1 = self.addSwitch("s1")
        self.addLink(s1, r1, intfName2="r1-eth0", params2={"ip": "10.0.1.1/24"})
        h12 = self.addHost(name="h12", ip="10.0.1.2/24", defaultRoute="via 10.0.1.1")
        h13 = self.addHost(name="h13", ip="10.0.1.3/24", defaultRoute="via 10.0.1.1")
        self.addLink(s1, h12)
        self.addLink(s1, h13)

        # router-r2 connections
        
        h22 = self.addHost(name="h22", ip="10.0.2.2/24", defaultRoute="via 10.0.2.1")
        self.addLink(h22, r2, intfName2="r2-eth0", params2={"ip": "10.0.2.1/24"})

        #router-r3 connections
        
        h32 = self.addHost(name="h32", ip="10.0.3.2/24", defaultRoute="via 10.0.3.1")
        self.addLink(h32, r3, intfName2="r3-eth0", params2={"ip": "10.0.3.1/24"})

        #router-r4 connections
       
        s2 = self.addSwitch("s2")
        self.addLink(s2, r4, intfName2="r4-eth0", params2={"ip": "10.0.4.1/24"})
        h42 = self.addHost(name="h42", ip="10.0.4.2/24", defaultRoute="via 10.0.4.1")
        h43 = self.addHost(name="h43", ip="10.0.4.3/24", defaultRoute="via 10.0.4.1")
        self.addLink(s2, h42)
        self.addLink(s2, h43)
        
        #Connections b/w routers

        self.addLink(
            r2,
            r4,
            intfName1="r2-eth1",
            intfName2="r4-eth1",
            params1={"ip": "192.168.2.1/24"},
            params2={"ip": "192.168.2.3/24"},
        )

        self.addLink(
            r1,
            r2,
            intfName1="r1-eth2",
            intfName2="r2-eth2",
            params1={"ip": "192.168.1.1/24"},
            params2={"ip": "192.168.1.3/24"},
        )

        self.addLink(
            r1,
            r3,
            intfName1="r1-eth1",
            intfName2="r3-eth1",
            params1={"ip": "192.168.0.1/24"},
            params2={"ip": "192.168.0.3/24"},
        )
        
        

def setup():
    topo = CustomTopo()
    net = Mininet(topo=topo)

    # connectivity before adding routing rules
    #net.pingAll()

    net["r1"].cmd("ip route add 10.0.2.0/24 via 192.168.1.3")       # r1->r2
    net["r1"].cmd("ip route add 10.0.3.0/24 via 192.168.0.3")       # r1->r3
    net["r1"].cmd("ip route add 10.0.4.0/24 via 192.168.1.3")       # r1->r4

    net["r2"].cmd("ip route add 10.0.1.0/24 via 192.168.1.1")       # r2->r1 
    net["r2"].cmd("ip route add 10.0.3.0/24 via 192.168.1.1")       # r2->r3 
    net["r2"].cmd("ip route add 10.0.4.0/24 via 192.168.2.3")       # r2->r4

    # from r3 for all other networks next-hop is r1
    net["r3"].cmd("ip route add 10.0.1.0/24 via 192.168.0.1")       # r3->r1 
    net["r3"].cmd("ip route add 10.0.2.0/24 via 192.168.0.1")       # r3->r2
    net["r3"].cmd("ip route add 10.0.4.0/24 via 192.168.0.1")       # r3->r4 

    # from r4 for all other networks next-hop is r2
    net["r4"].cmd("ip route add 10.0.1.0/24 via 192.168.2.1")        # r4->r2
    net["r4"].cmd("ip route add 10.0.2.0/24 via 192.168.2.1")        # r4->r2
    net["r4"].cmd("ip route add 10.0.3.0/24 via 192.168.2.1")        # r4->r2

    
    net.start()
    # connectivity after adding routing rules
    net.pingAll()

    info("\n NOW DISABLING TRAFFIC FLOW BETWEEN GIVEN HOSTS \n")

    # Appending new rule to drop traffic going ftom h12 to h22. We can add this rule either at r1 or r2. But adding at r2 is convenience as if r2
    #receives traffic related to h12 can be dropped.

    net["r2"].cmd("iptables -A FORWARD -s 10.0.1.2 -d 10.0.2.2 -j REJECT")  # -s --> source and -d --> destination, -j if matched then REJECT it.

    net.pingAll()

    CLI(net)
    

if __name__ =='__main__':
    setLogLevel('info')
    setup()


