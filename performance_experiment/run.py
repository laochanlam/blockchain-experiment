from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.util import dumpNodeConnections

class Startopo( Topo ):
	def __init__( self, **opts ):
            Topo.__init__(self, **opts)
            hosts = []
            s0 = self.addSwitch('S0')
            for counter in range(1, 10):
                counter = str(counter)
                hostname = 'h' + counter
                ip_ = '10.0.0.' + counter
                mac_ ='00:00:00:00:00:0' + counter
                host = self.addHost(hostname, ip=ip_, mac=mac_)
                self.addLink(hostname, s0)
                hosts.append(host)
                

if __name__ == '__main__':
    topo = Startopo()
    net = Mininet(topo, controller=None)
    net.start()
    # erase file context
    open('info.log', 'w').close()
    print('Start star topology...\n###################################')
    # cli = CLI(net, script='cli_script.sh')
    dumpNodeConnections(net.hosts)
    print('###################################')
    # cli = CLI(net)
    h1 = net.get('h1')
    result = h1.cmd('python3 ../client/receiver_origin.py god')
    print(result)
    net.stop()