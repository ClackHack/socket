import socket as so
import os,sys
from tkinter import messagebox
import tkinter as tk
clear=lambda:os.system("cls")
labeltext=''
import socket,_thread
sb = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sb.connect(("8.8.8.8", 80))
ip = str(sb.getsockname()[0])
sb.close()
MONOSPACES=("Consolas",11)
#target=input("IP: ")
#name = input("Whats Your Name: ")
class app(tk.Tk):
    def __init__(self,*args, **kwargs):
        tk.Tk.__init__(self,*args, **kwargs)
        self.frame=tk.Frame()
        self.geometry("1000x700")
        self.frame.pack(side = "top", fill = "both", expand = True)
        self.title("Chat")
        tk.Label(self.frame,text="Name: ").grid(row=0,column=0,padx=5,pady=5)
        self.name = tk.StringVar()
        tk.Entry(self.frame,textvariable=self.name).grid(row=0,column=1,padx=5,pady=5)
        tk.Label(self.frame,text="IP: ").grid(row=1,column=0,padx=5,pady=5)
        self.host = tk.StringVar()
        try:
            target=open("server.txt","r").read()
        except:
            target=""
        self.host.set(target)
        tk.Entry(self.frame,textvariable=self.host).grid(row=1,column=1,padx=5,pady=5)
        tk.Button(self.frame,text="Join",command=self.join).grid(row=2,column=0,padx=5,pady=5)
    def join(self):
        self.protocol("WM_DELETE_WINDOW",self.exit)
        if self.name.get() and self.host.get():
            open("server.txt","w").write(self.host.get())
        else:
            messagebox.showerror("Error","Field left blank")
            return
        for i in self.frame.winfo_children():
            i.destroy()
        self.setup()
    def setup(self):
        self.width=120
        self.frame.pack(side = "top", fill = "both", expand = True)
        self.table = tk.Listbox(self.frame,width=self.width,height=25,font=MONOSPACES,exportselection=False)
        self.table.grid(row=0,column=0,columnspan=4,padx=5,pady=5)
        self.text=tk.StringVar()
        tk.Entry(self.frame,textvariable=self.text,width=150).grid(row=1,column=0,columnspan=2,padx=5,pady=5)
        tk.Button(self.frame,text="Send",command=self.send).grid(row=2,column=0,padx=5,pady=5)
        tk.Button(self.frame,text="Exit",command=self.exit).grid(row=3,column=0,padx=5,pady=5)
        #Connect to server
        port=5001

        self.s=so.socket(so.AF_INET,so.SOCK_STREAM)
        self.s.connect((self.host.get(),port))
        self.s.settimeout(1)
        self.exit=False
        self.bind("<Return>",self.send)
        _thread.start_new_thread(self.handle,())
    def recv(self):
        while 1:
            try:
                if self.exit:
                    sys.exit()
                data = self.s.recv(3000)
                return str(data.decode('utf-8'))
            except OSError:
                pass
    def send(self,whatever=None):
        text = f"[{self.name.get()}]: "+self.text.get()
        self.s.send(bytes(str(text) + " " ,"utf-8"))
        self.text.set("")
    def handle(self):
        while 1:
            n = self.width -1
            data = []
            for j in self.recv().split("\n"):
                temp=[j[i:i+n] for i in range(0, len(j), n)]
                data.extend(temp)
            for i in data:
                self.table.insert(tk.END,"\n"+i)
            self.table.see(tk.END)
    def exit(self):
        self.s.close()
        self.exit=True
        self.destroy()
app().mainloop()
'''try:
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
    text = input("")
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


'''
