from cmath import phase,isnan,isinf
from math import log,pi
errorCodes={TypeError:1,ValueError:2,IndexError:3,KeyError:4,SyntaxError:5,ArithmeticError:6,RecursionError:7,Exception:8,SystemExit:9}
constants={"π":3.1415926535897932,"e":2.7182818284590452,"i":1j,"∞":float('inf'),"∅":float('nan')}
signatureNumber={'0','1','2','3','4','5','6','7','8','9','.','E','+','-','i','∞','∅'}
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
def value(v,s=None,ds=False):
    if(type(v)==str):
        if(ds):
            i,q1,q2=0,0,0
            substitutionTable={"#<":"⟨","#>":"⟩","#l":"↧","#r":"√","pi":"π"}
            while i<len(v):
                if(q2%2==0 and v[i]=='"' and i>1 and (v[i-1]!='\\' or v[i-2]=='\\')):
                    q1+=1
                elif(q1%2==0 and v[i]=="'"):
                    q2+=1
                elif((q1+q2)%2==0 and set([v[i:i+2]])-set(substitutionTable.keys())==set()):
                    v=v[:i]+substitutionTable[v[i:i+2]]+v[i+2:]
                i+=1
        if(v[:1]=="⟨"):
            v=Sequence(v,s)
        elif(v.lower()=="none" or v==""):
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
        elif(set([v[:1]])-(signatureNumber|{'(','n'})==set()):
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
class Sequence():
    def __init__(self,l,s=None):
        if(type(l)==str_):
            l=str(l)[1:-1]
        if(type(l)==str):
            nl,r,q1,q2=[],0,0,0
            b,e=0,0
            if(l=="⟨⟩" or l==""):
                l=list()
            else:
                i=0
                while i<len(l):
                    if(set([l[i]])-{"[","{","(","⟨"}==set() or (l[i]=='"' and r==1) or (l[i]=="'" and r==1)):
                        r+=1
                        if(l[i]=='"'):
                            q1+=1
                        if(l[i]=="'"):
                            q2+=1
                    elif((l[i]==" " or l[i]=="\t") and r==1):
                        b1,j=i,i+1
                        while j<len(l) and (l[j]==" " or l[j]=="\t"):
                            j+=1
                        if(j-b1>0):
                            i-=1
                            l=l[:b1]+l[j:]
                    elif((l[i]==";" or l[i]=="⟩") and r==1):
                        b=e
                        e=i
                        nl.append(value(l[b+1:e],s))
                    elif(set([l[i]])-{"]","}",")","⟩"}==set() or (q1==1 and l[i]=='"' and i>1 and (l[i-1]!='\\' or l[i-2]=='\\')) or (q2==1 and l[i]=="'")):
                        r-=1
                        if(l[i]=='"'):
                            q1-=1
                        if(l[i]=="'"):
                            q2-=1
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
    def __setitem__(self,i,v):
        self.s[int(i)]=v
    def pop(self,i):
        return self.s.pop(int(i))
    def insert(self,i,v):
        self.s.insert(int(i),v)
    def __eq__(self,other):
        if(type(self)==type(other)):
            return self.s==other.s
        return False
    def __add__(self,other):
        return list_(self.s+other.s)
    def sub(self,s,f):
        return list_(self.s[int(s):int(f)])
    def find(self,v):
        try:
            return self.s.index(v)
        except ValueError:
            return num_(-1)
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
        if(type(n)==str_):
            n=str(n)[1:-1]
        if(type(n)==str):
            if(n[:1]=='('):
                n=num_(ExpressionTreeNode(n[1:-1]).count())
            elif(n==""):
                n=0
            else:
                n=n.replace('∞','inf').replace('∅','nan').replace('i','j').replace('jnf','inf')
        try:
            if(isnan(complex(n))):
                n=complex('nan')
            elif(isinf(complex(n))):
                n=complex('inf')
        except ValueError:
            raise ValueError("This data cannot be converted to a number")
        self.n=complex(n) #оптимізувати щоб був int, float чи complex в залежності від числа
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
            return i+'i'
        else:
            r=str(self.n.real).replace('e','E')
            i=str(self.n.imag).replace('e','E')
            if(float(r)%1==0):
                r=r.replace('.0','')
            if(float(i)%1==0):
                i=i.replace('.0','')
            if(float(i)>=0):
                i='+'+i
            return r+i+'i'
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
        if(type(b)==num_):
            b=int(b)
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
        self.s=str(s).replace('\\n','\n').replace('\\t','\t').replace('\\"','\"').replace('\\\\','\\')
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
        if(type(l)==list):
            for i in range(len(l)):
                l[i]=value(l[i],s)
        if(type(l)==str_):
            l=str(l)[1:-1]
        if(type(l)==str):
            nl,r,q1,q2=[],0,0,0
            b,e=0,0
            if(l=="[]" or l==""):
                l=list()
            else:
                i=0
                while i<len(l):
                    if(set([l[i]])-{"[","{","(","⟨"}==set() or (l[i]=='"' and r==1) or (l[i]=="'" and r==1)):
                        r+=1
                        if(l[i]=='"'):
                            q1+=1
                        if(l[i]=="'"):
                            q2+=1
                    elif((l[i]==" " or l[i]=="\t") and r==1):
                        b1,j=i,i+1
                        while j<len(l) and (l[j]==" " or l[j]=="\t"):
                            j+=1
                        if(j-b1>0):
                            i-=1
                            l=l[:b1]+l[j:]
                    elif((l[i]=="," or l[i]=="]") and r==1):
                        b=e
                        e=i
                        nl.append(value(l[b+1:e],s))
                    elif(set([l[i]])-{"]","}",")","⟩"}==set() or (q1==1 and l[i]=='"' and i>1 and (l[i-1]!='\\' or l[i-2]=='\\')) or (q2==1 and l[i]=="'")):
                        r-=1
                        if(l[i]=='"'):
                            q1-=1
                        if(l[i]=="'"):
                            q2-=1
                    i+=1
                l=nl
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
            l,r,q1,q2=[],0,0,0
            b,m,e=0,0,0
            if(d=="[]" or d==""):
                d=dict()
            else:
                i=0
                while i<len(d):
                    if(set([d[i]])-{"[","{","(","⟨"}==set() or (d[i]=='"' and r==1) or (d[i]=="'" and r==1)):
                        r+=1
                        if(d[i]=='"'):
                            q1+=1
                        if(d[i]=="'"):
                            q2+=1
                    elif((d[i]==" " or d[i]=="\t") and r==1):
                        b1,j=i,i+1
                        while j<len(d) and (d[j]==" " or d[j]=="\t"):
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
                    elif(set([d[i]])-{"]","}",")","⟩"}==set() or (q1==1 and d[i]=='"' and i>1 and (d[i-1]!='\\' or d[i-2]=='\\')) or (q2==1 and d[i]=="'")):
                        r-=1
                        if(d[i]=='"'):
                            q1-=1
                        if(d[i]=="'"):
                            q2-=1
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
    def __init__(self,code,stack):
#         print(0,code)
        functions={"+":stack.plus,"-":stack.minus,"*":stack.mult,"/":stack.div,"^":stack.pow,"↧":stack.log,"↕":stack.abs,
                   "o":stack.round,"R":stack.random,"s":stack.sin,"c":stack.cos,"t":stack.tan,"S":stack.arcsin,"C":stack.arccos,
                   "T":stack.arctan,"=":stack.eq,"<":stack.lt,">":stack.gt,"¬":stack.not_,"∧":stack.and_,"∨":stack.or_,
                   "⊕":stack.xor,"w":stack.write,"f":stack.find,"a":stack.append,"d":stack.delete,"r":stack.read,"l":stack.len,
                   "u":stack.substring,"&":stack.concatenate,"@":stack.push,"D":stack.pop,"$":stack.copy,"L":stack.size,
                   "%":stack.Bswap,"‰":stack.Tswap,"↑":stack.moveUp,"↓":stack.moveDown,"p":stack.print,"e":stack.enter,
                   "№":stack.addNamedFun,"§":stack.doNamedFun,"!":stack.doFun,"?":stack.type,"F":stack.format,"_":lambda:None}
        substitutionTable={"#l":"↧","#m":"↕","#n":"¬","#a":"∧","#o":"∨","#x":"⊕","#%":"‰","#u":"↑","#d":"↓","#N":"№",
                           "#F":"§","#f":"→","#t":"⇀","#e":"⇁","#b":"↪","#<":"⟨","#>":"⟩","#r":"√","pi":"π"}
        i=0
        q1=0
        q2=0
        while i<len(code):
            if(q2%2==0 and code[i]=='"' and i>1 and (code[i-1]!='\\' or code[i-2]=='\\')):
                q1+=1
            elif(q1%2==0 and code[i]=="'"):
                q2+=1
            elif((q1+q2)%2==0 and set([code[i:i+2]])-set(substitutionTable.keys())==set()):
                code=code[:i]+substitutionTable[code[i:i+2]]+code[i+2:]
            i+=1
#         print(1,code)
        i=0
        b=0
        token=""
        tokens=[]
        brackets={'"':'"',"'":"'","(":")","{":"}","[":"]","⟨":"⟩"}
        markSymbols={"→","⇀","⇁","{","}","(","|",")"}
        marks=[]
        parts=[]
        while i<len(code):
            if(token=="" and set([code[i]])-(set(functions.keys())|markSymbols|{"↪"})==set()):
                token=code[i]
                if(code[i]=="@"):
                    if(code[i+1:i+5].lower()=="none"):
                        token+=code[i+1:i+5]
                        i+=5
                    elif(code[i+1:i+5].lower()=="true"):
                        token+=code[i+1:i+5]
                        i+=5
                    elif(code[i+1:i+6].lower()=="false"):
                        token+=code[i+1:i+6]
                        i+=6
                    elif(set([code[i+1:i+2]])-signatureNumber==set()):
                        token+=code[i+1]
                        i+=2
                    elif(set([code[i+1:i+2]])-set(brackets.keys())==set()):
                        token+=code[i+1]
                        i+=1
            elif(token[0:1]!="@" and code[i]!=" " and code[i]!="\t" and code[i]!="\n"):
                raise SyntaxError(f"unknown commands {code[i]}")
            if(token[0:1]=="@"):
                if(b>0 or set([code[i],token[1:2]])-(signatureNumber|{'a','n','f'})==set()):
                    token+=code[i]
                if(set([code[i],token[1:2]])-((set(brackets.keys())|set(brackets.values()))-{'"'})==set() or (token[1:2]=='"' and code[i]=='"' and i>1 and (code[i-1]!='\\' or code[i-2]=='\\'))):
                    if(code[i]==token[1:2] and not((token[1:2]=='"' or token[1:2]=="'") and b>0)):
                        b+=1
                    elif(code[i]==brackets[token[1:2]]):
                        b-=1
                if(b==0 and set([code[i]])-(signatureNumber|{'a','n','f'})!=set()):
                    tokens.append(token)
                    if(token!="@" and set([code[i],token[1:2]])-((set(brackets.keys())|set(brackets.values())))!=set()):
                        i-=1
                    token=""
            elif(token!=""):
                if(set([token])-markSymbols==set()):
                    if(token=="}" or token==")" or token=="|"):
                        try:
                            mstart=marks.pop()
                            mbegin=marks.pop()
                        except IndexError:
                            raise SyntaxError("opening parenthesis or marker arrow not found")
                        depth=len(marks)//2
                        parts.append([mbegin,mstart,[token,len(tokens)],depth])
                    if(set([token])-(markSymbols-{"}",")"})==set()):
                        marks.append([token,len(tokens)])
                tokens.append(token)
                token=""
            i+=1
        if(marks!=[]):
            raise SyntaxError("closing parenthesis not found")
#         print(2.,parts,marks)
#         print(2,tokens)
        for i in range(len(parts)):
            if(parts[i][0][1]!=parts[i][1][1]-1):
                for j in range(parts[i][1][1]-parts[i][0][1]-1):
                    tokens.insert(parts[i][2][1]-1,tokens.pop(parts[i][0][1]+1))
            j=1
            while(j<=i and parts[i-j][3]>=parts[i][3]):
                if(parts[i][0][0]=="{" and parts[i-j][3]==parts[i][3] and parts[i-j][0][0]=="(" and (parts[i-j][2][1]==parts[i][0][1]-1 or (parts[i-j][2][0]=="|" and parts[i-j+1][2][1]==parts[i][0][1]-1))):
                    for k in range(parts[i][2][1]-parts[i][0][1]+1):
                        tokens.insert(parts[i-j][0][1],tokens.pop(parts[i][2][1]))
                    break
                if(parts[i][1][0]=="⇁" and parts[i-j][3]==parts[i][3] and parts[i-j][0][0]=="(" and parts[i-j][2][1]==parts[i][0][1]):
                    tokens.insert(parts[i-j][0][1]+1,tokens.pop(parts[i][0][1]))
                    for k in range(parts[i][2][1]-parts[i][0][1]-1):
                        tokens.insert(parts[i-j][0][1]+1,tokens.pop(parts[i][2][1]-1))
                    break
                j+=1
#         print(3,tokens)
        text=""
        for i in range(len(tokens)):
            text+=tokens[i]
            if(set([tokens[i]])-{"{","}","(","|",")"}!=set()):
                text+=" "
        marks=[]
        parts=[]
        part=[]
        breaks=[]
        labels={}
        commands=[]
        for i in range(len(tokens)):
            if(set([tokens[i]])-markSymbols==set()):
                marks.append([tokens[i],i])
                part=[]
                if(len(marks)>=3 and tokens[marks[-3][1]-1:marks[-3][1]]!=["}"] and marks[-1][0]==")" and marks[-2][0]=="→" and marks[-3][0]=="("):
                    for j in range(3):
                        part.insert(0,marks.pop())
                    part.append("f1")
                elif(len(marks)>=3 and tokens[marks[-1][1]+1:marks[-1][1]+2]!=["("] and marks[-1][0]=="}" and marks[-2][0]=="→" and marks[-3][0]=="{"):
                    for j in range(3):
                        part.insert(0,marks.pop())
                    part.append("f2")
                elif(len(marks)>=6 and marks[-1][0]==")" and marks[-2][0]=="⇁" and marks[-3][0]=="(" and marks[-4][0]=="}" and marks[-5][0]=="→" and marks[-6][0]=="{"):
                    for j in range(6):
                        part.insert(0,marks.pop())
                    part.append("i1")
                elif(len(marks)>=6 and marks[-1][0]==")" and marks[-2][0]=="⇀" and marks[-3][0]=="(" and marks[-4][0]=="}" and marks[-5][0]=="→" and marks[-6][0]=="{"):
                    for j in range(6):
                        part.insert(0,marks.pop())
                    part.append("i2")
                elif(len(marks)>=8 and marks[-1][0]==")" and marks[-2][0]=="⇀" and marks[-3][0]=="|" and marks[-4][0]=="⇁" and marks[-5][0]=="(" and marks[-6][0]=="}" and marks[-7][0]=="→" and marks[-8][0]=="{"):
                    for j in range(8):
                        part.insert(0,marks.pop())
                    part.append("i3")
                elif(len(marks)>=6 and marks[-1][0]==")" and marks[-2][0]=="→" and marks[-3][0]=="(" and marks[-4][0]=="}" and marks[-5][0]=="→" and marks[-6][0]=="{"):
                    for j in range(6):
                        part.insert(0,marks.pop())
                    part.append("c1")
                elif(len(marks)>=8 and marks[-1][0]==")" and marks[-2][0]=="→" and marks[-3][0]=="|" and marks[-4][0]=="⇁" and marks[-5][0]=="(" and marks[-6][0]=="}" and marks[-7][0]=="→" and marks[-8][0]=="{"):
                    for j in range(8):
                        part.insert(0,marks.pop())
                    part.append("c2")
                if(part!=[]):
                    part.insert(-1,breaks)
                    breaks=[]
                    parts.append(part)
            elif(tokens[i]=="↪"):
                breaks.append(i)
        for i in range(len(parts)):
            for j in range(len(parts[i][-2])):
                tokens[parts[i][-2][j]]=f"ge{i}" #треба враховувати що для if має бути не {i}, а той n що є в першого не if в який вкладений цей if, або якщо ж такого немає то буде просто {i}
            if(parts[i][-1]=="f1"):
                tokens[parts[i][0][1]]="_"
                tokens[parts[i][1][1]]="_"
                tokens[parts[i][2][1]]=f"me{i}"
            elif(parts[i][-1]=="f2"):
                tokens[parts[i][0][1]]="_"
                tokens[parts[i][1][1]]="_"
                tokens[parts[i][2][1]]=f"me{i}"
            elif(parts[i][-1]=="i1"):
                tokens[parts[i][0][1]]="_"
                tokens[parts[i][1][1]]="_"
                tokens[parts[i][2][1]]=f"ie{i}"
                tokens[parts[i][3][1]]="_"
                tokens[parts[i][4][1]]="_"
                tokens[parts[i][5][1]]=f"me{i}"
            elif(parts[i][-1]=="i2"):
                tokens[parts[i][0][1]]="_"
                tokens[parts[i][1][1]]="_"
                tokens[parts[i][2][1]]=f"it{i}"
                tokens[parts[i][3][1]]=f"ge{i}"
                tokens[parts[i][4][1]]=f"mt{i}"
                tokens[parts[i][5][1]]=f"me{i}"
            elif(parts[i][-1]=="i3"):
                tokens[parts[i][0][1]]="_"
                tokens[parts[i][1][1]]="_"
                tokens[parts[i][2][1]]=f"it{i}"
                tokens[parts[i][3][1]]="_"
                tokens[parts[i][4][1]]="_"
                tokens[parts[i][5][1]]=f"ge{i}"
                tokens[parts[i][6][1]]=f"mt{i}"
                tokens[parts[i][7][1]]=f"me{i}"
            elif(parts[i][-1]=="c1"):
                tokens[parts[i][1][1]]=f"mi{i}"
                tokens[parts[i][2][1]]=f"ic{i}"
                tokens[parts[i][3][1]]=f"ge{i}"
                tokens[parts[i][4][1]]=f"mc{i}"
                tokens[parts[i][5][1]]=f"me{i}"
                tokens.insert(parts[i][5][1],f"gi{i}")
                tokens.pop(parts[i][0][1])
            elif(parts[i][-1]=="c2"):
                tokens[parts[i][0][1]]="_"
                tokens[parts[i][1][1]]=f"mi{i}"
                tokens[parts[i][2][1]]=f"ic{i}"
                tokens[parts[i][3][1]]="_"
                tokens[parts[i][5][1]]=f"ge{i}"
                tokens[parts[i][6][1]]=f"mc{i}"
                tokens[parts[i][7][1]]=f"me{i}"
                tokens.insert(parts[i][7][1],f"gi{i}")
                tokens.pop(parts[i][4][1])
#         print(4.,parts,marks)
#         print(4,tokens)
        for i in range(len(tokens)):
            if(tokens[i][:1]=="m"):
                labels[tokens[i][1:]]=len(commands)
            elif(tokens[i]!="_"):
                commands.append(tokens[i])
#         print(5.,labels)
#         print(5,commands)
        for i in range(len(commands)):
            if(commands[i][:1]=="@"):
                commands[i]=lambda s=stack,v=commands[i][1:]:s.push(v)
            elif(commands[i][:1]=="i"):
                commands[i]=lambda s=stack,i=labels[commands[i][1:]]:self.ifgoto(s,i)
            elif(commands[i][:1]=="g"):
                commands[i]=lambda i=labels[commands[i][1:]]:self.goto(i)
            else:
                commands[i]=functions[commands[i]]
#         print(6,commands)
        self.code=commands
        self.text=text
        self.i=0
    def __str__(self):
        return self.text
    def goto(self,i):
        self.i=i-1
    def ifgoto(self,stack,i):
        try:
            buffer=stack.pop()
        except IndexError:
            pass
        if(len(stack.stack)>0 and bool(bool_(buffer))):
            self.i=i-1
    def do(self):
        self.i=0
        try:
            while self.i<len(self.code):
                self.code[self.i]()
                self.i+=1
        except TypeError:
            self.push(error_(1))
        except ValueError:
            self.push(error_(2))
        except IndexError:
            self.push(error_(3))
        except KeyError:
            self.push(error_(4))
        except SyntaxError:
            self.push(error_(5))
        except ArithmeticError:
            self.push(error_(6))
        except RecursionError:
            self.push(error_(7))

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
        if(0<=int(code) and int(code)<=8):
            self.code=int(code)
        elif(int(code)==9):
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