#Server File
import socket as so
import _thread
import socket
import sys,requests
import programs
print("Modules loaded")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = str(s.getsockname()[0])
s.close()
HOST = ip
PORT=5001
def begin(text,r):
    return text[:len(r)]==r

s= so.socket(socket.AF_INET,so.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST,PORT))
s.listen(10)

print(f'Waitng for connection at {HOST}...')
def sendall(message,raw):
    global s
    global conns
    if raw == '': return
    for i in conns:
        try:
            i.sendall(message)
        except:
            continue
def remote_input(conn,text):
    conn.sendall(bytes("[Server]: "+text,"utf-8"))
    while 1:
        data=conn.recv(10000)
        dat=data.decode("utf-8")
        return dat
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
                sendall(bytes(str(data.decode('utf-8')),'utf-8'),data.decode('utf-8'))
                for i,j in programs.programs.items():
                    #print(i)
                    command = dat.split("]: ",1)[1]
                    #print(i,command)
                    if command.split(" ")[0].strip()==i:
                        #print(i)
                        args = command.replace(i+" ","",1)
                        try:
                            x=j(conn,args)
                            sendall(bytes("[Server]: "+x,"utf-8"),"[Server]: "+x)
                        except LookupError as e:
                            print(e)
                            sendall(bytes("[Server]: "+str(e),"utf-8"),"[Server]: "+str(e))

                #print('['+str(addr[0])+']:'+ str(data.decode('utf-8')))
               
                #sendall(bytes(str(data.decode('utf-8')),'utf-8'),data.decode('utf-8'))
                
            
        except KeyError as e:
            print('error')
            print(e)
            s.close()
            
            sys.exit()

conns = []
while 1:
    conn, addr = s.accept()
    conns.append(conn)
    
    print("The connection has been set up with %s " %(str(addr[0])))
    _thread.start_new_thread(client,(conn,addr))

