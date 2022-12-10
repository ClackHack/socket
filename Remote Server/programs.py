import random,praw
from random import choice
import wikipedia
import webcam_server, threading, time, sys
global programs
w = webcam_server.Webcam()
t= threading.Thread(target=w.start_server)
t.start()
def reddit(subred):
    redd = praw.Reddit(client_id='65QjysWPOx2BJA',client_secret= 'DZRSymghvq9ZOTB_xH0vDbn6_7Y',password='beepboop',username='IMeanMeTooThanksBot',user_agent='MeTooThanks')
    sub=redd.subreddit(subred)
    num = 0
    jokes =[]
    for sub in sub.hot(limit=30):
        num = num + 1
        if num == 1:
            continue
        joke = str(sub.title +'\n' +sub.selftext).replace('\n\n','\n')
        jokes.append(joke)
    return choice(jokes)
def remote_input(conn,text):
    conn.sendall(bytes("[Server]: "+text,"utf-8"))
    while 1:
        data=conn.recv(10000)
        dat=data.decode("utf-8")
        return dat.split("]: ",1)[1]
def send(conn,text):
    conn.sendall(bytes("[Server]: "+text,"utf-8"))

def repeat(conn,args):
    x=remote_input(conn,"Repeat: ")
    return x
def dice(conn,args):
    num = random.randint(1,6)
    out="\n#####\n"
    if num==1:
        out+="     \n"
        out+="  X  \n"
        out+="     \n"
    if num ==2:
        out+="X    \n"
        out+="     \n"
        out+="    X\n"
    if num == 3:
        out+="X    \n"
        out+="  X  \n"
        out+="    X\n"
    if num ==4:
        out+="X   X\n"
        out+="     \n"
        out+="X   X\n"
    if num == 5:
        out+="X   X\n"
        out+="  X  \n"
        out+="X   X\n"
    if num==6:
        out+="X   X\n"
        out+="X   X\n"
        out+="X   X\n"
    out+="#####"
    return out
def hangman(conn,args):
    phrases = open("words.txt",'r').read().split()
    secret = random.choice(phrases)
    del phrases
    temp=""
    for i in range(len(secret)):
        if secret[i] == " ":
            temp+="      "+" "
        else:
            temp+="_"+" "
    send(conn,temp)
    complete = False
    guessed = []
    count = -1
    n = 6
    while not complete:
        if count >=n:
            complete = True
            return f"You lose!!!, the word was {secret}\n"
            continue
        place = True
        for i in secret.lower():
            if i == " ": 
                continue
            if not i in guessed:
                
                place = False
        if place:
            return "You win!!!\n"
            complete = True
            continue
        count = count + 1
        send(conn,"You have "+ str(n-count+1)+ " guesses left...\n")
        
        let = remote_input(conn,"Letter: \n").strip()
        #print(let)
        if len(let) > 1:
            count = count-1
            send(conn,"Enter 1 letter at a time!\n")
            continue
        if not let in guessed:
            guessed.append(let.lower())
        else:
            send(conn,"You already entered that\n")
            #draw(count)
            continue
        if let in secret.lower():
            count = count - 1
        else:
            send(conn,"Incorrect\n")
        temp=""
        for i in secret:
            doesnt_match = True
            for b in guessed:
                if i.lower() ==b:
                    temp+=i+" "
                    doesnt_match = False
            if doesnt_match and i != " ":
                temp+="_"+" "
            elif i == " ":
                temp+="      "+ ""
        send(conn,temp+"\n\n")
        send(conn,'Guessed: \n')
        temp=""
        for i in guessed:
            temp+=i+' '
        send(conn,temp+"\n")
        #print("\n\n")
    return "Game Over"
def program_list(conn,args):
    global programs
    out="\n"
    for i,h in programs.items():
        out+=i+"\n"
    return out
def joke(conn,args):
    return reddit("Jokes")
def fact(conn,args):
    return reddit("todayilearned")
def red(conn,args):
    return reddit(args.strip())
def wiki(conn,args):
    lis = wikipedia.search(args.strip())
    #x=wikipedia.page(lis[0])
    return wikipedia.summary(lis[0],sentences=6)
def hangmanvs(conn,args):
    usage= "etaoinsrhdlucmfywgpbvkxqjz"
    words = open("words.txt","r").read().split()
    temp = []
    send(conn,"Welcome to hangman!\nThe computer will guess! \nRules are you must pick an english word\n")
    length = int(remote_input(conn,"What is the length of your word?: ").strip())
    for i in words:
        if len(i) == length and not "-" in i:
            temp.append(i.lower())
    lives = 6
    words = temp
    temp = []
    send(conn,str(len(words))+" possible words")
    guessed = []
    word = ["" for i in range(length)]
    def guess(letter):
        x = remote_input(conn,"Is '"+letter+"' your word? (y/n): ").strip()
        if x.lower() == "y":
            x = remote_input(conn,"What position(s) is '"+letter+"' at? (Start at index 1): ")
            x=x.split()
            x = [int(i) -1 for i in x]
            return x
        elif x.lower() == "n":
            return []
    def printlives(lives):
        out=""
        for i in range(lives): 
            out+="♥"
        send(conn,out+"\n")


    while "" in word:
       if lives <=0:
          break
       if len(words) == 0:
           return "You sure you put in an english word?\n"
           import sys
           sys.exit()
       if len(words) == 1:
           x=remote_input(conn,"Is "+words[0]+" your word? (y/n): ").strip()
           #x = input()
           if x.lower() == "y":
               lives = 1
               break
           else:
               lives = 0
               send(conn,"Not sure thats an english word but ok...\n")
               break
       letterprob = {}
       empty = []
       for i in range(len(word)):
           if word[i] == "":
               empty.append(i)
       for i in words:
            for j in empty:
                if i[j].lower() in guessed:
                    continue
                elif i[j].lower() in letterprob.keys():
                    letterprob[i[j].lower()] = letterprob[i[j].lower()]+1

                else:
                    letterprob[i[j].lower()] = 1
       maxletter=""
       maxnum=0
       for i,j in letterprob.items():
           if j > maxnum:
               maxletter = i
               maxnum = j
       guessed.append(maxletter)
       g = guess(maxletter)
       for i in g:
           word[i] = maxletter
       if g:
          for i in words:
               works = True
               for j in g:
                   if i[j] != maxletter:
                       works = False
               for j in range(len(i)):
                   if j in g:
                       continue
                   else:
                       if i[j] == maxletter:
                          works = False
               if works:
                    temp.append(i)
          words = temp
          temp = []
       else:
          lives -=1
          for i in words:
                if not maxletter in i:
                    temp.append(i)
          words = temp
          temp = []
       send(conn,"Possible Words: "+str(len(words))+"\n")
       out=""
       for i in word:
           if i == "":
               out+="_ "
           else:
               out+=i+" "
       send(conn,out+"\n")
       printlives(lives)
       
    if lives <=0:
        return "You win, you have bested me\n"
    else:
        return "HAHA, I win! Try again if you dare!\n"
def math(conn,args):
    return str(eval(args))    

def webcam(conn,args):
    global w
    if not args:
        return ""
    if args.strip().lower() == "start":
        w.start()
        return "serving webcam on port 5050"
    elif args.strip().lower() == "stop":
        w.stop()
        return "Webcam Stopped"


programs={"dice":dice,"hangman":hangman,"programs":program_list,
"joke":joke,"fact":fact,"reddit":red,"wikipedia":wiki,"hangmanvs":hangmanvs,"math":math,
"webcam":webcam}


if __name__ =="__main__":
    webcam(None,"start")
    print("running")
    time.sleep(30)
    webcam(None,"stop")
    print("process killed")
    time.sleep(20)
    webcam(None,"start")
    print("running")
    time.sleep(30)
    webcam(None,"stop")
    print("process killed")