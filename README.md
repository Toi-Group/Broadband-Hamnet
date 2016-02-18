# Broadband-Hamnet Chat Software
v0.4

This is a Temple EE Senior Project 2016. 
Official Project Website: https://sites.google.com/a/temple.edu/broadband-mcomm/

## Requires 
- [Google Protocol Buffers 3][] 
- Root privileges on your for utilizing raw sockets. ICMP messages are
implemented in python. 
- Python 3. Tested compatibility with [Anaconda Python 3.5][]
- Note this project contains a submodule to a Github Project [python-ping][]. 
After cloning this project you have to init and download the submodule. 
Follow the instructions below:
``` shell
$ git submodule init
$ git submodule update
```

[Anaconda Python 3.5]: https://www.continuum.io/downloads
[Google Protocol Buffers 3]: https://developers.google.com/protocol-buffers/
[python-ping]: https://github.com/l4m3rx/python-ping/