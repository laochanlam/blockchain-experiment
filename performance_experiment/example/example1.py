#!/usr/bin/python
 
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController

class SingleSwitchTopo(Topo):
    def __init__(self, n=2, **opts):
        Topo.__init__(self, **opts)
        switch = self.addSwitch('s1')
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch)  
 
def simpleTest():
    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo, controller=OVSController) 
    net.start() 
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"     
    net.pingAll()
    net.stop()
 
if __name__ == '__main__':
    setLogLevel('info') 
    simpleTest()
