import socket as so
import _thread
import socket,time
import sys,requests
from winsound import Beep
whistling=False
currently=False
def passive_whistle():
    while True:
        if whistling:
            whistle(5000)
            time.sleep(0.005)
            
def whistle(duration=5000):
    Beep(18000,duration)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = str(s.getsockname()[0])
s.close()
HOST = ip
PORT=5001


s= so.socket(socket.AF_INET,so.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST,PORT))
s.listen(10)

print(f'Waitng for connection at {HOST}...')
def sendall(message,raw):
    global whistling
    global s
    global conns
    if raw == '': return
    mess = str(message)
    #print("Message >" + mess +" "+str(type(mess)))
    if "beep" in mess:
        print("Beeping")
        whistle()
    if "start" in mess:
        print("continous beep start")
        whistling=True
    elif "stop" in mess:
        print("continous beep stop")
        whistling=False
    for i in conns:
        try:
            i.sendall(message)
        except:
            continue
        
def client(conn,addr):
    
    last5=[' ',' ',' ',' ',' ']
    while True:
        try:
            data=conn.recv(10000)
            dat = data.decode('utf-8')
            del last5[0]
            last5.append(dat)
            if last5 ==['','','','','']:
                
                print("Connection with " + str(addr[0]+' has been terminated.'))
                m = "Connection with " + str(addr[0]+' has been terminated.')
                sendall(bytes(m,'utf-8'),m)
                sys.exit()
            if not (dat==''):
                
                
                #print('['+str(addr[0])+']:'+ str(data.decode('utf-8')))
                
               
                sendall(bytes(str(data.decode('utf-8')),'utf-8'),data.decode('utf-8'))
                
            
        except Exception as e:
            print('error')
            print(e.with_traceback(None))
            s.close()
            
            sys.exit()

conns = []
_thread.start_new_thread(passive_whistle,())
while 1:
    conn, addr = s.accept()
    conns.append(conn)
    
    print("The connection has been set up with %s " %(str(addr[0])))
    _thread.start_new_thread(client,(conn,addr))

