#!/usr/bin/python

# script para adicionar um noh ao cluster
# modificacoes no dhcp, /etc/hosts e criacao de chaves vpn

# uso:
# python add-node.py hostname macaddress

import sys, os, subprocess

print """

 Script para adicao de noh ao sistema do servidor:

 * Inclusao no dhcp (ip automatico)
 * Inclusao no /etc/hosts /nfsroot/etc/hosts
 * Criacao das chaves vpn

"""

if (len(sys.argv)!=3):
  print 
  print " Uso do script: python addnode.py hostname macaddress"
  print
  sys.exit(0)
  
hostname = sys.argv[1]
macaddr = sys.argv[2]

if (macaddr.find(":")==-1 or len(macaddr)!=17):
  print
  print " Endereco mac com problemas."
  print " Utilize na forma aa:bb:cc:dd:ee:ff"
  print
  sys.exit(0)

## DHCP ##########################################################################################################
answer = raw_input(" Adicionar noh ao dhcp? [enter/n] ")

if (answer==''):
  try:
    filedhcp = open("/etc/dhcp/dhcpd.conf","r")
  except:
    print
    print " Arquivo /etc/dhcp/dhcpd.conf nao encontrado."
    print
    sys.exit(0)

  print " Arquivo /etc/dhcp/dhcpd.conf encontrado." 

  #backup do arquivo

  print " Fazendo backup do arquivo /etc/dhcp/dhcp.conf..." 
  os.system("cp /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd-backup.conf")
  print " Backup em /etc/dhcp/dhcp-backup.conf" 
  print
  
  buffer = []

  flag1=0
  for string in filedhcp.readlines():
    if (string.find("pxelinux.0")!=-1):
      flag1=1
    if (string.find('}')==0 and flag1==1):
      novoip = "192.168.0."+str(int(buffer[-1].split()[4].split('.')[3][0:-1])+1)
      #definir nova linha aqui
      novalinha = "  host "+hostname+" { fixed-address "+novoip+"; hardware ethernet "+macaddr+'; filename "pxelinux.0"; next-server 192.168.0.1; }\n'
      #imprimir no arquivo
      buffer.append(novalinha)
    buffer.append(string)
  filedhcp.close() #fecha para leitura

  filedhcp = open("/etc/dhcp/dhcpd.conf","w") #abre para gravacao
  for line in buffer:
    filedhcp.write("%s" % line)

  print
  print " Reinicie o servico de dhcp para efetivacao das mudancas: /etc/init.d/isc-dhcp-server restart"
  print


################################################################################################
answer = raw_input(" Adicionar noh ao /etc/hosts e /nfsroot/etc/hosts? [enter/n] ")

if (answer==''): # Se a resposta for sim

  if (novoip==''):
    novoip = raw_input(" Ip nao determinado automaticamente, escreva o ip ou aperte enter para finalizar: ")
  if (novoip==''):
    print
    print " Finalizando script."
    print  
    sys.exit(0)

  # definir a linha para ser incluida nos arquivos, ip\t hostname.gridnet\t hostname
  linha = novoip+"\t"+hostname+".gridlan\t"+hostname+"\n"

  try:
    with open("/etc/hosts", "a") as hostsfile:
      hostsfile.write(linha)
    with open("/nfsroot/etc/hosts", "a") as hostsfile:
      hostsfile.write(linha)
  except:
    print " Arquivo nao encontrado."
    sys.exit(0)
     
##################################################################################################################
answer = raw_input(" Criar novas chaves para o acesso vpn? [enter/n] ")
if (answer==''):
#  os.system("cd /etc/openvpn/easy-rsa && source ./vars && ./build-key "+hostname)
  subprocess.call("cd /etc/openvpn/easy-rsa && source ./vars && ./build-key "+hostname, shell=True, executable='/bin/bash')
  os.system("tar -cvvpzf /etc/openvpn/easy-rsa/keys/chaves-"+hostname+".tgz "+"/etc/openvpn/easy-rsa/keys/"+hostname+".* /etc/openvpn/easy-rsa/keys/ca.crt")
  print
  print " Credenciais para mandar para o cliente no arquivo /etc/openvpn/easy-rsa/keys/chaves-"+hostname+".tgz" 
  print " Para descompactar utilize:"
  print "   tar -xvvzf chaves-host-teste.tgz --strip-components 3 -C caminho"
  print


