from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.util import dumpNodeConnections
from mininet.node import UserSwitch
import threading
import time

# def run_origin_receiver(host):
#     print(host.cmd('ip route'))
#     host.cmd('python3 ../client/receiver_origin.py god &')

def run_receiver(host):
    print(host.name + ' started to work')
    print(host.cmd('ip route'))
    result = host.cmd('python3 ../client/receiver.py ' + host.name)
    print(result)

class Startopo( Topo ):
	def __init__( self ):
            Topo.__init__( self )
            # hosts = []
            # switches = []
            h1 = self.addHost('h1')
            h2 = self.addHost('h2')
            s0 = self.addSwitch('s1')
            self.addLink(h1, s0)
            self.addLink(h2, s0)
            # switches.append(s0)
            # for counter in range(1, 10):
            #     counter = str(counter)
            #     hostname = 'h' + counter
            #     ip_ = '10.0.0.' + counter
            #     mac_ ='00:00:00:00:00:0' + counter
            #     host = self.addHost(hostname, ip=ip_, mac=mac_)
            #     self.addLink(hostname, s0)
            #     hosts.append(host)
            # self.addLink(hosts[0], hosts[1 ])
                

if __name__ == '__main__':
    topo = Startopo()
    net = Mininet(topo=topo, controller=None)
    net.start()
    
    # erase file context
    # open('info.log', 'w').close()
    print('Start star topology...\n###################################')
    # cli = CLI(net, script='cli_script.sh')
    dumpNodeConnections(net.hosts)
    print('###################################')
    # cli = CLI(net)
    # h1 = net.get('h1')
    # h2 = net.get('h2')
    # h3 = net.get('h3')
    # h4 = net.get('h4')
    # origin_receiver
    # t1 = threading.Thread(target=run_origin_receiver, args=(h1,))

    # receiver
    # t3 = threading.Thread(target=run_receiver, args=(h3,))
    # t4 = threading.Thread(target=run_receiver, args=(h4,))
    # t1.start()
    # net.hosts[0].cmd('python3 ../client/receiver_origin.py god &')

    # CLI(net)
    net.pingAll()

    # print('wait until origin_receiver generate 5 blocks....')
    # # wait until origin_receiver generate 5 blocks.
    # while ( sum(1 for line in open('info.log')) < 2):
    #     print(sum(1 for line in open('info.log')))
    #     time.sleep(1)
    
    # print('Origin receiver already generated 5 blocks, start to work')
    # t2 = threading.Thread(target=run_receiver, args=(h2,))
    # t2.start()
    # cli = CLI(net)
    # result = h2.cmd('python3 ../client/receiver.py h2')
    # print(result)
    # t2.start()
    # t3.start()
    # t4.start()
    # time.sleep(100000)
    # print(result)
    net.stop()