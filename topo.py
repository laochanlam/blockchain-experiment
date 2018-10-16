from mininet.topo import Topo



class CustomTopo( Topo ):

	def build( self ):
                hosts = []
                for counter in range(0, 10):
                    counter = str(counter)
                    hostname = 'h' + counter
                    ip_ = '10.0.0.' + counter
                    mac_ ='00:00:00:00:00:0' + counter
                    host = self.addHost(hostname, ip=ip_, mac=mac_)                 
                    hosts.append(host)
                    
                
                for i in range(0, len(hosts)):
                    for j in range(i+1, len(hosts)):
                        self.addLink(hosts[i], hosts[j])

               #h1 = self.addHost("h1", ip='10.0.0.2', mac='00:00:00:00:02:00')
		#self.addLink(h1, h0)
                #print(hosts)

topos = {'mytopo': ( lambda: CustomTopo() ) }
