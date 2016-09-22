# Gridlan
Gridlan project

These instructions for building a Gridlan are under construction.

The Gridlan components are:

* The server. Will be responsible for the DHCP server, tftp server, NFS server, VPN server, the resource manager system and the monitoring systems (ganglia). 
* The Gridlan client. The connected computers are the Gridlan clients. The client main functions are to connect to the Gridlan VPN, start the virtual machine (which is the Gridlan node) and check periodically if the VM is up and running.
* The Gridlan node is the virtual machine which is started in each Gridlan client. It boots a Debian GNU/Linux via PXE and mount the '/' via nfsroot. The computing environment is in the virtual machine.

Instructions for setting the server for diskless nodes are in:

http://www.kerrighed.org/wiki/index.php/Kerrighed_on_NFSROOT
