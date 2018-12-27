# Installation
```
$ sudo apt-get install mininet
```

# How to run
```
$ sh run.sh
```

# Useful commands
```
$ xterm h1
```
Open terminal of h1.
```
$ h1 ifconfig
```
Execute `ifconfig` on h1.

# Structure
### topo.py
- Star topology with 9 hosts.
- Host's IP from 10.0.0.1 to 10.0.0.9.
### run.sh
- mininet running script.