#!/usr/bin/python

import platform, os, sys, subprocess

try:
  import psutil
except:
  print
  print " Para a execucao do script instale o pacote python-psutil."
  print
  sys.exit(0)

class instalation:
  def __init__(self):
    self.path='0'
    self.configurado='0'
    self.distro=platform.dist()[0] # Ubuntu, debian, centos, redhat, SuSE
    self.macaddr=''
    self.host=''
    self.pastainstalacao=''
    self.listapacotes='libvirt-bin libvirt0 python-libvirt kvm qemu-system-x86-64 qemu-kvm openvpn'
    self.pastainstalacao='/opt/gridlocal/'
    self.tuncapable=''
    self.dirname=os.path.dirname(sys.argv[0]) # caminho como em python /home/attila/teste/teste.py, self.dirname=/home/attila/teste
    if (self.dirname==''):
      self.dirname='.'

  def showmenu(self):
    print
    print " *********************************************************************************"
    print " Script para customizacao dos recursos disponiveis para o grid local e instalacao."
    print
    print " Opcoes:"
    if (self.configurado=='0'):
      print " 1) Customizacao dos recursos a serem disponibilizados para o grid local;"
    if (self.configurado=='1'):
      print " 1) Customizacao dos recursos a serem disponibilizados para o grid local; *configuracoes a serem instaladas"
    print " 2) Instalacao no sistema;"
    print " 3) Sair."
    print
    self.path = raw_input(" > ")
    if (self.path=='3'):
      sys.exit(0)

  def msgfinal(self,IPSERVIDOR,CONTATOEMAIL,host,macaddr):
    print
    print " *****"
    print " O seu computador precisa agora ser registrado no servidor do grid ("+IPSERVIDOR+")."
    print " Para proceder com o registro, envie um email para "+CONTATOEMAIL+", com as seguinte informacoes:"
    print
    print " Nome do host: "+host
    print " end. mac: "+macaddr
    print " *****"

  def checkuser(self):
    ### CHECAGEM DE ROOT PARA OPCAO 2 ###################################################################################
    if (self.path=='2'):
      if (os.popen("whoami").read()[0:-1]!='root'):
        print
        print " Usuario "+os.popen("whoami").read()[:-1]+", para utilizar esta opcao voce deve ter poderes de root."
        print
        self.path='9' # o procedimento=9 serve para o script ir ate o fim sem executar nada e reiniciar em seguida

  def checkvm(self): # CHECAGEM SE O PC PODE RODAR UMA VM, PARA A INSTALACAO
    if (self.path == '2'):
      if (os.popen("egrep '( vmx | svm )' /proc/cpuinfo").read()==''):
        print
        print " Este computador nao esta habilitado a rodar uma maquina virtual."
        print " Antes de instalar o sistema habilite a virtualizacao na bios e/ou no sistema operacional."
        print " Saindo do script."
        print
        print sys.exit(0)

  def getmacaddr(self):  ## PEGAR END. MAC ###################################################################################################
    iface = raw_input(" Digite a interface eth utilizada para conexao a rede ['enter' para eth0, 'list' para checar as interfaces disponiveis]: ")
    if (iface==''):
      iface='eth0'
    if (iface=='list'):
      print os.popen("/sbin/ifconfig |grep 'eth\|inet'").read()[0:-1]
      iface = raw_input(" Digite a interface eth utilizada para conexao a rede: ")

    self.macaddr = os.popen("/sbin/ifconfig |grep "+iface).read()[0:-1].split()[-1] # pega o ultimo campo da saida do comando
    print " Endereco mac da interface "+iface+": "+self.macaddr

  def customizarxml(self):
    subprocess.call("cp "+self.dirname+"/gridnode.bak "+self.dirname+"/gridnode.xml", shell=True, executable='/bin/bash') # copiar o xml de trabalho
    #name: changename
    answer2='n'
    while (answer2=='n'):
      answer = raw_input(" Digite o nome do computador a ser registrado no grid [enter para sugestao automatica]: ")

      if (answer == ''):
        host = os.popen("hostname").read()
        host = host[0:-1]
        host = host+'-'+self.macaddr[-8:].replace(':','')
      else:
        host=answer
      print
      answer2 = raw_input(" O nome da maquina virtual e do computador do grid sera "+host+". Confirma? [enter/n]: ")
      print
    self.host=host
    # modificando o xml
    subprocess.call("sed -i s/changename/"+host+"/g "+self.dirname+"/gridnode.xml", shell=True, executable='/bin/bash')

    # memory KiB: changememory
    answer = '1'
    while (int(answer) < 256):
      answer = raw_input(" Quantidade de memoria ram maxima a ser disponibilizada [enter para a sugestao: "+str(int(psutil.TOTAL_PHYMEM)/(1024*1024*6)
)+"MB (minimo de 256MB)]: ")
      if (answer==''): break
    # gravando no xml, deve ser em KiB
    if (answer==''):
      subprocess.call("sed -i s/changememory/"+str(int(psutil.TOTAL_PHYMEM)/(1024*6))+"/g "+self.dirname+"/gridnode.xml", shell=True, executable='/bin/bash')
    else:
      subprocess.call("sed -i s/changememory/"+str(int(answer)*1024)+"/g "+self.dirname+"/gridnode.xml", shell=True, executable='/bin/bash')

    ###
    # vcpu: changencpu
    # recomendacao de uso de cpus: metade dos nucleos logicos menos 1
    # checando se o hyperthread esta ligado
    if (os.popen("cat /proc/cpuinfo|grep ' ht '").read() != ''):
      ht=1
    else:
      ht=0

    if (ht==1):
      ncpus=int(psutil.NUM_CPUS)/2-1
    else:
      ncpus=int(psutil.NUM_CPUS)-1
    # modificando o xml
    subprocess.call("sed -i s/changencpu/"+str(ncpus)+"/g "+self.dirname+"/gridnode.xml", shell=True, executable='/bin/bash')
    print " Alocando "+str(ncpus)+" ao grid local."

    # mac: changemac
    # jah tenho o endereco mac do computador
    subprocess.call("sed -i s/changemac/"+self.macaddr+"/g "+self.dirname+"/gridnode.xml", shell=True, executable='/bin/bash')

  def customizarvpn(self):
    ### modificar arquivo de conf vpn cliente
    subprocess.call("cp "+self.dirname+"/vpn-cliente-grid.bak "+self.dirname+"/vpn-cliente-grid.conf", shell=True, executable='/bin/bash') # copiar o con de trabalho
    os.system("echo ca /opt/gridlocal/keys/ca.crt >> "+self.dirname+"/vpn-cliente-grid.conf")
    os.system("echo cert /opt/gridlocal/keys/"+self.host+".crt >> "+self.dirname+"/vpn-cliente-grid.conf")
    os.system("echo key /opt/gridlocal/keys/"+self.host+".key >> "+self.dirname+"/vpn-cliente-grid.conf")

  def instalarconfvpn(self):
    # copiar para a pasta /opt/gridlocal
    os.system("cp "+self.dirname+"/vpn-cliente-grid.conf "+self.pastainstalacao)

  def instalarpacotes(self):
    ## PACOTES ##########################################################################################################
    answer = raw_input(" Pressione enter para instalar os pacotes necessarios [enter/n]: ")
    if (answer==''):
      if (self.distro=='debian' or self.distro=='Ubuntu'): # SWITCH CASE: DEBIAN/UBUNTU
        os.system("apt-get install "+self.listapacotes)
      elif (self.distro=='centos' or self.distro=='redhat' or self.distro=='fedora'): #CENTOS
        os.system("yum install "+self.listapacotes)
      elif (self.distro=='SuSE'): #SUSE
        os.system("yast --install "+self.listapacotes)
      elif (self.distro=='gentoo'): #GENTOO
        os.system("emerge "+self.listapacotes)
      else: 
        print " Distribuicao "+self.distro+" nao suportada. "
        print " Saindo do script."
        sys.exit(0)
    else:
      print " Abortando instalacao de pacotes."
      print

  def instalarscriptservico(self):
    ## INTERFACE TAP ####################################################################################################
    answer = raw_input(" Pressione enter para instalar o script de inicializacao gridlocal [enter/n]: ")
    if (answer==''):
      if (self.distro=='debian'): # DEBIAN
        # O 1o comando troca o requisito para a execucao do script gridlocal na inicializacao
        subprocess.call("sed -i s/'libvirt-bin'/'libvirt-guests'/g "+self.dirname+"/gridlocal", shell=True, executable='/bin/bash')
        os.system("cp "+self.dirname+"/gridlocal /etc/init.d/")
        os.system("chmod 755 /etc/init.d/gridlocal")
        os.system("update-rc.d gridlocal defaults")
      if (self.distro=='Ubuntu'): # UBUNTU
        os.system("cp "+self.dirname+"/gridlocal /etc/init.d/")
        os.system("chmod 755 /etc/init.d/gridlocal")
        os.system("update-rc.d gridlocal defaults")
      elif (self.distro=='centos' or self.distro=='redhat' or self.distro=='fedora'): #CENTOS
        os.system("cp "+self.dirname+"/gridlocal /etc/init.d/")
        os.system("chmod 755 /etc/init.d/gridlocal")
        os.system("chkconfig --level 345 gridlocal on")
      elif (self.distro=='SuSE'): #SUSE
        os.system("cp "+self.dirname+"/gridlocal /etc/init.d/")
        os.system("chmod 755 /etc/init.d/gridlocal")
        os.system("insserv /etc/init.d/gridlocal")
      elif (self.distro=='gentoo'): #GENTOO
        pass
      else: 
        print " Distribuicao "+self.distro+" nao suportada. "
    else:
      print " Instalacao de script de inicializacao."
      print

  def criarpastainstalacao(self):
    ## DETERMINAR A PASTA DOS ARQUIVOS DE CONFIGURACAO ##################################################################
    subprocess.call("mkdir -p "+self.pastainstalacao+"keys", shell=True, executable='/bin/bash')

  def instaladiscovm(self):
    # instalar o disco na pasta /var/lib/libvirt/images/changename.img
    # primeiro descobrir o nome do host dentro do xml
    print
    print " Instalando o disco virtual de 2GB na pasta /var/lib/libvirt/images/"+self.host+".img"
    print
    subprocess.call("qemu-img create -f qcow2 -o size=2G /var/lib/libvirt/images/"+self.host+".img", shell=True, executable='/bin/bash') 

  def instalarxml(self):
    if (self.configurado=='1'):
      print
      print " Copiando o xml pronto para a pasta de configuracoes do gridlocal."
      print
      subprocess.call("cp "+self.dirname+"/gridnode.xml "+self.pastainstalacao, shell=True, executable='/bin/bash') 
      print " Criando arquivo "+self.pastainstalacao+"/host."
      os.system("echo "+self.host+" > "+self.pastainstalacao+"/host")
    else:
      print
      print " Eh necessario configurar o xml com a opcao '1' primeiramente."
      print

  def checkmodules(self): #checagem de modulos para a instalacao, kvm, tun...
    kvm='0'
    kvmintel='0'
    kvmamd='0'
    #tun
    checkdevtun = os.popen("test ! -c /dev/net/tun && echo 0 || echo 1").read()[0:-1] # 1 se existe o /dev/net/tun
    if (checkdevtun=='0'):
      subprocess.call("modprobe tun", shell=True, executable='/bin/bash') 
      if (os.popen("test ! -c /dev/net/tun && echo 0 || echo 1").read()[0:-1]=='1'):
        subprocess.call("echo tun >> /etc/modules", shell=True, executable='/bin/bash')
        print " Modulo tun adicionado ao arquivo /etc/modules"
      else:
        print
        print " Nao eh possivel inicializar uma interface tap exigida pelo openvpn."
        print " Saindo do script de instalacao."
        print
        print sys.exit(0)
    else:
      print " Interface tun encontrada."
    #kvm
    if (os.popen("lsmod|grep kv[m]").read()[0:-1]!=''):
      kvm='1'
    if (os.popen("lsmod|grep kvm_inte[l]").read()[0:-1]!=''):
      kvmintel='1'
    if (os.popen("lsmod|grep kvm_am[d]").read()[0:-1]!=''):
      kvmamd='1'
    if (kvm=='0'):
      subprocess.call("modprobe kvm", shell=True, executable='/bin/bash')
      if (os.popen("lsmod|grep kv[m]").read()[0:-1]!=''):
        kvm='1'
        subprocess.call("echo kvm >> /etc/modules", shell=True, executable='/bin/bash')
        print " Colocando o modulo kvm no arquivo /etc/modules."
        subprocess.call("modprobe kvm_intel", shell=True, executable='/bin/bash')
        if (os.popen("lsmod|grep kvm_inte[l]").read()[0:-1]!=''):
          kvmintel='1'
          subprocess.call("echo kvm_intel >> /etc/modules", shell=True, executable='/bin/bash')
          print " Colocando o modulo kvm_intel no arquivo /etc/modules."
        subprocess.call("modprobe kvm_amd", shell=True, executable='/bin/bash')
        if (os.popen("lsmod|grep kvm_am[d]").read()[0:-1]!=''):
          kvmamd='1'
          subprocess.call("echo kvm_amd >> /etc/modules", shell=True, executable='/bin/bash')
          print " Colocando o modulo kvm_amd no arquivo /etc/modules."
        if (kvmintel!='1' and kvmamd!='1'):
          print " Nao consigo carregar o modulo kvm especifico do processador."
          print " Saindo o script."
      else:
        print " Nao consigo carregar o modulo kvm."
        print " Saindo o script."
        sys.exit(0)
