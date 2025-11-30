from tabulate import *
from BasicTypes import *
from BasicFunctions import *
def root(s):
    s.push(num_(1))
    s.Bswap()
    s.div()
    s.exp()
s=Stack()
v,l=[num_(0),num_(1),num_(2),num_(-2),num_(3+3j),num_(-3-3j),num_('inf'),num_('nan')],[]
for i in range(len(v)):
    l.append([str(v[i])])
    for j in range(len(v)):
        s.push(v[i])
        s.push(v[j])
        s.plus()
        l[-1].append(str(s.pop()))
print("|--------+--------+--------+--------+--------+---------+----------+-----+-----|")
print(tabulate(l,headers=["a+b"]+v,tablefmt='orgtbl'))
l=[]
for i in range(len(v)):
    l.append([str(v[i])])
    for j in range(len(v)):
        s.push(v[i])
        s.push(v[j])
        s.minus()
        l[-1].append(str(s.pop()))
print("|--------+--------+--------+--------+--------+---------+----------+-----+-----|")
print(tabulate(l,headers=["a-b"]+v,tablefmt='orgtbl'))
l=[]
for i in range(len(v)):
    l.append([str(v[i])])
    for j in range(len(v)):
        s.push(v[i])
        s.push(v[j])
        s.mult()
        l[-1].append(str(s.pop()))
print("|--------+-----+--------+--------+--------+---------+----------+-----+-----|")
print(tabulate(l,headers=["a*b"]+v,tablefmt='orgtbl'))
l=[]
for i in range(len(v)):
    l.append([str(v[i])])
    for j in range(len(v)):
        s.push(v[i])
        s.push(v[j])
        s.div()
        s.push(num_(3))
        s.round()
        if(type(s.stack[-1])==error_ and s.stack[-1]==error_(1)):
            s.pop()
            s.pop()
        l[-1].append(str(s.pop()))
print("|--------+-----+--------+------------+------------+----------------+----------------+-----+-----|")
print(tabulate(l,headers=["a/b"]+v,tablefmt='orgtbl'))
l=[]
for i in range(len(v)):
    l.append([str(v[i])])
    for j in range(len(v)):
        s.push(v[i])
        s.push(v[j])
        s.exp()
        s.push(num_(3))
        s.round()
        if(type(s.stack[-1])==error_ and s.stack[-1]==error_(1)):
            s.pop()
            s.pop()
        l[-1].append(str(s.pop()))
print("|--------+-----+--------+------+----------+------------------------+--------------------+-----+-----|")
print(tabulate(l,headers=["a^b"]+v,tablefmt='orgtbl'))
l=[]
for i in range(len(v)):
    l.append([str(v[i])])
    for j in range(len(v)):
        s.push(v[i])
        s.push(v[j])
        root(s)
        s.push(num_(3))
        s.round()
        if(type(s.stack[-1])==error_ and s.stack[-1]==error_(1)):
            s.pop()
            s.pop()
        l[-1].append(str(s.pop()))
print("|--------+-----+--------+---------------+---------------+---------------+---------------+-----+-----|")
print(tabulate(l,headers=["b√a"]+v,tablefmt='orgtbl'))
l=[]
for i in range(len(v)):
    l.append([str(v[i])])
    for j in range(len(v)):
        s.push(v[i])
        s.push(v[j])
        s.log()
        s.push(num_(3))
        s.round()
        if(type(s.stack[-1])==error_ and s.stack[-1]==error_(1)):
            s.pop()
            s.pop()
        l[-1].append(str(s.pop()))
print("|------------+-----+-----+---------------+---------------+--------------+--------------+-----+-----|")
print(tabulate(l,headers=["log_b(a)"]+v,tablefmt='orgtbl'))
l=[]
v=[num_(pi),num_(pi/2),num_(pi/3),num_(pi/4),num_(pi/6),num_(0),num_(-pi/6*1j),num_(-pi/4*1j),num_(-pi/3*1j),num_(-pi/2*1j),num_(-pi*1j),num_('inf'),num_('nan')]
o=[lambda s: None,lambda s: s.sin(),lambda s: s.cos(),lambda s: s.tan()]
ao=[lambda s: None,lambda s: s.arcsin(),lambda s: s.arccos(),lambda s: s.arctan(),]
vn=["op","π","π/2","π/3","π/4","π/6","0","-π/6*i","-π/4*i","-π/3*i","-π/2*i","-π*i","∞","∅"]
on=["no op","sin","cos","tan"]
aon=["no op","arcsin","arccos","arctan"]
for i in range(1,len(o)):
    l.append([on[i]])
    for j in range(len(v)):
        s.push(v[j])
        o[i](s)
        s.push(num_(3))
        s.round()
        if(type(s.stack[-1])==error_ and s.stack[-1]==error_(1)):
            s.pop()
            s.pop()
        l[-1].append(str(s.pop()))
print("|------+-----+-------+-------+-------+-------+-----+----------+----------+----------+----------+-----------+-----+-----|")
print(tabulate(l,headers=vn,tablefmt='orgtbl'))
l=[]
for i in range(len(ao)):
    l.append([aon[i]])
    for j in range(len(v)):
        s.push(num_(v[j]))
        o[i](s)
        ao[i](s)
        s.push(num_(3))
        s.round()
        if(type(s.stack[-1])==error_ and s.stack[-1]==error_(1)):
            s.pop()
            s.pop()
        l[-1].append(str(s.pop()))
print("Перевірка чи дорівнює arc-функції значеню яке було передано функціям:")
print("|--------+-------+-------+--------+-------+-------+-----+----------+----------+----------+----------+----------+-----+-----|")
print(tabulate(l,headers=vn,tablefmt='orgtbl'))

s=Stack()
print(s)
s.push({"a":[1,2,3],"b":[4,5,6],"c":[7,8,9]})
s.push(10000000000000000+9999999999999999999999j)
s.push("'\x00\x01\xff∞'")
print(s,"push")
s.push([0,"b",1])
s.moveUp()
print(s,"moveUp")
s.push([0,"b",1])
s.moveDown()
print(s,"moveDown")
s.random()
s.random()
print(s,"random")
s.push(num_(1j))
s.mult()
s.plus()
print(s,"об'єднання чисел у комплексне")
s.push(num_(5))
s.round()
print(s,"round")
s.abs()
print(s,"abs")
print("Докладна перевірка tan й arctan:")
n=3
for i in range(n*2+1):
    s.push(num_(i*pi/n-pi))
    s.push(num_(i*pi/n-pi))
    s.tan()
    s.push(num_(i*pi/n-pi))
    s.tan()
    s.arctan()
    print(f"tan(α)= {str(s.stack[-2]): <20}| {i-n: >3}*π/{n}= {str(s.stack[-3]): <20}| arctan(tan(α))= {str(s.stack[-1]): <19}")

print("Test str to value",value("[None,4^2~3,True,'\\1\\55',\"test value()\",[False,0,\'abc\'],[0:\"0\",1:\"1\"] ,[type],{4}]"))# ,{₴}(→ @2 @2 + P p)
print("Test value to str to value")
print(none_(str_(none_(None))))
print(num_(str_(num_(2E3+5j))))
print(bool_(str_(bool_(True))))
print(bytes_(str_(bytes_([0,15,255,32767]))))
print(str_(str_(str_("abc"))))
print(list_(str_(list_([1,2,3]))))
print(dict_(str_(dict_({"a":1,"b":2,"c":3}))))
# print(function_(str_(function_({₴}(5→ @2 @2 + P p)))))
print(type_(str_(type_(num_))))
print(error_(str_(error_(0))))
print("Test value to python value to value")
print(num_(complex(num_(2E3+5j))))
print(bool_(bool(bool_(True))))
print(bytes_(bytes(bytes_([0,15,255,32767]))))
print(str_(str(str_("abc"))))
print(list_(list(list_([1,2,3]))))
print(dict_(dict(dict_({"a":1,"b":2,"c":3}))))