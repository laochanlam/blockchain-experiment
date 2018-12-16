#!/usr/bin/python
 
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
 
class SingleSwitchTopo(Topo):
def __init__(self, n=2, **opts):
Topo.__init__(self, **opts)
switch = self.addSwitch('s1')     #添加一个交换机在拓扑中
for h in range(n):
host = self.addHost('h%s' % (h + 1))   #添加主机到拓扑中
self.addLink(host, switch)   #添加双向连接拓扑
 
def simpleTest():
topo = SingleSwitchTopo(n=4)
net = Mininet(topo)    #主要类来创建和管理网络
net.start()    #启动您的拓扑网络
print "Dumping host connections"
dumpNodeConnections(net.hosts)       #转存文件连接
print "Testing network connectivity"     
net.pingAll()    #所有节点彼此测试互连
net.stop()       #停止您的网络
 
if __name__ == '__main__':
setLogLevel('info')  # 设置 Mininet 默认输出级别，设置 info 它将提供一些有用的信息
simpleTest()
