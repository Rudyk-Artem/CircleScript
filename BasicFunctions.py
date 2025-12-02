from math import sin,cos,sinh,cosh,pi
from cmath import isnan,isinf
from random import random
from BasicTypes import *
NamedFunction={}
class Stack():
    def __init__(self):
        self.stack=list()
    def __str__(self):
        if(len(self.stack)==0):
            return "⟨⟩"
        s="⟨"
        for i in range(len(self.stack)):
            s=s+str(self.stack[i])+"; "
        return s[:-2]+"⟩"
    def plus(self):
        if(type(self.stack[-1])==num_ and type(self.stack[-2])==num_):
            try:
                buffer=[self.pop(),self.pop()]
                self.push(buffer[1]+buffer[0])
            except ArithmeticError:
                self.push(buffer[1])
                self.push(buffer[0])
                self.push(error_(6))
        else:
            self.push(error_(1))
    def minus(self):
        if(type(self.stack[-1])==num_ and type(self.stack[-2])==num_):
            try:
                buffer=[self.pop(),self.pop()]
                self.push(buffer[1]-buffer[0])
            except ArithmeticError:
                self.push(buffer[1])
                self.push(buffer[0])
                self.push(error_(6))
        else:
            self.push(error_(1))
    def mult(self):
        if(type(self.stack[-1])==num_ and type(self.stack[-2])==num_):
            try:
                buffer=[self.pop(),self.pop()]
                self.push(buffer[1]*buffer[0])
            except ArithmeticError:
                self.push(buffer[1])
                self.push(buffer[0])
                self.push(error_(6))
        else:
            self.push(error_(1))
    def div(self):
        if(type(self.stack[-1])==num_ and type(self.stack[-2])==num_):
            try:
                buffer=[self.pop(),self.pop()]
                self.push(buffer[1]/buffer[0])
            except ArithmeticError:
                self.push(buffer[1])
                self.push(buffer[0])
                self.push(error_(6))
        else:
            self.push(error_(1))
    def exp(self):
        if(type(self.stack[-1])==num_ and type(self.stack[-2])==num_):
            try:
                buffer=[self.pop(),self.pop()]
                self.push(buffer[1]**buffer[0])
            except ValueError:
                self.push(buffer[1])
                self.push(buffer[0])
                self.push(error_(2))
            except ArithmeticError as err:
                self.push(buffer[1])
                self.push(buffer[0])
                self.push(error_(6))
        else:
            self.push(error_(1))
    def log(self):
        if(type(self.stack[-1])==num_ and type(self.stack[-2])==num_):
            try:
                buffer=[complex(self.pop()),complex(self.pop())]
                if(buffer[0]==1 or isinf(buffer[0])):
                    self.push(num_('nan'))
                else:
                    self.push(round(num_(buffer[1]).Ln()/num_(buffer[0]).Ln(),15))
            except ValueError:
                self.push(num_(buffer[1]))
                self.push(num_(buffer[0]))
                self.push(error_(2))
            except ArithmeticError:
                self.push(num_(buffer[1]))
                self.push(num_(buffer[0]))
                self.push(error_(6))
        else:
            self.push(error_(1))
    def abs(self):
        if(type(self.stack[-1])==num_):
            try:
                buffer=complex(self.pop())
                self.push(num_(abs(buffer)))
            except ArithmeticError:
                self.push(num_(buffer))
                self.push(error_(6))
        else:
            self.push(error_(1))
    def round(self):
        if(type(self.stack[-1])==num_ and type(self.stack[-2])==num_):
            try:
                buffer=[int(self.pop()),self.pop()]
                self.push(round(buffer[1],buffer[0]))
            except ValueError:
                self.push(num_(buffer[1]))
                self.push(num_(buffer[0]))
                self.push(error_(2))
            except ArithmeticError:
                self.push(num_(buffer[1]))
                self.push(num_(buffer[0]))
                self.push(error_(6))
        else:
            self.push(error_(1))
    def random(self):
        self.push(num_(random()))
    def sin(self):
        if(type(self.stack[-1])==num_):
            try:
                buffer=complex(self.pop())
                if(isinf(buffer)):
                    self.push(num_('nan'))
                else:
                    self.push(round(num_(sin(buffer.real)*cosh(buffer.imag)+1j*cos(buffer.real)*sinh(buffer.imag)),15))
            except ValueError:
                self.push(num_(buffer))
                self.push(error_(2))
            except ArithmeticError:
                self.push(num_(buffer))
                self.push(error_(6))
        else:
            self.push(error_(1))
    def cos(self):
        if(type(self.stack[-1])==num_):
            try:
                buffer=complex(self.pop())
                if(isinf(buffer)):
                    self.push(num_('nan'))
                else:
                    self.push(round(num_(cos(buffer.real)*cosh(buffer.imag)-1j*sin(buffer.real)*sinh(buffer.imag)),15))
            except ValueError:
                self.push(num_(buffer))
                self.push(error_(2))
            except ArithmeticError:
                self.push(num_(buffer))
                self.push(error_(6))
        else:
            self.push(error_(1))
    def tan(self):
        if(type(self.stack[-1])==num_):
            try:
                buffer=complex(self.pop())
                if(isinf(buffer)):
                    self.push(num_('nan'))
                else:
                    self.push(round(num_((sin(2*buffer.real)+1j*sinh(2*buffer.imag))/(cos(2*buffer.real)+cosh(2*buffer.imag))),15))
            except ZeroDivisionError:
                self.push(num_('inf'))
            except ValueError:
                self.push(num_(buffer))
                self.push(error_(2))
            except ArithmeticError:
                self.push(num_(buffer))
                self.push(error_(6))
        else:
            self.push(error_(1))
    def arcsin(self):
        if(type(self.stack[-1])==num_):
            try:
                buffer=complex(self.pop())
                self.push(round(num_(-1j)*num_(1j*buffer+(1-buffer**2)**(1/2)).Ln(),15))
            except ValueError:
                self.push(num_(buffer))
                self.push(error_(2))
            except ArithmeticError:
                self.push(num_(buffer))
                self.push(error_(6))
        else:
            self.push(error_(1))
    def arccos(self):
        if(type(self.stack[-1])==num_):
            try:
                buffer=complex(self.pop())
                self.push(round(num_(-1j)*num_(buffer+(buffer**2-1)**(1/2)).Ln(),15))
            except ValueError:
                self.push(num_(buffer))
                self.push(error_(2))
            except ArithmeticError:
                self.push(num_(buffer))
                self.push(error_(6))
        else:
            self.push(error_(1))
    def arctan(self):
        if(type(self.stack[-1])==num_):
            try:
                buffer=complex(self.pop())
                if(isinf(buffer)):
                    self.push(num_(pi/2))
                else:
                    self.push(round(num_(-0.5j)*num_((1+1j*buffer)/(1-1j*buffer)).Ln(),15))
            except ValueError:
                self.push(num_(buffer))
                self.push(error_(2))
            except ArithmeticError:
                self.push(num_(buffer))
                self.push(error_(6))
        else:
            self.push(error_(1))
    def eq(self):
        if(type(self.stack[-1])==type(self.stack[-2])):
            self.push(bool_(self.pop()==self.pop()))
        else:
            self.push(error_(1))
    def lt(self):
        if(type(self.stack[-1])==type(self.stack[-2])):
            if(type(self.stack[-1])==num_ and self.stack[-1].isReal() and self.stack[-2].isReal()):
                self.push(bool_(float(self.pop())<float(self.pop())))
            elif(type(self.stack[-1])==str_):
                self.push(bool_(str(self.pop())<str(self.pop())))
            elif(type(self.stack[-1])==bytes_):
                self.push(bool_(bytes(self.pop())<bytes(self.pop())))
            else:
                self.push(error_(1))
        else:
            self.push(error_(1))
    def gt(self):
        if(type(self.stack[-1])==type(self.stack[-2])):
            if(type(self.stack[-1])==num_ and self.stack[-1].isReal() and self.stack[-2].isReal()):
                self.push(bool_(float(self.pop())>float(self.pop())))
            elif(type(self.stack[-1])==str_):
                self.push(bool_(str(self.pop())>str(self.pop())))
            elif(type(self.stack[-1])==bytes_):
                self.push(bool_(bytes(self.pop())>bytes(self.pop())))
            else:
                self.push(error_(1))
        else:
            self.push(error_(1))
    def not_(self):
        if(type(self.stack[-1])==bool_):
            self.push(bool_(not bool(self.pop())))
        else:
            self.push(error_(1))
    def and_(self):
        if(type(self.stack[-1])==bool_ and type(self.stack[-2])==bool_):
            buffer=[bool(self.pop()),bool(self.pop())]
            self.push(bool_(buffer[0] and buffer[1]))
        else:
            self.push(error_(1))
    def or_(self):
        if(type(self.stack[-1])==bool_ and type(self.stack[-2])==bool_):
            buffer=[bool(self.pop()),bool(self.pop())]
            self.push(bool_(buffer[0] or buffer[1]))
        else:
            self.push(error_(1))
    def xor(self):
        if(type(self.stack[-1])==bool_ and type(self.stack[-2])==bool_):
            buffer=[bool(self.pop()),bool(self.pop())]
            self.push(bool_(not(buffer[0] or not(buffer[0] or buffer[1])) or not(not(buffer[0] or buffer[1]) or buffer[1])))
        else:
            self.push(error_(1))
    def write(self):
        pass
    def find(self):
        pass
    def append(self):
        pass
    def delete(self):
        pass
    def read(self):
        pass
    def len(self):
        pass
    def substring(self):
        pass
    def concatenate(self):
        pass
    def push(self,v):
        if((type(v)==str and v[:1]=='⟨') or (type(v)==str_ and str(v[1:2])=='⟨')):
            if(type(v)==str_):
                v=str(v)[1:-1]
            s,f=0,0
            while v.count("; ")+v.count(" ;")+v.count("⟨ ")+v.count(" ⟩")>0:
                v=v.replace("; ", ";")
                v=v.replace(" ;", ";")
                v=v.replace("⟨ ", "⟨")
                v=v.replace(" ⟩", "⟩")
            for i in range(len(v)):
                if(v[i]==";" or v[i]=="⟩"):
                    s=f
                    f=i
                    self.stack.append(value(v[s+1:f]))
        else:
            self.stack.append(value(v))
    def pop(self):
        return self.stack.pop()
    def copy(self):
        self.push(self.stack[-1])
    def size(self):
        self.push(len(self.stack))
    def Bswap(self):
        self.stack.insert(-1,self.pop())
    def Tswap(self):
        self.stack.insert(-2,self.pop())
    def moveUp(self):
        if(type(self.stack[-1])==num_):
            self.push(self.stack.pop(self.stack.pop()))
        elif(type(self.stack[-1])==list_):
            buffer=[list(self.stack.pop())]
            for i in range(len(buffer[0])):
                if(type(buffer[0][i])==num_):
                    if(not buffer[0][i].isInteger()):
                        self.push(list_(buffer[0]))
                        self.push(error_(2))
                        return
                elif(not (issubclass(type(buffer[0][i]),value_) and (type(buffer[0][i])!=list_ and type(buffer[0][i]))!=dict_)):
                    self.push(list_(buffer[0]))
                    self.push(error_(1))
                    return
            try:
                buffer.append(self.stack[int(buffer[0][0])])
                for i in range(1,len(buffer[0])-1):
                    if(type(buffer[1])==list_):
                        buffer[1]=buffer[1][int(buffer[0][i])]
                    elif(type(buffer[1])==dict_):
                        buffer[1]=buffer[1][buffer[0][i]]
                    else:
                        self.push(list_(buffer[0]))
                        self.push(error_(1))
                self.push(buffer[1].pop(buffer[0][-1]))
            except TypeError:
                self.push(list_(buffer[0]))
                self.push(error_(1))
            except IndexError:
                self.push(list_(buffer[0]))
                self.push(error_(3))
            except KeyError:
                self.push(list_(buffer[0]))
                self.push(error_(4))
        else:
            self.push(error_(1))
    def moveDown(self):
        if(type(self.stack[-1])==int):
            self.stack.insert(self.pop(),self.pop())
        elif(type(self.stack[-1])==list_):
            buffer=[self.stack.pop()]
            for i in range(len(buffer[0])):
                if(type(buffer[0][i])==num_):
                    if(not buffer[0][i].isInteger()):
                        self.push(list_(buffer[0]))
                        self.push(error_(2))
                        return
                elif(not (issubclass(type(buffer[0][i]),value_) and (type(buffer[0][i])!=list_ and type(buffer[0][i]))!=dict_)):
                    self.push(list_(buffer[0]))
                    self.push(error_(1))
                    return
            try:
                buffer.append(self.stack[int(buffer[0][0])])
                for i in range(1,len(buffer[0])-1):
                    if(type(buffer[1])==list_):
                        buffer[1]=buffer[1][int(buffer[0][i])]
                    elif(type(buffer[1])==dict_):
                        buffer[1]=buffer[1][buffer[0][i]]
                if(type(buffer[1])==list_ and int(buffer[0][-1])<0):
                    buffer[0][-1]=num_(int(buffer[0][-1])+1)
                    if(int(buffer[0][-1])==0):
                        buffer[0][-1]=num_(len(self.stack))
                buffer[1].insert(buffer[0][-1],self.pop())
            except TypeError:
                self.push(list_(buffer[0]))
                self.push(error_(1))
            except IndexError:
                self.push(list_(buffer[0]))
                self.push(error_(3))
            except KeyError:
                self.push(list_(buffer[0]))
                self.push(error_(4))
        else:
            self.push(error_(1))
    def print(self):
        if(type(self.stack[-1])==str_):
            print(self.stack.pop())
        else:
            self.push(error_(1))
    def enter(self):
        self.push(str_(input()))
    def doNamedFun(self):
        try:
            if(type(-self.stack[-1])==str_):
                NamedFunction[str(self.pop())[1:-1]].do()
            else:
                self.push(error_(1))
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
    def doFun(self):
        try:
            if(type(self.stack[-1])==num_ and type(self.stack[-self.stack[-1]-2])==function_):
                self.stack[-self.pop()-1].do()
            else:
                self.push(error_(1))
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
    def type(self):
        self.push(type_(type(self.pop())))
    def format(self):
        if(type(self.stack[-1])==type_):
            self.push(self.pop().t(self.pop()))