from cmath import phase,isnan,isinf
from math import log,pi
errorCodes={Exception:0,TypeError:1,ValueError:2,IndexError:3,KeyError:4,SyntaxError:5,ArithmeticError:6,RecursionError:7,SystemExit:8}
priorityOfOperations={"+":1,"-":1,"*":2,"/":2,"↧":3,"^":4,"√":4,"E":5,"~":6}
constants={"τ":6.2831853071795864,"π":3.1415926535897932,"e":2.7182818284590452,"φ":1.6180339887498948,"i":1j,"∞":complex('inf'),"∅":complex('nan')}
defaultValue={"+":(0,0),"-":(0,0),"*":(1,1),"/":(1,1),"↧":(constants["e"],1),"^":(2,1),"√":(2,1),"E":(1,0),"~":(-1,-1)}
signatureNumber={'0','1','2','3','4','5','6','7','8','9','+','-','i','n','∞','∅','('}
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
def value(v,s=None):
    if(type(v)==str):
        if(v[:4].lower()=="none" or v[:1].lower()=="n"):
            v=none_()
        elif(v[:4].lower()=="true" or v[:5].lower()=="false" or v[:1].lower()=="t" or v[:1].lower()=="f"):
            v=bool_(v)
        elif(v[:1]=='"'):
            v=str_(v[1:-1])
        elif(v[:1]=="'"):
            v=bytes_(v)
        elif(v[:1]=='(' and v.count("→")+v.count("⇀")>0):
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
        elif(set([v[:1]])-signatureNumber==set()):
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
            elif(n==""):
                n=0
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
        return self.b==other.b
    def __hash__(self):
        return hash(self.b)
class bytes_(value_):
    def __init__(self,b):
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
        return self.b==other.b
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
    def __init__(self,s):
        if(type(s)==str_):
            s=str(s)[1:-1]
        self.s=str(s)
    def __str__(self):
        return '"'+self.s+'"'
    def __eq__(self,other):
        return self.s==other.s
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
            while l.count(", ")+l.count(" ,")+l.count("[ ")+l.count(" ]")>0:
                l=l.replace(", ", ",")
                l=l.replace(" ,", ",")
                l=l.replace("[ ", "[")
                l=l.replace(" ]", "]")
            if(l=="[]" or l==""):
                l=list()
            else:
                for i in range(len(l)):
                    if(l[i]=="["):
                        r+=1
                    elif((l[i]=="," or l[i]=="]") and r==1):
                        b=e
                        e=i
                        nl.append(value(l[b+1:e],s))
                    elif(l[i]=="]"):
                        r-=1
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
        return self.l==other.l
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
            while d.count(", ")+d.count(" ,")+d.count("[ ")+d.count(" ]")>0:
                d=d.replace(", ", ",")
                d=d.replace(" ,", ",")
                d=d.replace("[ ", "[")
                d=d.replace(" ]", "]")
            if(d=="[]" or d==""):
                d=dict()
            else:
                for i in range(len(d)):
                    if(d[i]=="["):
                        r+=1
                    elif(d[i]==":" and r==1):
                        m=i
                    elif((d[i]=="," or d[i]=="]") and r==1):
                        b=e
                        e=i
                        l.append((value(d[b+1:m]),value(d[m+1:e],s)))
                    elif(d[i]=="]"):
                        r-=1
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
        return self.d==other.d
    def __add__(self,other):
        for k,i in other.d.items():
            self.d[k]=i
        return self
    def find(self,fv):
        return (lambda l: l[0] if len(l)>0 else num_(-1))([k for k,v in self.d.items() if v==fv])
class function_(value_):
    class Code():
        def __init__(self,c,s,b=0,ef=(lambda:None)):
            functions={"+":lambda s=s:s.plus(),"-":lambda s=s:s.minus(),"*":lambda s=s:s.mult(),"/":lambda s=s:s.div(),"^":lambda s=s:s.exp(),"↧":lambda s=s:s.log(),
                       "↕":lambda s=s:s.abs(),"o":lambda s=s:s.round(),"R":lambda s=s:s.random(),"s":lambda s=s:s.sin(),"c":lambda s=s:s.cos(),"t":lambda s=s:s.tan(),
                       "S":lambda s=s:s.arcsin(),"C":lambda s=s:s.arccos(),"T":lambda s=s:s.arctan(),"=":lambda s=s:s.eq(),"<":lambda s=s:s.lt(),">":lambda s=s:s.gt(),
                       "¬":lambda s=s:s.not_(),"⋀":lambda s=s:s.and_(),"∨":lambda s=s:s.or_(),"⊕":lambda s=s:s.xor(),"w":lambda s=s:s.write(),"f":lambda s=s:s.find(),
                       "a":lambda s=s:s.append(),"d":lambda s=s:s.delete(),"r":lambda s=s:s.read(),"l":lambda s=s:s.len(),"u":lambda s=s:s.substring(),
                       "&":lambda s=s:s.concatenate(),"@":lambda s=s:s.push(),"D":lambda s=s:s.pop(),"$":lambda s=s:s.copy(),"L":lambda s=s:s.size(),"%":lambda s=s:s.Bswap(),
                       "‰":lambda s=s:s.Tswap(),"↑":lambda s=s:s.moveUp(),"↓":lambda s=s:s.moveDown(),"p":lambda s=s:s.print(),"e":lambda s=s:s.enter(),
                       "§":lambda s=s:s.doNamedFun(),"!":lambda s=s:s.doFun(),"?":lambda s=s:s.type(),"F":lambda s=s:s.format(),"↪":lambda s=s:"break"}
            code=[]
            p=["",False,'']
            r={'"':0,"'":0,"[":0,"{":0,"(":0,"⟨":0}
            for i in range(len(c)):
                l=c[(i+b)%len(c)]
                print(l,r,p)
                if(p[1]):
                    if(set([l])-{"[","{","(","⟨"}==set() or (l=='"' and r['"']==0) or (l=="'" and r["'"]==0)):
                        r[l]+=1
                    elif(set([l])-{'"',"'","]","}",")","⟩"}==set()):
                        r[l.replace("]","[").replace("}","{").replace(")","(").replace("⟩","⟨")]-=1
                    if((p[2]=='"' and l=='"' and r['"']==0) or (p[2]=="'" and l=="'" and r["'"]==0) or (p[2]=='[' and l==']' and r['[']==0) or (p[2]=='{' and (l=='}' or l==')') and r['{']==0 and c[(i+b+1)%len(c)]!='(') or (p[2]=='⟨' and l=='⟩' and r['⟨']==0) or (p[2]=='(' and (l==')' or l=='}') and r['(']==0 and c[(i+b+1)%len(c)]!='{') or (set([p[2]])-signatureNumber==set() and set([l])-(signatureNumber|{'E','.','~','j','f','a'})!=set()) or ((p[2]=='n' or p[2]=='t' or p[2]=='f') and l==' ') or (i==len(c)-1)):
                        if(l!=' '):
                            p[0]=p[0]+l
                        code.append(lambda s=s,d=p[0]: s.push(d))
                        p=["",False,'']
                        r={'"':0,"'":0,"[":0,"{":0,"(":0,"⟨":0}
                        print(code)
                    else:
                        p[0]=p[0]+l
                elif(l==" " or l=="→" or l=="⇀" or l=="⇁"):
                    pass
                elif(l=="@"):
                    p[1]=True
                    p[2]=c[(i+b+1)%len(c)].lower()
                elif(set([l])-set(functions.keys())==set()):
                    code.append(functions[l])
                else:
                    raise SyntaxError(f"unknown commands {l}")
            code.append(ef)
            self.code=code
            self.Stack=s
        def do(self):
            for i in range(len(self.code)):
                self.code[i]()
    def __init__(self,f,s):
        if(type(f)==str_):
            f=str(f)[1:-1]
        if(type(f)==str):
            wb,we,ob,oe,om,os,st,se=None,None,None,None,None,None,None,None
            i,r1,r2,r3=0,0,0,0
            while i<len(f):
                if(f[i]=="("):
                    r1+=1
                    if(r1==1):
                        ob=i
                elif(f[i]=="{"):
                    r2+=1
                    if(r2==1):
                        wb=i
                elif(f[i]=="["):
                    r3+=1
                elif(f[i]==")"):
                    r1-=1
                    if(r1==0):
                        oe=i
                elif(f[i]=="}"):
                    r2-=1
                    if(r2==0):
                        we=i
                elif(f[i]=="]"):
                    r3-=1
                elif(f[i]=="|"):
                    if(r1==1):
                        om=i
                elif(f[i]=="→"):
                    if(r1==1):
                        os=i
                elif(f[i]=="⇀"):
                    if(r1==1):
                        st=i
                elif(f[i]=="⇁"):
                    if(r1==1):
                        se=i
                elif(f[i]==" "):
                    b,j=i+1,i+1
                    while f[j]==" ":
                        j+=1
                    if(j-b>0):
                        f=f[:b]+f[j:]
                i+=1
            if(r1!=0 or r2!=0 or r3!=0):
                raise SyntaxError("the number of open parentheses is not equal to the number of closed parentheses")
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
            if(os!=None and ob!=None):
                if(If==""):
                    Then=function_.Code(Then,s,os-ob)
                else:
                    Then=function_.Code(Then,s,os-ob,lambda foo=self: foo.If.do())
            elif(st!=None and ob!=None):
                Then=function_.Code(Then,s,st-ob)
            else:
                Then=function_.Code(Then,s)
            if(se!=None and om!=None):
                Else=function_.Code(Else,s,se-om)
            else:
                Else=function_.Code(Else,s)
            if(If==""):
                If=function_.Code(If,s,0,lambda foo=self: foo.Then.do())
            else:
                If=function_.Code(If,s,0,lambda foo=self: foo.Then.do() if s.pop() else foo.Else.do())
#         w=f[wb+1:we]
#         f=f[ob+1:oe]
#         os=os-ob
#         st=st-ob
#         se=se-ob
#         l,t,el=[],[],[]
#         p=["",False,'']
#         for i in range(len(f)):
#             e=f[(i+os)%len(f)]
#             if(p[1]):
#                 if((p[2]=='"' and e=='"') or (p[2]=="'" and e=="'") or (p[2]=='[' and e==']') or (p[2]=='{' and e=='}') or (p[2]=='⟨' and e=='⟩') or (p[2]=='(' and e==')') or (set([p[2]])-signatureNumber==set() and set([e])-(signatureNumber|{'E','.','~','f','a'})!=set())):
#                     if(e!=' '):
#                         p[0]=p[0]+e
#                     l.append("@"+p[0])
#                     p=["",False,'']
#                 else:
#                     p[0]=p[0]+e
#             elif(e==" "):
#                 pass
#             elif(e=="@"):
#                 p[1]=True
#                 p[2]=f[(i+os+1)%len(f)]
#             elif(set([e])-set(functions.keys())==set() and e!='g' and e!='i'):
#                 l.append(e)
#         if(w[:1]=="{"):
#             w=function_(w)
#         print(w,l,el)
        self.If=If
        self.Then=Then
        self.Else=Else
        self.text=str(f)
    def __str__(self):
#         s="{"+str(self.If)+"}(→ "
#         for i in self.Then:
#             s=s+str(i)+" "
#         s=s+"|⇁ "
#         for i in self.Else:
#             s=s+str(i)+" "
#         return s[:-1]+")"
        return self.text
    def __eq__(self,other):
        return self.f==other.f
    def do(self):
        self.If.do()
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
        return self.t==other.t
    def __hash__(self):
        return hash(self.t)
class error_(value_):
    def __init__(self,code=0):
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
        return self.code==other.code
    def __hash__(self):
        return hash(self.code)