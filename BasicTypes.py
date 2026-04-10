from cmath import phase,isnan,isinf
from math import log,pi
errorCodes={Exception:9,TypeError:1,ValueError:2,IndexError:3,KeyError:4,SyntaxError:5,ArithmeticError:6,RecursionError:7,SystemExit:8}
constants={"π":3.1415926535897932,"e":2.7182818284590452,"i":1j,"∞":complex('inf'),"∅":complex('nan')}
signatureNumber={'0','1','2','3','4','5','6','7','8','9','+','-','i','n','∞','∅'}
priorityOfOperations={"+":1,"-":1,"*":2,"/":2,"↧":3,"^":4,"√":4,"E":5,"~":6}
def is_number(s):
    if(s==""):
        return False
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
        defaultValue={"+":(0,0),"-":(0,0),"*":(1,1),"/":(1,1),"↧":(constants["e"],1),"^":(2,1),"√":(2,1),"E":(1,0),"~":(-1,-1)}
        operations={"+":lambda a,b:a+b,"-":lambda a,b:a-b,"*":lambda a,b:a*b,"/":lambda a,b:a/b,"↧":lambda a,b:a.Ln()/b.Ln(),
                    "^":lambda a,b:a**b,"√":lambda a,b:b**(num_(1)/a),"E":lambda a,b:a*num_(10)**b,"~":lambda a,b:a*b,
                    "n":lambda a:num_(a),"c":lambda a:num_(constants[a]),"d":lambda d:num_(defaultValue[d[0]][d[1]])}
        if(set([self.op])-set(operations.keys())==set()):
            if(set([self.op])-set(priorityOfOperations.keys())==set()):
#                 print(self.op,self.left,self.right,self.value,operations[self.op](self.left.count(),self.right.count()))
                return operations[self.op](self.left.count(),self.right.count())
            return operations[self.op](self.value)
    def __str__(self):
        return f"({str(self.op)};{str(self.left)};{str(self.right)};{str(self.value)})"
def value(v,s=None):
    if(type(v)==str):
        if(v[:1]=="⟨"):
            v=Sequence(v,s)
        elif(v.lower()=="none"):
            v=none_(v)
        elif(v.lower()=="true" or v.lower()=="false"):
            v=bool_(v)
        elif(v[:1]=='"'):
            v=str_(v[1:-1])
        elif(v[:1]=="'"):
            v=bytes_(v)
        elif(v[:1]=='(' and v.count("→")+v.count("⇀")+v.count("⇁")>0):
            v=function_(v,s)
        elif(v[:1]=='{'):
            if(v.count('(')>0):
                v=function_(v,s)
            else:
                v=error_(v)
        elif(v[:1]=='['):
            if(set([v])-{"[none]","[num]","[bool]","[bytes]","[str]","[list]","[dict]","[function]","[type]","[error]"}==set()):
                v=type_(v)
            else:
                for i in range(1,len(v)):
                    if(v[i]==':'):
                        v=dict_(v,s)
                        break
                    elif(v[i]==',' or v[i]=='['):
                        v=list_(v,s)
                        break
        elif(set([v[:1]])-(signatureNumber|{'('})==set()):
            v=num_(v)
    try:
        if(type(v)==type and set([v])-set(errorCodes.keys())==set()):
            v=error_(v)
        else:
            baseValueTypes={type(None):none_,int:num_,float:num_,complex:num_,bool:bool_,bytes:bytes_,str:str_,list:list_,dict:dict_,type:type_}
            v=baseValueTypes[type(v)](v,s)
    except KeyError:
        pass
    if(issubclass(type(v),value_) or type(v)==Sequence):
        return v
    else:
        raise ValueError
class Code():
    def __init__(self,c,s,b=0,ef=(lambda:None)):
#         print(f"{c} , {s} , {b} , {ef}")
        functions={"+":s.plus,"-":s.minus,"*":s.mult,"/":s.div,"^":s.exp,"↧":s.log,"↕":s.abs,"o":s.round,"R":s.random,
                   "s":s.sin,"c":s.cos,"t":s.tan,"S":s.arcsin,"C":s.arccos,"T":s.arctan,"=":s.eq,"<":s.lt,">":s.gt,
                   "¬":s.not_,"⋀":s.and_,"∨":s.or_,"⊕":s.xor,"w":s.write,"f":s.find,"a":s.append,"d":s.delete,
                   "r":s.read,"l":s.len,"u":s.substring,"&":s.concatenate,"@":s.push,"D":s.pop,"$":s.copy,"L":s.size,
                   "%":s.Bswap,"‰":s.Tswap,"↑":s.moveUp,"↓":s.moveDown,"p":s.print,"e":s.enter,"№":s.addNamedFun,
                   "§":s.doNamedFun,"!":s.doFun,"?":s.type,"F":s.format,"↪":lambda:"break"}
        code=[]
        p=["",False,'']
        f=["",False,0]
        r={'"':0,"'":0,"[":0,"{":0,"(":0,"⟨":0}
        for i in range(len(c)):
            l=c[(i+b)%len(c)]
#             print(l,r,p,f)
            if(p[1]):
                if(set([l])-{"[","{","(","⟨"}==set() or (l=='"' and r['"']==0) or (l=="'" and r["'"]==0)):
                    r[l]+=1
                elif(set([l])-{'"',"'","]","}",")","⟩"}==set()):
                    r[l.replace("]","[").replace("}","{").replace(")","(").replace("⟩","⟨")]-=1
                if((p[2]=='"' and l=='"' and r['"']==0) or (p[2]=="'" and l=="'" and r["'"]==0) or (p[2]=='[' and l==']' and r['[']==0) or (p[2]=='{' and (l=='}' or l==')') and r['{']==0 and c[(i+b+1)%len(c)]!='(') or (p[2]=='⟨' and l=='⟩' and r['⟨']==0) or (p[2]=='(' and (l==')' or l=='}') and r['(']==0 and c[(i+b+1)%len(c)]!='{') or (set([p[2]])-signatureNumber==set() and set([l])-(signatureNumber|{'E','.','~','j','f','a'})!=set()) or ((p[2]=='n' or p[2]=='t' or p[2]=='f') and l==' ') or (i==len(c)-1) or (set([p[2]])-{'"',"'","[","{","(","⟨"}!=set() and l=="@")):
                    if(l!=' ' and l!='→' and l!='⇀' and l!='⇁' and l!='@'):
                        p[0]=p[0]+l
                    code.append(lambda s=s,d=value(p[0],s): s.push(d))
                    r={'"':0,"'":0,"[":0,"{":0,"(":0,"⟨":0}
                    if(l=="@"):
                        p=["",True,c[(i+b+1)%len(c)].lower()]
                    else:
                        p=["",False,'']
                else:
                    p[0]=p[0]+l
            elif(f[1]):
                f[0]=f[0]+l
                if(l=="(" or l=="{"):
                    f[2]+=1
                elif(l==")" or l=="}"):
                    f[2]-=1
                if(f[2]==0 and ((f[0][0]=="{" and l==")") or (f[0][0]=="(" and l=="}") or (f[0][0]=="(" and l==")" and c[(i+b+1)%len(c)]!="{"))):
                    code.append(lambda foo=function_(f[0],s): foo.do())
                    f=["",False,0]
            elif(l==" " or l=="	" or l=="→" or l=="⇀" or l=="⇁" or l=="#"):
                pass
            elif(l=="@"):
                p[1]=True
                p[2]=c[(i+b+1)%len(c)].lower()
            elif(l=="{" or l=="("):
                f=[l,True,1]
            elif(set([l])-set(functions.keys())==set()):
                code.append(functions[l])
            else:
                raise SyntaxError(f"unknown commands {l}")
        code.append(ef)
#         print(code)
        self.code=code
        self.Stack=s
    def do(self):
        try:
            for i in range(len(self.code)):
                try:
                    if(self.code[i]()=="break"):
                        return "break"
#                     print(i,self.code[i],self.Stack)
                except TypeError:
                    self.Stack.push(error_(1))
                except ValueError:
                    self.Stack.push(error_(2))
                except IndexError:
                    self.Stack.push(error_(3))
                except KeyError:
                    self.Stack.push(error_(4))
                except SyntaxError:
                    self.Stack.push(error_(5))
                except ArithmeticError:
                    self.Stack.push(error_(6))
        except RecursionError:
            self.Stack.push(error_(7))
    def __str__(self):
        return str(self.code)
class Sequence():
    def __init__(self,l,s=None):
        if(type(l)==str_):
            l=str(l)[1:-1]
        if(type(l)==str):
            nl,r=[],0
            b,e=0,0
            if(l=="⟨⟩" or l==""):
                l=list()
            else:
                i=0
                while i<len(l):
                    if(set([l[i]])-{"[","{","(","⟨"}==set() or (l[i]=='"' and r==1) or (l[i]=="'" and r==1)):
                        r+=1
                    elif((l[i]==" " or l[i]=="	") and r==1):
                        b1,j=i,i+1
                        while j<len(l) and (l[j]==" " or l[j]=="	"):
                            j+=1
                        if(j-b1>0):
                            i-=1
                            l=l[:b1]+l[j:]
                    elif((l[i]==";" or l[i]=="⟩") and r==1):
                        b=e
                        e=i
                        nl.append(value(l[b+1:e],s))
                    elif(set([l[i]])-{'"',"'","]","}",")","⟩"}==set()):
                        r-=1
                    i+=1
                l=nl
        if(type(l)==list):
            for i in range(len(l)):
                l[i]=value(l[i],s)
        if(type(l)!=list):
            l=[l,]
        self.s=list(l)
        self.i=0
    def __str__(self):
        if(self.s==list()):
            return "⟨⟩"
        s="⟨"
        for i in self.s:
            s=s+str(i)+"; "
        return s[:-2]+"⟩"
    def __iter__(self):
        self.i=0
        return self
    def __next__(self):
        if self.i<len(self.s):
            res=self.s[self.i]
            self.i+=1
            return res
        else:
            raise StopIteration
    def __len__(self):
        return len(self.s)
    def __getitem__(self,i):
        return self.s[i]
    def __eq__(self,other):
        if(type(self)==type(other)):
            return self.s==other.s
        return False
class value_():
    def __init__(self,v,s=None):
        self.v=v
    def __str__(self):
        return str(self.v)
    def __eq__(self,other):
        if(type(self)==type(other)):
            return self.v==other.v
        return False
class none_(value_):
    def __init__(self,v=None,s=None):
        pass
    def __str__(self):
        return "None"
    def __eq__(self,other):
        return type(self)==type(other)
    def __hash__(self):
        return hash(None)
class num_(value_):
    def __init__(self,n,s=None):
#         print(n)
        if(type(n)==str_):
            n=str(n)[1:-1]
        if(type(n)==str):
            if(n[:1]=='('):
                n=num_(ExpressionTreeNode(n[1:-1]).count())
            elif(n==""):
                n=0
            else:
                n=n.replace('∞','inf').replace('∅','nan').replace('~i','j')
        try:
            if(isinf(complex(n)) or isnan(complex(n)) or abs(complex(n))==0):
                n=abs(complex(n))
        except ValueError:
            raise ValueError
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
        if(type(self)==type(other)):
            if(isnan(self.n) and isnan(other.n)):
                return True
            return self.n==other.n
        return False
    def __hash__(self):
        return hash(self.n)
    def __round__(self,n):
        if(type(n)==int):
            self.n=complex(round(self.n.real,n),round(self.n.imag,n))
            return self
        raise ValueError
    def __neg__(self):
        return num_(-self.n)
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
    def __init__(self,b,s=None):
        if(type(b)==str_):
            b=str(b)[1:-1]
        if(type(b)==str):
            if(b.lower()=="true" or b.lower()=="t"):
                b=True
            elif(b.lower()=="false" or b.lower()=="f"):
                b=False
        if(type(b)==int):
            if(b==1):
                b=True
            elif(b==0):
                b=False
        self.b=bool(b)
    def __str__(self):
        if(self.b):
            return "True"
        return "False"
    def __bool__(self):
        return self.b
    def __eq__(self,other):
        if(type(self)==type(other)):
            return self.b==other.b
        return False
    def __hash__(self):
        return hash(self.b)
class bytes_(value_):
    def __init__(self,b,s=None):
        if(type(b)==str_):
            b=str(b)[1:-1]
        if(type(b)==str):
            l=[]
            s,e=1,1
            for i in range(1,len(b)):
                if(b[s]=='\\'):
                    if((b[i]=="\\" or b[i]=="'") and i>1):
                        s=e
                        e=i
                        l.append(int(b[s+1:e],16))
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
        if(type(self)==type(other)):
            return self.b==other.b
        return False
    def __len__(self):
        return len(self.b)
    def __getitem__(self,i):
        return self.b[i]
    def __setitem__(self,i,v):
        self.b=self.b[:int(i)]+bytes(v)+self.b[int(i)+1:]
    def pop(self,i):
        buffer=self.b[int(i)]
        self.b=self.b[:int(i)]+self.b[int(i)+1:]
        return buffer
    def __hash__(self):
        return hash(self.b)
    def __add__(self,other):
        return bytes_(self.b+other.b)
    def sub(self,s,f):
        return bytes_(self.b[int(s):int(f)])
    def find(self,v):
        return self.b.find(bytes(v))
class str_(value_):
    def __init__(self,s,st=None):
        if(type(s)==str_):
            s=str(s)[1:-1]
        self.s=str(s)
    def __str__(self):
        return '"'+self.s+'"'
    def __eq__(self,other):
        if(type(self)==type(other)):
            return self.s==other.s
        return False
    def __len__(self):
        return len(self.s)
    def __getitem__(self,i):
        return self.s[i]
    def __setitem__(self,i,v):
        if(type(v)==type(self)):
            v=str(v)[1:-1]
        self.s=self.s[:int(i)]+v+self.s[int(i)+1:]
    def pop(self,i):
        buffer=self.s[int(i)]
        self.s=self.s[:int(i)]+self.s[int(i)+1:]
        return buffer
    def __hash__(self):
        return hash(self.s)
    def __add__(self,other):
        return str_(self.s+other.s)
    def sub(self,s,f):
        return str_(self.s[int(s):int(f)])
    def find(self,v):
        if(type(v)==type(self)):
            v=str(v)[1:-1]
        return self.s.find(str(v))
class list_(value_):
    def __init__(self,l,s=None):
        if(type(l)==str_):
            l=str(l)[1:-1]
        if(type(l)==str):
            nl,r=[],0
            b,e=0,0
            if(l=="[]" or l==""):
                l=list()
            else:
                i=0
                while i<len(l):
                    if(set([l[i]])-{"[","{","(","⟨"}==set() or (l[i]=='"' and r==1) or (l[i]=="'" and r==1)):
                        r+=1
                    elif((l[i]==" " or l[i]=="	") and r==1):
                        b1,j=i,i+1
                        while j<len(l) and (l[j]==" " or l[j]=="	"):
                            j+=1
                        if(j-b1>0):
                            i-=1
                            l=l[:b1]+l[j:]
                    elif((l[i]=="," or l[i]=="]") and r==1):
                        b=e
                        e=i
                        nl.append(value(l[b+1:e],s))
                    elif(set([l[i]])-{'"',"'","]","}",")","⟩"}==set()):
                        r-=1
                    i+=1
                l=nl
        if(type(l)==list):
            for i in range(len(l)):
                l[i]=value(l[i],s)
        if(type(l)!=list):
            l=[l,]
        self.l=list(l)
        self.i=0
    def __str__(self):
        if(self.l==list()):
            return "[]"
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
        self.l[int(i)]=v
    def pop(self,i):
        return self.l.pop(int(i))
    def insert(self,i,v):
        self.l.insert(int(i),v)
    def __eq__(self,other):
        if(type(self)==type(other)):
            return self.l==other.l
        return False
    def __add__(self,other):
        return list_(self.l+other.l)
    def sub(self,s,f):
        return list_(self.l[int(s):int(f)])
    def find(self,v):
        try:
            return self.l.index(v)
        except ValueError:
            return num_(-1)
class dict_(value_):
    def __init__(self,d,s=None):
        if(type(d)==str_):
            d=str(d)[1:-1]
        if(type(d)==str):
            l,r=[],0
            b,m,e=0,0,0
            if(d=="[]" or d==""):
                d=dict()
            else:
                i=0
                while i<len(d):
                    if(set([d[i]])-{"[","{","(","⟨"}==set() or (d[i]=='"' and r==1) or (d[i]=="'" and r==1)):
                        r+=1
                    elif((d[i]==" " or d[i]=="	") and r==1):
                        b1,j=i,i+1
                        while j<len(d) and (d[j]==" " or d[j]=="	"):
                            j+=1
                        if(j-b1>0):
                            i-=1
                            d=d[:b1]+d[j:]
                    elif(d[i]==":" and r==1):
                        m=i
                    elif((d[i]=="," or d[i]=="]") and r==1):
                        b=e
                        e=i
                        l.append((value(d[b+1:m]),value(d[m+1:e],s)))
                    elif(set([d[i]])-{'"',"'","]","}",")","⟩"}==set()):
                        r-=1
                    i+=1
                d=dict(l)
        if(type(d)==dict):
            nd={}
            for k,i in d.items():
                nd[value(k)]=value(i,s)
            d=nd
        self.d=dict(d)
        self.i=0
    def __str__(self):
        if(self.d==dict()):
            return "[]"
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
        if(type(self)==type(other)):
            return self.d==other.d
        return False
    def __add__(self,other):
        for k,i in other.d.items():
            self.d[k]=i
        return self
    def find(self,fv):
        return (lambda l: l[0] if len(l)>0 else num_(-1))([k for k,v in self.d.items() if v==fv])
class function_(value_):
    def __init__(self,f,s):
#         print(f,s)
        if(type(f)==str_):
            f=str(f)[1:-1]
        if(type(f)==str):
            wb,we,ob,oe,om,os,si,st,se=None,None,None,None,None,None,None,None,None
            i,r1,r2,r3,r4,r5=0,0,0,0,0,0
            while i<len(f):
                if(f[i]=='"' and r5==0):
                    if(r4==0):
                        r4+=1
                    else:
                        r4-=1
                elif(f[i]=="'" and r4==0):
                    if(r5==0):
                        r5+=1
                    else:
                        r5-=1
                elif(f[i]=="(" and r4+r5==0):
                    r1+=1
                    if(r1+r2==1):
                        ob=i
                elif(f[i]=="{" and r4+r5==0):
                    r2+=1
                    if(r1+r2==1):
                        wb=i
                elif(f[i]=="[" and r4+r5==0):
                    r3+=1
                elif(f[i]==")" and r4+r5==0):
                    r1-=1
                    if(r1+r2==0):
                        oe=i
                elif(f[i]=="}" and r4+r5==0):
                    r2-=1
                    if(r1+r2==0):
                        we=i
                elif(f[i]=="]" and r4+r5==0):
                    r3-=1
                elif(f[i]=="|" and r4+r5==0):
                    if(r1+r2==1):
                        om=i
                elif(f[i]=="→" and r4+r5==0):
                    if(r1==1 and r2==0):
                        os=i
                    elif(r2==1 and r1==0):
                        si=i
                elif(f[i]=="⇀" and r4+r5==0):
                    if(r1+r2==1):
                        st=i
                elif(f[i]=="⇁" and r4+r5==0):
                    if(r1+r2==1):
                        se=i
                elif((f[i]==" " or f[i]=="	") and r4+r5==0):
                    b,j=i+1,i+1
                    while j<len(f) and (f[j]==" " or f[j]=="	"):
                        j+=1
                    if(j-b>0):
                        f=f[:b]+f[j:]
                i+=1
#             print(f"{{ - {wb}, }} - {we}, ( - {ob}, ) - {oe}, | - {om}, (→) - {os}, {{→}} - {si}, ⇀ - {st}, ⇁ - {se}, len - {i}, () - {r1}, {{}} - {r2}, [] - {r3}, \"\" - {r4}, '' - {r5}")
            if(r1+r2+r3+r4+r5!=0):
                raise SyntaxError(f"the number of open parentheses is not equal to the number of closed parentheses. Parentheses balance: () {r1}; {{}} {r2}; [] {r3}; \"\" {r4}; \'\' {r5}")
            if(wb!=None and we!=None):
                If=f[wb+1:we]
            else:
                If=""
            if(om==None):
                Then=f[ob+1:oe]
                Else=""
            else:
                Then=f[ob+1:om]
                Else=f[om+1:oe]
            if(os!=None and om!=None and os>om or st!=None and om!=None and st>om):
                Then,Else=Else,Then
                ob,om=om,ob
#             print(f'"{If}" , "{Then}" , "{Else}"')
            if(os!=None and ob!=None):
                if(If==""):
#                     print(1.1)
                    Then=Code(Then,s,os-ob)
                    t="function"
                else:
#                     print(1.2)
                    Then=Code(Then,s,os-ob,lambda foo=self: foo.If.do())
                    t="while"
            elif(st!=None and ob!=None):
#                 print(1.3)
                Then=Code(Then,s,st-ob)
                t="if"
            else:
#                 print(1.4)
                Then=Code(Then,s)
                if(If=="" or se==None):
                    t="undefined"
                else:
                    t="if"
            if(se!=None and om!=None):
#                 print(2.1)
                Else=Code(Else,s,se-om)
            else:
#                 print(2.2)
                Else=Code(Else,s)
            if(si!=None and wb!=None):
                if(If==""):
#                     print(3.1)
                    If=Code(If,s,si-wb,lambda foo=self: foo.Then.do())
                else:
#                     print(3.2)
                    If=Code(If,s,si-wb,lambda s=s,foo=self: foo.Then.do() if (lambda s=s:bool(s.pop()) if (type(s.stack[-1])==bool_ or type(s.stack[-1])==bool) else s.push(error_(1)))(s) else foo.Else.do())
            else:
                if(If==""):
#                     print(3.3)
                    If=Code(If,s,0,lambda foo=self: foo.Then.do())
                else:
#                     print(3.4)
                    If=Code(If,s,0,lambda s=s,foo=self: foo.Then.do() if (lambda s=s:bool(s.pop()) if (type(s.stack[-1])==bool_ or type(s.stack[-1])==bool) else s.push(error_(1)))(s) else foo.Else.do())
#             print(f,t)
            self.If=If
            self.Then=Then
            self.Else=Else
            self.text=str(f)
            self.type=str(t)
        elif(type(f)==function_):
            return f
        else:
            raise TypeError
        
    def __str__(self):
        return self.text
    def __eq__(self,other):
        if(type(self)==type(other)):
            return self.f==other.f
        return False
    def do(self):
        if(self.If.do()=="break" and self.type=="if"):
            return "break"
class type_(value_):
    def __init__(self,t,s=None):
        if(type(t)==str_):
            t=str(t)[1:-1]
        if(type(t)==str):
            try:
                valueTypes={"[none]":none_,"[num]":num_,"[bool]":bool_,"[bytes]":bytes_,"[str]":str_,
                            "[list]":list_,"[dict]":dict_,"[function]":function_,"[type]":type_,"[error]":error_}
                t=valueTypes[t]
            except KeyError:
                if(t=="[]" or t==""):
                    self.t=None
                    return
                else:
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
        if(type(self)==type(other)):
            return self.t==other.t
        return False
    def __hash__(self):
        return hash(self.t)
class error_(value_):
    def __init__(self,code=0,s=None):
        if(type(code)==str_):
            code=str(code)[1:-1]
        if(type(code)==str):
            try:
                code=int(code[1:-1])
            except ValueError:
                code=0
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
        if(type(self)==type(other)):
            return self.code==other.code
        return False
    def __hash__(self):
        return hash(self.code)