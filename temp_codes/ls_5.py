# -*- coding: utf-8 -*-

import numpy
import scipy.special
import scipy.optimize

def lin_sourc_r(x,t,p):
    """
    The heat transfer model for line sources
    """
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
    interm2=numpy.zeros(len(t))
    for cnt in range(len(t)):
        if cnt<ind:
            interm2[cnt]=numpy.inf
        else:
            interm2[cnt]=r_sq/(4*kapa*(t[cnt]-t0))

    

    const=q/(4*numpy.pi*lamda)
    
    term1=scipy.special.expn(1,interm1)
    term2=scipy.special.expn(1,interm2)
    term=term1-term2
    res=const*term

    return res

def objective(x,t,p,y0,func):
    return y0 - func(x,t,p)

class Model:
    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return "A model computed with %d"%(self._name)

def line_source(data_set,
                t0=8,
                q=85,
                rho=1000,
                lamda=0.6,
                c=4174,
                r=0.006):
    """

    Examples::

        >>> import sys
        >>> sys.path.append(".")
        >>> from temp_codes.data_set import DataSet
        >>> from temp_codes.ls_5 import line_source
        >>> data_set = DataSet("temp_codes/agar_data_try.dat")
        >>> model = line_source(data_set, q=140.8)
        >>> model.fit_optimized_parameters
        array([ 0.00662857])
        >>> print(model.mesg)
        Both actual and predicted relative reductions in the sum of squares
          are at most 0.000000
    """

    model = Model("line_source")
    model.kapa=lamda/(rho*c)
    model.r_sq=r**2

    parameters = [t0,q,rho,c,lamda]
    times = numpy.asarray(data_set.times)

    # Could be extracted in a separate function that builds a synthetic data set
    if data_set.temperature_responses is None:
        #t0,q,rho,c,lamda=p
        y_noer=lin_sourc_r(r,times,parameters)
        er=0.01*numpy.random.standard_normal(len(times))
        temperature_responses = y_noer+er

    temperature_responses = numpy.asarray(data_set.temperature_responses)
    heat_transfer_model   = lin_sourc_r

    # Compute the inversion
    args = (times, parameters, temperature_responses, heat_transfer_model)
    x0=0.005
    #r_fit, cov_x, infodict, mesg, ier = scipy.optimize.minpack.leastsq(objective,x0,args=param,full_output=True,warning=True)
    model.fit_optimized_parameters, cov_x, model.infodict, model.mesg, ier = scipy.optimize.minpack.leastsq(
        objective, x0, args=args, full_output=True)
    #print r_fit

    model.fit_temperature_responses = heat_transfer_model(model.fit_optimized_parameters, times, parameters)
    model.times = times

    return model

