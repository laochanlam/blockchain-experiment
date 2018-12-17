from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.util import dumpNodeConnections
from mininet.node import OVSController
import threading
import time

def run_origin_receiver(host):
    host.cmd('python3 ../client/receiver_origin.py god')

def run_receiver(host):
    print(host.name + ' started to work')
    host.cmd('python3 ../client/receiver.py ' + host.name)

class Startopo( Topo ):
	def __init__( self, **opts ):
            Topo.__init__(self, **opts)
            hosts = []
            switches = []
            s0 = self.addSwitch('S0')
            switches.append(s0)
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
    net = Mininet(topo, controller=OVSController)
    net.start()
    
    # erase file context
    open('info.log', 'w').close()
    print('Start star topology...\n###################################')
    # cli = CLI(net, script='cli_script.sh')
    dumpNodeConnections(net.hosts)
    print('###################################')
    # cli = CLI(net)
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')
    # origin_receiver
    t1 = threading.Thread(target=run_origin_receiver, args=(h1,))
    t1.daemon = True
    # receiver
    t2 = threading.Thread(target=run_receiver, args=(h2,))
    t3 = threading.Thread(target=run_receiver, args=(h3,))
    t4 = threading.Thread(target=run_receiver, args=(h4,))
    t1.start()

    print('wait until origin_receiver generate 1 blocks....')
    # wait until origin_receiver generate 1 blocks.
    while ( sum(1 for line in open('info.log')) < 2):
        # print(sum(1 for line in open('info.log')))
        time.sleep(1)
    
    print('Origin receiver already generated 1 blocks, start to work')

    t2.start()
    t3.start()
    t4.start()
    
    time.sleep(100000)  
    net.stop()