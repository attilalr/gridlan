import sys, os

###################################################################
def load_nodes_data(filename='/etc/gridlocal/nodes.stats'):

  # load file in "nodename n_cpus comp_power" format
  try:
    file=open(filename,'r')
  except:
    print " Problem when loading file "+filename
    print
    sys.exit(0)

  ret_lst=[]

  linha=file.readline()
  while(linha):
    # check if there is 3 fields before an '#'
    if (len(linha[:linha.find('#')].split())==3):
      ret_lst.append([linha.split()[0],int(linha.split()[1]),float(linha.split()[2])])
    linha=file.readline()
  file.close()

  # sort by total computational power
  ret_lst.sort(key=lambda x:x[1]*x[2])
  return ret_lst

###################################################################
def share_work(amount,lst):
  total_comp_power=0
  for i in lst:
    total_comp_power=total_comp_power+(float(i[1])*i[2])
  return_lst=[]
  count=0
  # loop in all but the last node
  for i in range(len(lst)-1):
    quant=int((float(lst[i][1])*lst[i][2]/total_comp_power)*amount)
    return_lst.append([lst[i][0],quant])
    count=count+quant
  return_lst.append([lst[len(lst)-1][0],amount-count])

  return return_lst

###################################################################
def store_nodes_data(lst,filename='/etc/gridlocal/nodes.stats'):
  try:
    file=open(filename,'w')
  except:
    print
    print " Problem when loading file "+filename+", check folder permissions."
    print
    return -1

  file.write("# nodename n_cores comp_power_per_core\n")
  for node in lst:
    file.write(node[0]+' '+str(node[1])+' '+str(node[2]))
    file.write('\n')
  file.close()

#################################################
def check_nodes_n_cores(lst_hosts):

  ret_lst=[]

  for node in lst_hosts:
    n_cores=os.popen('ssh '+node+' cat /proc/cpuinfo|grep processor|wc -l').read()
    if (n_cores != ''):
      ret_lst.append([node,int(n_cores)])
    else:
      print ' Problem in '+'ssh '+node+' cat /proc/cpuinfo|grep processor|wc -l'+' command.'
      print ' Node may be down. Script will exit.'
      sys.exit(0)

  return ret_lst

##################################### run tests ######
def run_new_test(lst,minutes):

  # user send lst, lets use just the hostnames and return a new nodes list
  nodes=list()
  cores=list()

  # first lets get the number os cores in each node
  for i in lst:
    node=i[0]
    nodes.append(node)
    return_cmd=os.popen('rsh '+node+' cat /proc/cpuinfo|grep processor|wc -l').read()[:-1]
    if (return_cmd != ''):
      cores.append(int(return_cmd))
    else:
      print " Problem when connecting node "+node+". Script will exit."
      print
      sys.exit(0)

  #write mpi python file for the cpu test
  try:
    file=open('./mpitest.py','w')
  except:
    print ' Problem to write the mpi python file for tests. Check the folder where you are.'
    sys.exit(0)

  #creating a mpi python file to run the tests
  #deb dependency: python-mpi4py
  file.write('from mpi4py import MPI\n')
  file.write('import numpy, time\n')
  file.write('min_to_run=float('+str(minutes)+')\n')
  file.write('N=2000\n')
  file.write('comm = MPI.COMM_WORLD\n')
  file.write('rank = comm.Get_rank()\n')
  file.write('start=time.time()\n')
  file.write('while((time.time()-start)/60.0 < min_to_run):\n')
  file.write('  cont=0\n')
  file.write('  for i in range(N):\n')
  file.write('    for j in range(N):\n')
  file.write('      x=numpy.random.rand()\n')
  file.write('      y=numpy.random.rand()\n')
  file.write('      if (x*x+y*y<1):\n')
  file.write('        cont=cont+1\n')
  file.write('  result=4*(float(cont)/N/N)\n')
  file.write('  print MPI.Get_processor_name()\n')
  file.close()

  # running the tests
  # first we set a string with the node names in node01,node02,node03 format
  str_hosts=''
  for host in lst[:-1]:
    str_hosts=str_hosts+host[0]+','
  str_hosts=str_hosts+lst[-1][0]
  try:
#    print 'mpirun -H '+str_hosts+' python mpitest.py'
    result=os.popen('mpirun -H '+str_hosts+' python mpitest.py').read()
  except:
    print " Problem when running mpirun:"
    print result
    print
    return -1

  # remove mpi file
  os.system('rm ./mpitest.py')

  # now we analyze the results
  l_data=result.split()
  # put all in lower case
  for i in range(len(l_data)):
    l_data[i]=l_data[i].lower()
  l_power=list()
  min_value=10000000
  for i in lst:
    node=i[0]
    data=l_data.count(node.lower())
    if (data<min_value):
      min_value=data
    l_power.append(data)

  # normalizing by the lesser value
  for i in range(len(l_power)):
    l_power[i]=float(l_power[i])/min_value


  # create and sort by comp power the final list
  ret_list=list()
  for node, n_cores, power in zip(nodes,cores,l_power):
    ret_list.append([node,n_cores,power])

  ret_list.sort(key=lambda x:float(x[1])*x[2])
  return ret_list

if __name__ == '__main__':

  lst_nodes=load_nodes_data('/home/attila/nodes.stats')
#  print share_work(1000,lst_nodes)
  print lst_nodes
  lst_nodes=run_new_test(lst_nodes,200)
  print lst_nodes
  print share_work(1000,lst_nodes)
  store_nodes_data(lst_nodes,'/home/attila/nodes.stats')

