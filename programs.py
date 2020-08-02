import random
def remote_input(conn,text):
    conn.sendall(bytes("[Server]: "+text,"utf-8"))
    while 1:
        data=conn.recv(10000)
        dat=data.decode("utf-8")
        return dat.split("]: ",1)[1]
def send(conn,text):
    conn.sendall(bytes("[Server]: "+text,"utf-8"))

    
programs={}
