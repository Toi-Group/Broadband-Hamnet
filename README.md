# Broadband-Hamnet Chat Software
v0.4alpha

This is a Temple EE Senior Project 2016. 

Official Project Website: https://sites.google.com/a/temple.edu/broadband-mcomm/

## Requires 
- Root privileges on your PI for utilizing raw sockets. ICMP messages are
implemented directly in Python. 
- Router scripts [router_request_arpinfo.sh][], and [router_tx_arpinfo.sh][] 
need to be preloaded onto your router. 
- Python 3.2 or Greater.
- [Google Protocol Buffers 3][]
- Requires [`sshpass`][] for recurring `ssh` communications with 
Broadband-Hamnet router. 

## Installation Instructions
To install run the following commands:
``` shell
$ git clone https://github.com/Toi-Group/ToiChat.git
$ cd ToiChat
$ sudo python3 setup.py install
```

To run the program in via a CLI:
``` shell
# Assuming you are in the root ToiChat directory
#
$ cd src/pi_scripts
$ sudo python3 toiChatShell.py
```

## Acknowledgments
- Note this project contains a reference to Github Project:
[python-ping][] which is distributed under the GNU General Public License 
(GPL) License. 


[`sshpass`]: http://linux.die.net/man/1/sshpass
[Google Protocol Buffers 3]: https://developers.google.com/protocol-buffers/
[python-ping]: https://github.com/l4m3rx/python-ping/
[router_request_arpinfo.sh]: https://github.com/Toi-Group/ToiChat/blob/master/src/router-scripts/router_request_arpinfo.sh
[router_tx_arpinfo.sh]: https://github.com/Toi-Group/ToiChat/blob/master/src/router-scripts/router_tx_arpinfo.sh