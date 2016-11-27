import os
import sys

#from numpy import *
import numpy
from pylab import *
import scipy.special
import scipy.optimize

def lin_sourc_r(x,t,p):
    t0,q,rho,c,lamda=p
    kapa=lamda/(rho*c)
    r_sq=x**2
    
    cond=0
    cnt=-1

    while cond!=1:
        cnt=cnt+1
        if t[cnt]>t0:
            ind=cnt
            cond=1

    interm1=r_sq/(4*kapa*t)
    interm2=zeros(len(t))
    for cnt in range(len(t)):
        if cnt<ind:
            interm2[cnt]=inf
        else:
            interm2[cnt]=r_sq/(4*kapa*(t[cnt]-t0))

    

    const=q/(4*pi*lamda)
    
    term1=scipy.special.expn(1,interm1)
    term2=scipy.special.expn(1,interm2)
    term=term1-term2
    res=const*term

    return res

def objective(x,t,p,y0,func):
    return y0 - func(x,t,p)


t0=8
tim=r_[1:180:0.5]

q=85
rho=1000
lamda=0.6
c=4174
kapa=0.6/(rho*c)
r=0.006
r_sq=r**2

#t0,q,rho,c,lamda=p
p=[t0,q,rho,c,lamda]

y_noer=lin_sourc_r(r,tim,p)
er=0.01*numpy.random.standard_normal(len(tim))
y_er=y_noer+er

function=lin_sourc_r
param=(tim,p,y_er,function)
x0=0.005
r_fit, cov_x, infodict, mesg, ier = scipy.optimize.minpack.leastsq(objective,x0,args=param,full_output=True,warning=True)
print r_fit

y_fit=lin_sourc_r(r_fit,tim,p)

plot(tim,y_er,'.')
plot(tim,y_fit,'r')
xlabel('Time (sec)')
ylabel('$\Delta$ T (\xb0C)')
text(t0+50,0.1,r_fit)

show()