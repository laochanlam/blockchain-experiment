from mininet.topo import Topo



class CustomTopo( Topo ):

	def build( self ):
                    host1 = self.addHost('h0')
                    host2 = self.addHost('h1')
                    host3 = self.addHost('h2')                
                    self.addLink(host1, host3)
                    self.addLink(host1, host2)

               #h1 = self.addHost("h1", ip='10.0.0.2', mac='00:00:00:00:02:00')
		#self.addLink(h1, h0)
                #print(hosts)
topos = {'mytopo': ( lambda: CustomTopo() ) }
