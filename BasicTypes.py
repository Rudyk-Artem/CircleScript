class value_():
    def __init__(self,v):
        self.v=v
    def __str__(self):
        return str(self.v)
    def __eq__(self,other):
        return self.v==other.v
class none_(value_):
    def __init__(self):
        pass
    def __str__(self):
        return "None"
    def __eq__(self,other):
        return type(self)==type(other)
class num_(value_):
    def __init__(self,n):
        if(type(n)==str_):
            n=str(n)
        if(type(n)==str):
            n=n.replace('∞','inf').replace('∅','nan').replace('*i','j')
        if(str(abs(complex(n)))=='inf' or str(abs(complex(n)))=='nan' or abs(complex(n))==0):
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
            return i+'*i'
        else:
            r=str(self.n.real).replace('e','E')
            i=str(self.n.imag).replace('e','E')
            if(float(r)%1==0):
                r=r.replace('.0','')
            if(float(i)%1==0):
                i=i.replace('.0','')
            if(float(i)>=0):
                i='+'+i
            return r+i+'*i'
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
        return self.n==other.n
    def __round__(self,n):
        if(type(n)==int):
            self.n=complex(round(self.n.real,n),round(self.n.imag,n))
            return self
        raise ValueError
    def isInteger(self):
        return (self.n.imag==0 and self.n.real%1==0 and abs(self.n.real)<9007199254740992)
    def isReal(self):
        return (self.n.imag==0)
    def isImag(self):
        return (self.n.real==0)
class bool_(value_):
    def __init__(self,b):
        if(type(b)==str_):
            b=str(b)
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
class bytes_(value_):
    def __init__(self,b):
        self.b=bytes(b)
    def __str__(self):
        return str(self.b)
    def __bytes__(self):
        return self.b
    def __eq__(self,other):
        return self.b==other.b
class str_(value_):
    def __init__(self,s):
        self.s=str(s)
    def __str__(self):
        return '"'+self.s+'"'
    def __eq__(self,other):
        return self.s==other.s
class list_(value_):
    def __init__(self,l):
        self.l=list(l)
        self.i=0
    def __str__(self):
        s="["
        for i in range(len(self.l)):
            s=s+str(self.l[i])+", "
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
    def __getitem__(self,i):
        return self.l[i]
    def __setitem__(self,i,v):
        self.l[i]=v
    def __len__(self):
        return len(self.l)
    def insert(self,i,v):
        self.l.insert(i,v)
    def pop(self,i):
        return self.l.pop(i)
    def __eq__(self,other):
        return self.l==other.l
class dict_(value_):
    def __init__(self):
        pass
    def __str__(self):
        pass
    def __eq__(self,other):
        return self.d==other.d
class function_(value_):
    def __init__(self):
        pass
    def __str__(self):
        pass
    def __eq__(self,other):
        return self.f==other.f
class type_(value_):
    def __init__(self):
        pass
    def __str__(self):
        pass
    def __eq__(self,other):
        return self.t==other.t
class error_(value_):
    def __init__(self,code=0):
        self.code=int(code)
    def __str__(self):
        return "{"+str(self.code)+"}"
    def __eq__(self,other):
        return self.code==other.code