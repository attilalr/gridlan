import zerorpc, os, time, datetime

def log(msg):
  try:
    file=open(os.environ['programfiles']+'\\gridlan\heartbeat.log','a')
    file.write(str(datetime.datetime.today())+": "+msg+'\n')
    file.close()
  except:
    pass

hostname=os.popen('more "%programfiles%\gridlan\hostname.txt"').read()[:-1]

c = zerorpc.Client()

try:
  c.connect("tcp://143.54.155.233:4242")
  log("connected")
  if c.chk_stats(hostname)=='off':
    log("running restart script!")
    os.system('cd %programfiles%\\gridlan && restart_all')
  else:
    log(c.chk_stats(hostname))
except:
  pass

