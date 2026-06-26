from BasicTypes import *
from BasicFunctions import *
from tkinter import *
from tkinter import filedialog
def definingTheFilePath(method=0):
    if(method==0):
        return "test code.cyrx"
    elif(method==1):
        return input("Шлях до файлу .cyrx: ")
    elif(method==2):
        Window=Tk()
        Label(Window,text=
"""CircleScript використовує файли
.cyrx для зберігання коду та .cyrl
для зберігання бібліотек функцій.
Хоча ви можете зберігати ці данні
й в інших текстових форматах""").pack()
        filetypes=[("CircleScript","*.cyrx"),("CircleScriptLib","*.cyrl"),("All files","*")]
        path=filedialog.askopenfilenames(parent=Window,initialdir='',initialfile='',filetypes=filetypes)
        Window.destroy()
        if(len(path)>0):
            return path[0]
    return ""
path=definingTheFilePath(0)
with open(path,'r',encoding='utf-8') as file:
    info=[]
    for line in file:
        if(line.strip()!=""):
            info.append(line.strip())
functions=[]
for i in range(len(info)):
    if(info[i][0]=="↣" or info[i][0:2]=="#s"):
        n=""
        if(info[i][0]=="↣"):
            offset=1
        else:
            offset=2
        for j in range(offset,len(info[i])):
            if(set([info[i][j]])-{"0","1","2","3","4","5","6","7","8","9"}==set()):
                n+=info[i][j]
            else:
                if(n!=""):
                    functions.append([int(n),info[i]])
                break
functions.sort(key=lambda x:x[0])
for i in range(len(functions)):
    f,b,r,j="",0,0,0
    while j<len(functions[i][1]):
        if(functions[i][1][j]=="{" or functions[i][1][j]=="("):
            r+=1
            if(f==""):
                f=functions[i][1][j]
                b=j
        elif(functions[i][1][j]=="}" or functions[i][1][j]==")"):
            r-=1
        if((f=="{" and functions[i][1][j]==")" and r==0) or (f=="(" and functions[i][1][j]=="}" and r==0) or (f=="(" and functions[i][1][j]==")" and functions[i][1][j+1:j+2]!="{" and r==0)):
            functions[i]=functions[i][1][b:j+1]
            break
        j+=1
s=Stack()
for i in range(len(functions)):
    function_(functions[i],s).do()
print("Стек:",s)