# How to Run
```
mininet> xterm h1 h2 h3 h4
```

分别开启h1, h2, h3, h4的终端机 作为进行PBFT共识的4个矿机，这里令f=1
```
h1> python3 ../client/receiver.py God
```
```
h2> python3 ../client/receiver.py user1
```
```
h3> python3 ../client/receiver.py user2
```
```
h4> python3 ../client/receiver.py user3 
```
因为是PBFT共识，所以应该一次性(第一个区块产生之前）运行上面4个脚本

在h5执行发送交易的脚本，在程序中输入收款人及金额后，检查sender金钥及本地钱包剩额合法后把交易广播到区块链网络中并等待确认。
```
h5> python3 ../client/sender.py God
```
          