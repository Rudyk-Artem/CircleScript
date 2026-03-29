from BasicTypes import *
from BasicFunctions import *

path="D:\\мої програми\\Python\\CircleScript\\test code.cyrx"
# path=input("Шлях до файлу з кодом: ")
try:
    with open(path,'r',encoding='utf-8') as file:
        info=[]
        for line in file:
            if(line.strip()!=""):
                info.append(line.strip())
except FileNotFoundError:
    print(f"Error: The file '{path}' was not found.")
except IOError:
    print(f"Error reading the file: '{path}'.")
# print(info)
functions={}
for i in range(len(info)):
    if(info[i][0]=="↣"):
        n=""
        for j in range(1,len(info[i])):
            if(set([info[i][j]])-{"0","1","2","3","4","5","6","7","8","9"}==set()):
                n+=info[i][j]
            else:
                if(n!=""):
                    functions[int(n)]=info[i]
                break
functions=list(functions.items())
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
        elif(functions[i][1][j]=="\\"):
            if(functions[i][1][j+1:j+2]=="\\"):
                functions[i]=(functions[i][0],functions[i][1][:j]+"\\"+functions[i][1][j+2:])
            elif(functions[i][1][j+1:j+2]=="n"):
                functions[i]=(functions[i][0],functions[i][1][:j]+"\n"+functions[i][1][j+2:])
            elif(functions[i][1][j+1:j+2]=="t"):
                functions[i]=(functions[i][0],functions[i][1][:j]+"\t"+functions[i][1][j+2:])
        if((f=="{" and functions[i][1][j]==")" and r==0) or (f=="(" and functions[i][1][j]=="}" and r==0) or (f=="(" and functions[i][1][j]==")" and functions[i][1][j+1:j+2]!="{" and r==0)):
            functions[i]=functions[i][1][b:j+1]
            break
        j+=1
# print(functions)
s=Stack()
for i in range(len(functions)):
    function_(functions[i],s).do()
# print(s)