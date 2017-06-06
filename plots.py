# -*- coding: utf-8 -*-
"""
Created on Wed May 24 13:30:11 2017

@author: keith
"""
import numpy as np
#np.set_printoptions(threshold=np.inf)
import matplotlib.pyplot as plt
from scipy.integrate import odeint
#Isotopes considered are those listed in Neutron Physics by Paul Reuss in figures 12.2 and 12.3.
#Halflife Data from Chart of the Nuclides 17th Edition.
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
   
molwe = {#Contains the atomic numbers of the respective isotopes (used to convert between mass and number) 
    "Th_231": 231, "Th_232": 232, "Th_233": 233, 
    "Pa_231": 231, "Pa_232": 232, "Pa_233": 233,
    "U_232": 232, "U_233": 233, "U_234": 234, "U_235": 235, "U_236": 236, "U_237": 237, "U_238": 238, "U_239": 239,
    "Np_237": 237, "Np_238": 238, "Np_239": 239, 
    "Pu_238": 238, "Pu_239": 239, "Pu_240": 240, "Pu_241": 241, "Pu_242": 242, "Pu_243": 243,
    "Am_241": 241, "Am_242_metastable": 242, "Am_242": 242, "Am_243": 243, "Am_244": 244,
    "Cm_242": 242, "Cm_243": 243, "Cm_244": 244}
   
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
   
#None type used when isotope is not considered, not shown in figures 12.2 and 12.3
#Tranmutation Modes    
tm = {"Th_231": {"decay": "Pa_231", "capture": "Th_232"}, 
    "Th_232": {"decay": None, "capture": "Th_233"}, 
    "Th_233": {"decay": "Pa_233", "capture": None}, 
    "Pa_231": {"decay": None, "capture": "Pa_232"},
    "Pa_232": {"decay": "U_232", "capture": "Pa_233"}, 
    "Pa_233": {"decay": "U_233", "capture": None}, 
    "U_232": {"decay": None, "capture": "U_233"}, 
    "U_233": {"decay": None, "capture": "U_234"}, 
    "U_234": {"decay": None, "capture": "U_235"}, 
    "U_235": {"decay": "Th_231", "capture": "U_236"}, 
    "U_236": {"decay": "Th_232", "capture": "U_237"},
    "U_237": {"decay": "Np_237", "capture": "U_238"}, 
    "U_238": {"decay": None, "capture": "U_239"}, 
    "U_239": {"decay": "Np_239", "capture": None},
    "Np_237": {"decay": "Pa_233", "capture": "Np_238"}, 
    "Np_238": {"decay": "Pu_238", "capture": "Np_239"}, 
    "Np_239": {"decay": "Pu_239", "capture": None}, 
    "Pu_238": {"decay": "U_234", "capture": "Pu_239"},
    "Pu_239": {"decay": "U_235", "capture": "Pu_240"},         
    "Pu_240": {"decay": "U_236", "capture": "Pu_241"}, 
    "Pu_241": {"decay": "Am_241", "capture": "Pu_242"}, 
    "Pu_242":{"decay": "U_238", "capture": "Pu_243"},
    "Pu_243": {"decay": "Am_243", "capture": None}, 
    "Am_241": {"decay": "Np_237", "capture": {"mode1": "Am_242_metastable","mode2": "Am_242"}}, 
    "Am_242_metastable": {"decay": "Np_238", "capture": "Am_243"},
    "Am_242": {"decay": {"mode1": "Cm_242","mode2": "Pu_242"}, "capture": "Am_243"}, 
    "Am_243": {"decay": "Np_239", "capture": "Am_244"}, 
    "Am_244": {"decay": "Cm_244", "capture": None}, 
    "Cm_242":{"decay": "Pu_238", "capture": "Cm_243"}, 
    "Cm_243": {"decay": "Pu_239", "capture": "Cm_244"}, 
    "Cm_244": {"decay": "Pu_240", "capture": None}}

#Matrix Order
mo = ["Th_231", "Th_232", "Th_233", 
      "Pa_231", "Pa_232", "Pa_233",
      "U_232", "U_233", "U_234", "U_235", "U_236", "U_237", "U_238", "U_239",
      "Np_237", "Np_238", "Np_239", 
      "Pu_238", "Pu_239", "Pu_240",  "Pu_241", "Pu_242", "Pu_243",
      "Am_241", "Am_242_metastable", "Am_242", "Am_243", "Am_244",
      "Cm_242", "Cm_243", "Cm_244"] 

def number(isotope, mass_0, flux, time):
    #Calculates the initial amount of atoms of the listed isotope given mass
    no = [0]*31
    atomic_mass = molwe[isotope]
    Na = 0.6022E24
    N_0 = mass_0*(Na)/(atomic_mass)
    no[mo.index(isotope)] = N_0
    M = np.zeros((len(mo),len(mo)))#Creates a nxn matrix where n is the number of considered isotopes
    for i in range(0,len(mo)):
        #Creates the diagonal of the coefficient matrix of N, used to solve matrix*N = dN/dt
        M[i,i] = -np.log(2)/hl[mo[i]] - flux*(xs[mo[i]]["fission"]+xs[mo[i]]["capture"])*1E-24
        if tm[mo[i]]["decay"] != None:
            if len(tm[mo[i]]["decay"]) != 2:
                M[mo.index(tm[mo[i]]["decay"]), i] = np.log(2)/hl[mo[i]]
            else:#Americium 242 decays two different ways
                M[mo.index(tm[mo[i]]["decay"]["mode1"]), i] = 0.83*np.log(2)/hl[mo[i]]
                M[mo.index(tm[mo[i]]["decay"]["mode2"]), i] = 0.17*np.log(2)/hl[mo[i]]
        if tm[mo[i]]["capture"] != None:
            if len(tm[mo[i]]["capture"]) != 2:
                M[mo.index(tm[mo[i]]["capture"]), i] = flux*(xs[mo[i]]["capture"])*1E-24
            else:#Americium 241 captures into a metastable and an unstable isotope
                M[mo.index(tm[mo[i]]["capture"]["mode1"]), i] = 0.11*flux*(xs[mo[i]]["capture"])*1E-24
                M[mo.index(tm[mo[i]]["capture"]["mode2"]), i] = 0.89*flux*(xs[mo[i]]["capture"])*1E-24   
    def y_prime(y, time, M):#Solves the set of differential equations contained in the matrix M
        return(np.dot(M, y))
    sol = odeint(y_prime, no, time, args=(M,))
    return(sol)
def fission_rate(isotope, mass_0 = 1E-6, flux = 1E13, endtime = 3.1536E7):
    """Plots the fission rates for given initial conditions over a specified time."""
    time = np.linspace(0, endtime, 100)
    sol = number(isotope, mass_0, flux, time)
    for i in range(0, len(time)): #Converts the matrix containing number of atoms to fission rates.
        for j in range(0,len(sol[0])):
            sol[i][j] = sol[i][j]*flux*xs[mo[j]]["fission"]*10**-24
    fission = []    #Contains the fission contribution of each isotope at one time interval.
    fissionsum = [] #Contains the total fission contribution of all isotopes at each time interval.
    for i in range(0,len(time)):
        for j in range(0,len(sol[0])):
            fission.append(sol[i][j])
        fissionsum.append(sum(fission))
        fission = []
    #Will apply a legend entry if the isotope ever contributes at least 5% to total fission.
    sf = []#Stores Isotopes order number for the list "mo" if the above condition is met.
    for i in range(0,len(time)):
        for j in range(0,len(sol[0])):
            if sol[i][j] > 0.05*fissionsum[i]:
                sf.append(j)
    sf = list(set(sf))
    sol = sol[:,sf]#Deletes isotopes from the array if the 5% condition is not met.
    other = []     #Sums all isotope contributions that do not meet the 5% condition.
    for i in range(0,len(time)):
        temp = []  #Temporarily contains the element of the list "other" for each time interval.
        for j in range(0,len(sol[0])):
            temp.append(sol[i][j])
            temp = [sum(temp)]
        other.append(fissionsum[i]-temp[0])   
    legend = []    #Contains the titles that will be used in the legend
    for i in sf:   #Adds in the isotope names that met the 5% condition
        legend.append(mo[i])
    legend.append("Other")
    legend.append("Total")
    plot = plt.plot(time, sol,time,other,time,fissionsum,"k--")
    plt.legend(plot,legend,loc="center left",bbox_to_anchor=(1.0,0.5))
    plt.xlabel("Time(s)")
    plt.ylabel("Fission Rate(fissions/second)")
    plt.title("Initially 1 microgram of "+ str(isotope))
    plt.yscale("log")
    plt.show()
    plt.close()
def mass(isotope, mass_0 = 1E-6, flux = 1E13, endtime = 3.1536E7):
    #Calculates the mass (in micrograms) of each isotope for given initial conditions over time
    time = np.linspace(0, endtime, 100)
    sol = number(isotope, mass_0, flux, time)
    Na = 0.6022E24
    for i in range(0,len(time)):
        for j in range(0,len(sol[0])):
            sol[i][j] = sol[i][j]*molwe[mo[j]]/Na*10**6
    sm = []#Sufficient mass condition used to discriminate against isotopes of negligible mass
    for i in range(0,len(time)):
        for j in range(0,len(sol[0])):
            if sol[i][j] > 0.01:
                sm.append(j)
    sm = list(set(sm))
    legend = []
    for i in sm:
        legend.append(mo[i])
    sol = sol[:,sm]
    fig = plt.plot(time, sol)
    plt.xlabel("Time(s)")
    plt.ylabel("Mass(microgram)")
    plt.legend(fig,legend,loc="center left",bbox_to_anchor=(1.0,0.5))
    plt.title("Initially 1 microgram of "+str(isotope))
    plt.show()
    plt.close()
    
