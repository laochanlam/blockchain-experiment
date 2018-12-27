from mininet.topo import Topo

class Startopo( Topo ):
	def build( self ):
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
                
topos = {'startopo': ( lambda: Startopo() ) }
