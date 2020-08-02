import socket as so
import os
clear=lambda:os.system("cls")
labeltext=''
import socket
sb = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sb.connect(("8.8.8.8", 80))
ip = str(sb.getsockname()[0])
sb.close()
#target=input("IP: ")
name = input("Whats Your Name: ")
try:
    target=open("server.txt","r").read()
except:
    target = input("IP: ")
    open("server.txt","w").write(target)
port=5001
print("Connecting...")
s=so.socket(so.AF_INET,so.SOCK_STREAM)
s.connect((target,port))
s.settimeout(1)
def recv():
  global s
  global exit
  while 1:
    try:
      if exit:
        sys.exit()
      data = s.recv(3000)
      return str(data.decode('utf-8'))
    except OSError:
      pass
def send():
  global ip
  global s
  global labeltext
  while 1:
    text = input()
    clear()
    import time
    if text == '':
      global exit
      exit=True
      exitt()
    print(labeltext)
    if exit:
      return
      sys.exit()
    text = f"[{name}]: "+text
    s.send(bytes(str(text) + " " ,"utf-8"))
def exitt():
  print('Exiting...')
  global s
  s.close()
  global exit
  exit = True
  sys.exit()
#s.close()
labeltext='Connecting...\nConnected'
import _thread
_thread.start_new_thread(send,())
exit = False
print('Connected')
while 1:
  try:
    data = recv()
    print(data)
    labeltext = labeltext + str('\n'+data)
  except TypeError as e:
    pass


