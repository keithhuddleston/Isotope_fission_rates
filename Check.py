#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 10:10:56 2017

@author: keith
"""

import matplotlib.pyplot as plt
import numpy as np 
from sympy import *
init_printing()

flux = 1E13
x,x2,t,C1,C2 = symbols(("x","x2","t","C1","C2"))
hl = {#Contains the half lives of varius isotopes.
    "Th_231": 1.063*8.64E4, "Th_232": 1.40e10*3.1536E7, "Th_233": 21.83*60,
    "Pa_231": 3.28E4*3.1536E7, "Pa_232": 1.32*8.64E4, "Pa_233": 26.967*8.64E4,
    "U_232": 69.8*3.1536E7, "U_233": 1.592E5*3.1536E7, "U_234": 2.46E5*3.1536E7, 
    "U_235": 7.04E5*3.1536E7, "U_236": 2.342E7*3.1536E7, "U_237": 6.752*8.64E4, 
    "U_238": 4.468E9*3.1536E7, "U_239": 23.47*60,
    "Np_237": 2.14E6*3.1536E7, "Np_238": 2.103*8.64E4, "Np_239": 2.356*8.64E4, 
    "Pu_238": 87.7*3.1536E7, "Pu_239": 2.410E4*3.1536E7, "Pu_240": 6.56E3*3.1536E7,
    "Pu_241": 14.29*3.1536E7, "Pu_242": 3.75E5*3.1536E7, "Pu_243": 4.956*3600, 
    "Am_241": 432.7*3.1536E7, "Am_242_metastable": 141*3.1536E7, "Am_242": 16.02*3600,
    "Am_243": 7.37E3*3.1536E7, "Am_244": 10.1*3600,
    "Cm_242": 162.8*8.64E4,"Cm_243": 29.1*3.1536E7,"Cm_244": 18.1*3.1536E7}
   
#Cross Section Data from Brookhaven National Laboratory Website.
xs = {#Contains the cross sections of varius isotopes when incident neutrons are at 0.0253 ev.
    "Th_231": {"capture": 1630.76,"fission": 40.0085}, 
    "Th_232": {"capture": 7.37062,"fission": 0}, 
    "Th_233": {"capture": 1290.6,"fission": 15.0059}, 
    "Pa_231": {"capture": 201.206,"fission": 0.020911}, 
    "Pa_232": {"capture": 590.973,"fission": 1491.6}, 
    "Pa_233": {"capture": 42.7054,"fission": 0}, 
    "U_232": {"capture": 75.7322,"fission": 76.8539}, 
    "U_233": {"capture": 45.3734,"fission": 532.707}, 
    "U_234": {"capture": 101.314,"fission": 0.073664},  
    "U_235": {"capture": 98.7947,"fission": 585.472}, 
    "U_236": {"capture": 4.15817,"fission": 0.0473308}, 
    "U_237": {"capture": 454.082,"fission": 1.70884},
    "U_238": {"capture": 2.69447,"fission": 1.68688E-5}, 
    "U_239": {"capture": 22.424,"fission": 14.3092}, 
    "Np_237": {"capture": 175.973,"fission": 0.0280143}, 
    "Np_238": {"capture": 481.949,"fission": 2211.0},
    "Np_239": {"capture": 45.014,"fission": 0.0280143}, 
    "Pu_238": {"capture": 413.31,"fission": 17.7872}, 
    "Pu_239": {"capture": 271.803,"fission": 751.322},  
    "Pu_240": {"capture": 288.5,"fission": 0.0642595}, 
    "Pu_241": {"capture": 363.414,"fission": 1013.11},  
    "Pu_242": {"capture": 21.3302,"fission": 0.013863}, 
    "Pu_243": {"capture": 88.3989,"fission": 181.996}, 
    "Am_241": {"capture": 684.874,"fission": 3.1258}, 
    "Am_242_metastable": {"capture": 1234.21,"fission": 6415.92}, 
    "Am_242": {"capture": 219.925,"fission": 2103.69}, 
    "Am_243": {"capture": 80.7365,"fission": 0.0816593}, 
    "Am_244": {"capture": 600.162,"fission": 2300.74}, 
    "Cm_242": {"capture": 19.2054,"fission": 4.68339}, 
    "Cm_243": {"capture": 131.96,"fission": 589.769}, 
    "Cm_244": {"capture": 15.2818,"fission": 1.02554}}

fun = Eq(x(t).diff(t),-np.log(2)/hl["U_235"]*x(t) - flux*(xs["U_235"]["capture"]+xs["U_235"]["fission"])*10**-24*x(t))
sol = dsolve(fun,x(t))
solsub = sol.subs(C1, 1E-6)
fun2 = Eq(x2(t).diff(t),-np.log(2)/hl["U_236"]*x2(t) - flux * (xs["U_236"]["capture"] + xs["U_236"]["fission"])*10**-24 * x2(t) + solsub.rhs*flux*xs["U_235"]["capture"]*10**-24)
sol2 = dsolve(fun2,x2(t))
C = sol2.subs(t,0)
C = Eq(C.rhs)
C = solve(C)
sol2sub = sol2.subs(C1, C[0])