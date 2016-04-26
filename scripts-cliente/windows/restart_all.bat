net stop openvpnservice
timeout 4
net start openvpnservice
timeout 30
taskkill /F /IM vboxheadless.exe
timeout 4
cd "%programfiles%\oracle\virtualbox"
vboxmanage startvm node --type headless

