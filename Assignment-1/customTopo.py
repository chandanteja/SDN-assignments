from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.node import Controller, OVSSwitch, RemoteController
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.cli import CLI


class MyTopo(Topo):
    def __init__(self, numHosts = 11, numSwitches = 4, bw = (0,5), delay=(2,30)):
        Topo.__init__(self)

        self.allHosts = []      #list of all hosts
        self.allSwitches = []   #lisyt of all switches
        
        # creating of hosts
        for i in range(1,numHosts+1):
            self.allHosts.append(self.addHost('h%s' % i, ip = "10.0.0.{}/24".format(i))) #h%s means append string represented by %s to 'h'.
        
        #creation of switches
        for i in range(1, numSwitches+1):
            self.allSwitches.append(self.addSwitch('s%s' % i, protocols = "OpenFlow13"))

        self.HostsToSwitch = [0 for i in range(len(self.allSwitches))]      # this keeps track of hosts connected to a particular switch

        index = 0

        for i in range(len(allHosts)):
            if(self.HostsToSwitch[index] >= math.ceil(len(self.allHosts)/len(self.allSwitches))):
                index+=1
            print("Connected host-{} to switch-{}".format(i,index))
            self.addLink(self.allHosts[i],self.allSwitches[index], 
                        bw = random.uniform(bw[0],bw[1]),    
                        delay = "{}ms".format(random.uniform(delay[0], delay[1])) )
            self.HostsToSwitch[index] += 1


        for i in range(len(self.allSwitches)-1):
            last = len(self.allSwitches)-i;
            print("Connected Switch{}, Switch{}".format(i,last))
            self.addLink(self.allSwitches[i],self.allSwitches[last], 
                        bw = random.uniform(bw[0],bw[1]),    
                        delay = "{}ms".format(random.uniform(delay[0], delay[1])) )




        
def Experiment():
    topo = MyTopology()
    #net = Mininet(topo = MyTopology,controller = RemoteController(name = "ODL controller", ip = "172.16.128.140"), switch = OVSSwitch, link = TCLink)
    net = Mininet(
        topo=topo,  
        controller=lambda name: RemoteController(
            name,
            ip="172.16.128.220"
        ),  
        switch=OVSSwitch,
        link=TCLink,
    )

    net.start()
    CLI(net)
    # dumpNodeConnections(net.allHosts)
    # net.pingall()
    # net.stop()
if __name__ =='__main__':
    setLogLevel('info')
    Experiment()