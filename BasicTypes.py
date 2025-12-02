from cmath import phase,isnan,isinf
from math import log,pi
errorCodes={Exception:0,TypeError:1,ValueError:2,IndexError:3,KeyError:4,SyntaxError:5,ArithmeticError:6,RecursionError:7,SystemExit:8}
priorityOfOperations={"+":1,"-":1,"*":2,"/":2,"↧":3,"^":4,"√":4,"E":5,"~":6}
constants={"τ":6.2831853071795864,"π":3.1415926535897932,"e":2.7182818284590452,"φ":1.6180339887498948,"i":1j,"∞":complex('inf'),"∅":complex('nan')}
defaultValue={"+":(0,0),"-":(0,0),"*":(1,1),"/":(1,1),"↧":(constants["e"],1),"^":(2,1),"√":(2,1),"E":(1,0),"~":(-1,-1)}
operations={"+":lambda a,b:a+b,"-":lambda a,b:a-b,"*":lambda a,b:a*b,"/":lambda a,b:a/b,"↧":lambda a,b:a.Ln()/b.Ln(),"^":lambda a,b:a**b,"√":lambda a,b:a**(num_(1)/b),
            "E":lambda a,b:a*num_(10)**b,"~":lambda a,b:a*b,"n":lambda a:num_(a),"c":lambda a:num_(constants[a]),"d":lambda d:num_(defaultValue[d[0]][d[1]])}
def is_number(s):
    try:
        num_(s)
        return True
    except:
        return False
class ExpressionTreeNode():
    def __init__(self,v,d=("+",0)):
        pl=[]
        for i in range(len(v)):
            if(set([v[i]])-set(priorityOfOperations.keys())==set()):
                pl.append(priorityOfOperations[v[i]])
        if(pl!=[]):
            o=min(pl)
            for i in range(len(v)):
                try:
                    if(priorityOfOperations[v[i]]==o):
                        self.op=v[i]
                        self.left=ExpressionTreeNode(v[:i],(v[i],0))
                        self.right=ExpressionTreeNode(v[i+1:],(v[i],1))
                        self.value=None
                        break
                except:
                    pass
        else:
            if(set([v])-set(constants.keys())==set()):
                self.op='c'
                self.left=None
                self.right=None
                self.value=v
            elif(is_number(v)):
                self.op='n'
                self.left=None
                self.right=None
                self.value=v
            else:
                self.op='d'
                self.left=None
                self.right=None
                self.value=d
    def count(self):
        if(set([self.op])-set(operations.keys())==set()):
            if(set([self.op])-set(priorityOfOperations.keys())==set()):
                return operations[self.op](self.left.count(),self.right.count())
            return operations[self.op](self.value)
def value(v):
    if(type(v)==str):
        if(v[:4].capitalize()=="None"):
            v=none_()
        elif(v[:4].capitalize()=="True" or v[:5].capitalize()=="False"):
            v=bool_(v)
        elif(v[:1]=='"'):
            v=str_(v[1:-1])
        elif(v[:1]=="'"):
            v=bytes_(v)
        elif(v[:1]=='{'):
            for i in range(1,len(v)):
                if(v[i]=='@' or v[i]=='₴'):
                    v=function_(v)
                    break
                elif(v[i]=='}'):
                    v=error_(v)
                    break
        elif(v[:1]=='['):
            if(set([v])-{"[none]","[num]","[bool]","[bytes]","[str]","[list]","[dict]","[function]","[type]","[error]"}==set()):
                v=type_(v)
            else:
                for i in range(1,len(v)):
                    if(v[i]==':'):
                        v=dict_(v)
                        break
                    elif(v[i]==',' or v[i]=='['):
                        v=list_(v)
                        break
        elif(set([v[:1]])-{'0','1','2','3','4','5','6','7','8','9','+','-','i','n','∞','∅','('}==set()):
            v=num_(v)
    try:
        if(type(v)==type and set([v])-set(errorCodes.keys())==set()):
            v=error_(v)
        else:
            baseValueTypes={type(None):none_,int:num_,float:num_,complex:num_,bool:bool_,bytes:bytes_,str:str_,list:list_,dict:dict_,type:type_}
            v=baseValueTypes[type(v)](v)
    except KeyError:
        pass
    if(issubclass(type(v),value_)):
        return v
    else:
        raise ValueError
class value_():
    def __init__(self,v):
        self.v=v
    def __str__(self):
        return str(self.v)
    def __eq__(self,other):
        return self.v==other.v
class none_(value_):
    def __init__(self,v=None):
        pass
    def __str__(self):
        return "None"
    def __eq__(self,other):
        return type(self)==type(other)
    def __hash__(self):
        return hash(None)
class num_(value_):
    def __init__(self,n):
        if(type(n)==str_):
            n=str(n)[1:-1]
        if(type(n)==str):
            if(n[:1]=='('):
                n=num_(ExpressionTreeNode(n[1:-1]).count())
            else:
                n=n.replace('∞','inf').replace('∅','nan').replace('~i','j')
        if(isinf(complex(n)) or isnan(complex(n)) or abs(complex(n))==0):
            n=abs(complex(n))
        self.n=complex(n)
    def __str__(self):
        if(self.isReal()):
            r=str(self.n.real).replace('e','E')
            if(float(r)%1==0):
                r=r.replace('.0','')
            return r.replace('inf','∞').replace('nan','∅')
        elif(self.isImag()):
            i=str(self.n.imag).replace('e','E')
            if(float(i)%1==0):
                i=i.replace('.0','')
            return i+'~i'
        else:
            r=str(self.n.real).replace('e','E')
            i=str(self.n.imag).replace('e','E')
            if(float(r)%1==0):
                r=r.replace('.0','')
            if(float(i)%1==0):
                i=i.replace('.0','')
            if(float(i)>=0):
                i='+'+i
            return r+i+'~i'
    def __int__(self):
        if(self.isInteger()):
            return int(self.n.real)
        raise ValueError
    def __float__(self):
        if(self.isReal()):
            return self.n.real
        raise ValueError
    def __complex__(self):
        return self.n
    def __eq__(self,other):
        if(isnan(self.n) and isnan(other.n)):
            return True
        return self.n==other.n
    def __hash__(self):
        return hash(self.n)
    def __round__(self,n):
        if(type(n)==int):
            self.n=complex(round(self.n.real,n),round(self.n.imag,n))
            return self
        raise ValueError
    def __add__(self,other):
        return num_(self.n+other.n)
    def __sub__(self,other):
        return num_(self.n-other.n)
    def __mul__(self,other):
        return num_(self.n*other.n)
    def __truediv__(self,other):
        if(other.n==0):
            if(self.n==0 or isnan(self.n)):
                return num_('nan')
            else:
                return num_('inf')
        else:
            return num_(self.n/other.n)
    def __pow__(self,other):
        if(isnan(other.n) or isnan(self.n) or (other.n==0 and (self.n==0 or isinf(self.n))) or (isinf(other.n) and isinf(self.n))):
            return num_('nan')
        elif(((other.n.imag!=0 or other.n.real<0) and self.n==0) or ((other.n.real>0) and isinf(self.n)) or (isinf(other.n) and (self.n!=1))):
            return num_('inf')
        elif((other.n.real<0) and isinf(self.n)):
            return num_(0)
        else:
            return num_(self.n**other.n)
    def Ln(self,k=0):
        if(self.n==0):
            return num_('nan')
        return num_(log(abs(self.n))+1j*(phase(self.n)+2*pi*k))
    def isInteger(self):
        return (self.n.imag==0 and self.n.real%1==0 and abs(self.n.real)<9007199254740992)
    def isReal(self):
        return (self.n.imag==0)
    def isImag(self):
        return (self.n.real==0)
class bool_(value_):
    def __init__(self,b):
        if(type(b)==str_):
            b=str(b)[1:-1]
        if(type(b)==str):
            if(b=="True" or b=="true"):
                b=True
            elif(b=="False" or b=="false"):
                b=False
        if(type(b)==int):
            if(b==1):
                b=True
            elif(b==0):
                b=False
        if(type(b)==bool):
            self.b=bool(b)
        else:
            raise ValueError
    def __str__(self):
        if(self.b):
            return "True"
        return "False"
    def __bool__(self):
        return self.b
    def __eq__(self,other):
        return self.b==other.b
    def __hash__(self):
        return hash(self.b)
class bytes_(value_):
    def __init__(self,b):
        if(type(b)==str_):
            b=str(b)[1:-1]
        if(type(b)==str):
            l=[]
            s,f=1,1
            for i in range(1,len(b)):
                if(b[s]=='\\'):
                    if((b[i]=="\\" or b[i]=="'") and i>1):
                        s=f
                        f=i
                        l.append(int(b[s+1:f],16))
                elif(i!=len(b)-1):
                    s=i
                    l.append(ord(b[i]))
            b=l
        if(type(b)==list_):
            b=list(b)
        if(type(b)==list):
            i=0
            while i<len(b):
                b[i]=int(b[i])
                if(b[i]>255):
                    n=b.pop(i)
                    while n>0:
                        b.insert(i,n%256)
                        n=n//256
                i+=1
        self.b=bytes(b)
    def __str__(self):
        s="'"
        for i in range(len(self.b)):
            s=s+'\\'+'0'*(1-int(self.b[i])//16)+hex(int(self.b[i]))[2:].upper()
        return s+"'"
    def __bytes__(self):
        return self.b
    def __eq__(self,other):
        return self.b==other.b
    def __hash__(self):
        return hash(self.b)
class str_(value_):
    def __init__(self,s):
        if(type(s)==str_):
            s=str(s)[1:-1]
        self.s=str(s)
    def __str__(self):
        return '"'+self.s+'"'
    def __eq__(self,other):
        return self.s==other.s
    def __hash__(self):
        return hash(self.s)
class list_(value_):
    def __init__(self,l):
        if(type(l)==str_):
            l=str(l)[1:-1]
        if(type(l)==str):
            nl,r=[],0
            s,f=0,0
            while l.count(", ")+l.count(" ,")+l.count("[ ")+l.count(" ]")>0:
                l=l.replace(", ", ",")
                l=l.replace(" ,", ",")
                l=l.replace("[ ", "[")
                l=l.replace(" ]", "]")
            for i in range(len(l)):
                if(l[i]=="["):
                    r+=1
                elif((l[i]=="," or l[i]=="]") and r==1):
                    s=f
                    f=i
                    nl.append(value(l[s+1:f]))
                elif(l[i]=="]"):
                    r-=1
            l=nl
        if(type(l)==list):
            for i in range(len(l)):
                l[i]=value(l[i])
        self.l=list(l)
        self.i=0
    def __str__(self):
        s="["
        for i in self.l:
            s=s+str(i)+", "
        return s[:-2]+"]"
    def __iter__(self):
        self.i=0
        return self
    def __next__(self):
        if self.i<len(self.l):
            res=self.l[self.i]
            self.i+=1
            return res
        else:
            raise StopIteration
    def __len__(self):
        return len(self.l)
    def __getitem__(self,i):
        return self.l[i]
    def __setitem__(self,i,v):
        self.l[i]=v
    def pop(self,i):
        return self.l.pop(int(i))
    def insert(self,i,v):
        self.l.insert(int(i),v)
    def __eq__(self,other):
        return self.l==other.l
class dict_(value_):
    def __init__(self,d):
        if(type(d)==str_):
            d=str(d)[1:-1]
        if(type(d)==str):
            l,r=[],0
            s,m,f=0,0,0
            while d.count(", ")+d.count(" ,")+d.count("[ ")+d.count(" ]")>0:
                d=d.replace(", ", ",")
                d=d.replace(" ,", ",")
                d=d.replace("[ ", "[")
                d=d.replace(" ]", "]")
            for i in range(len(d)):
                if(d[i]=="["):
                    r+=1
                elif(d[i]==":" and r==1):
                    m=i
                elif((d[i]=="," or d[i]=="]") and r==1):
                    s=f
                    f=i
                    l.append((value(d[s+1:m]),value(d[m+1:f])))
                elif(d[i]=="]"):
                    r-=1
            d=dict(l)
        if(type(d)==dict):
            nd={}
            for k,i in d.items():
                nd[value(k)]=value(i)
            d=nd
        self.d=dict(d)
        self.i=0
    def __str__(self):
        s="["
        for k,i in self.d.items():
            s=s+str(k)+":"+str(i)+", "
        return s[:-2]+"]"
    def __iter__(self):
        self.i=0
        return self
    def __next__(self):
        if self.i<len(self.d):
            key=list(self.d.keys())[self.i]
            self.i+=1
            return (key,self.d[key])
        else:
            raise StopIteration
    def __len__(self):
        return len(self.d)
    def __getitem__(self,k):
        return self.d[k]
    def __setitem__(self,k,v):
        self.d[k]=v
    def pop(self,k):
        buffer=self.d[k]
        del self.d[k]
        return buffer
    def insert(self,k,v):
        self.d[k]=v
    def __eq__(self,other):
        return self.d==other.d
class function_(value_):
    def __init__(self):
        pass
    def __str__(self):
        pass
    def __eq__(self,other):
        return self.f==other.f
    def do(self):
        pass
class type_(value_):
    def __init__(self,t):
        if(type(t)==str_):
            t=str(t)[1:-1]
        if(type(t)==str):
            try:
                valueTypes={"[none]":none_,"[num]":num_,"[bool]":bool_,"[bytes]":bytes_,"[str]":str_,
                            "[list]":list_,"[dict]":dict_,"[function]":function_,"[type]":type_,"[error]":error_}
                t=valueTypes[t]
            except KeyError:
                raise ValueError
        if(type(t)!=type):
            t=type(t)
        if(issubclass(t,value_)):
            self.t=t
        else:
            raise TypeError
    def __str__(self):
        return '['+str(self.t)[19:-3]+']'
    def __eq__(self,other):
        return self.t==other.t
    def __hash__(self):
        return hash(self.t)
class error_(value_):
    def __init__(self,code=0):
        if(type(code)==str_):
            code=str(code)[1:-1]
        if(type(code)==str):
            code=int(code[1:-1])
        if(type(code)==type and set([code])-set(errorCodes.keys())==set()):
            try:
                code=errorCodes[code]
            except KeyError:
                code=0
        if(0<=int(code) and int(code)<=7):
            self.code=int(code)
        elif(int(code)==8):
            exit()
        else:
            raise ValueError
    def __str__(self):
        return "{"+str(self.code)+"}"
    def __eq__(self,other):
        return self.code==other.code
    def __hash__(self):
        return hash(self.code)