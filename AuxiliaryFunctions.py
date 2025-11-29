from cmath import phase
from math import log,pi
import BasicTypes
def Ln(n,k=0):
    if(n==0):
        return complex('inf')
    return log(abs(n))+1j*(phase(n)+2*pi*k)
errorCodes={Exception:0,TypeError:1,ValueError:2,IndexError:3,KeyError:4,SyntaxError:5,ArithmeticError:6,RecursionError:7,SystemExit:8}
priorityOfOperations={"+":1,"-":1,"*":2,"/":2,"↧":3,"^":4,"√":4,"E":5,"~":6}
constants={"τ":6.2831853071795864,"π":3.1415926535897932,"e":2.7182818284590452,"φ":1.6180339887498948,"i":1j,"∞":complex('inf'),"∅":complex('nan')}
defaultValue={"+":(0,0),"-":(0,0),"*":(1,1),"/":(1,1),"↧":(2.7182818284590452,1),"^":(2,1),"√":(2,1),"E":(1,0),"~":(-1,-1)}
operations={"+":lambda a,b:a+b,"-":lambda a,b:a-b,"*":lambda a,b:a*b,"/":lambda a,b:a/b,"↧":lambda a,b:Ln(a)/Ln(b),"^":lambda a,b:a**b,"√":lambda a,b:a**(1/b),
            "E":lambda a,b:a*10**b,"~":lambda a,b:a*b,"n":lambda a:complex(a),"c":lambda a:constants[a],"d":lambda d:defaultValue[d[0]][d[1]]}
def is_number(s):
    try:
        complex(s)
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
                an=operations[self.op](self.left.count(),self.right.count())
            else:
                an=operations[self.op](self.value)
        return an
def value(v):
    if(type(v)==str):
        if(v[:4].capitalize()=="None"):
            v=BasicTypes.none_()
        elif(v[:4].capitalize()=="True" or v[:5].capitalize()=="False"):
            v=BasicTypes.bool_(v)
        elif(v[:1]=='"'):
            v=BasicTypes.str_(v[1:-1])
        elif(v[:1]=="'"):
            v=BasicTypes.bytes_(v)
        elif(v[:1]=='{'):
            for i in range(len(v)):
                if(v[i]=='@' or v[i]=='₴'):
                    v=BasicTypes.function_(v)
                    break
                elif(v[i]=='}'):
                    v=BasicTypes.error_(v)
                    break
        elif(v[:1]=='['):
            if(set([v[1:2]])-{'n','s','b','l','d','f','t','e'}==set()):
                v=BasicTypes.type_(v)
            else:
                for i in range(len(v)):
                    if(v[i]==':'):
                        v=BasicTypes.dict_(v)
                        break
                    elif(v[i]==',' or v[i]=='['):
                        v=BasicTypes.list_(v)
                        break
        elif(set([v[:1]])-{'0','1','2','3','4','5','6','7','8','9','+','-','~','τ','π','e','φ','i','∞','∅'}==set()):
            v=BasicTypes.num_(ExpressionTreeNode(v).count())
    try:
        if(type(v)==type and set([v])-set(errorCodes.keys())==set()):
            v=BasicTypes.error_(v)
        else:
            valueTypes={type(None):BasicTypes.none_,int:BasicTypes.num_,float:BasicTypes.num_,complex:BasicTypes.num_,bool:BasicTypes.bool_,
                        bytes:BasicTypes.bytes_,str:BasicTypes.str_,list:BasicTypes.list_,dict:BasicTypes.dict_,type:BasicTypes.type_}
            v=valueTypes[type(v)](v)
    except KeyError:
        pass
    if(issubclass(type(v),BasicTypes.value_)):
        return v
    else:
        raise ValueError