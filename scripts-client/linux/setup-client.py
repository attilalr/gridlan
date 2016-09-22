#!/usr/bin/python

# uso:
# python setup-cliente.py

import sys
from instalation import instalation

# must change!
IPSERVIDOR="127.0.0.1"
CONTATOEMAIL="admin@server"

gridlocal=instalation()

while (1):

  gridlocal.showmenu() # OPCAO DE SAIDA EH TRATADA AQUI
  procedimento = gridlocal.path

  gridlocal.checkuser() # CHECAGEM DE USUARIO PARA A INSTALACAO
  gridlocal.checkvm() # CHECAGEM SE O PC PODE RODAR UMA VM, PARA A INSTALACAO

  if (gridlocal.path=='1'):
    gridlocal.getmacaddr()
    gridlocal.customizarxml()
    gridlocal.customizarvpn()
    gridlocal.msgfinal(IPSERVIDOR,CONTATOEMAIL,gridlocal.host,gridlocal.macaddr)
    gridlocal.configurado='1'

  # NESTA ETAPA DEVEM SER TRADATAS DISTROS DIFERENTES
  if (gridlocal.path=='2'):
    gridlocal.checkmodules() # verificar se o sistema tem tun e kvm
    gridlocal.instalarpacotes()
    gridlocal.instalarscriptservico() # em /etc/init.d e nos rc's
    gridlocal.criarpastainstalacao() # /opt/gridlocal/keys
    gridlocal.instalarconfvpn() # em /opt/gridlocal
# currently the local disks arent used
#    gridlocal.instaladiscovm() # em /var/lib/libvirt/images
    gridlocal.instalarxml() # em /opt/gridlocal






