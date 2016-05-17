taskkill /F /IM vboxheadless.exe
timeout 4
net stop openvpnservice
timeout 4
netsh interface set interface name="Gridlan Bridge" admin=disable
timeout 8
netsh interface set interface name="Gridlan Bridge" admin=enable
timeout 8
net start openvpnservice
timeout 8
cd "%programfiles%\oracle\virtualbox"
vboxmanage dhcpserver remove --ifname "VirtualBox Host-Only Ethernet Adapter"
vboxmanage startvm node --type headless

