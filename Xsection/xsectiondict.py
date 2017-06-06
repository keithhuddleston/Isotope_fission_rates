# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib.pyplot as plt
mo = ["Th_231", "Th_232", "Th_233", 
      "Pa_231", "Pa_232", "Pa_233",
      "U_232", "U_233", "U_234", "U_235", "U_236", "U_237", "U_238", "U_239",
      "Np_237", "Np_238", "Np_239", 
      "Pu_238", "Pu_239", "Pu_240",  "Pu_241", "Pu_242", "Pu_243",
      "Am_241", "Am_242_metastable", "Am_242", "Am_243", "Am_244",
      "Cm_242", "Cm_243", "Cm_244"] 
dict = {}
for i in mo:
    energy = []
    xsection = []
    dict[i] = {"capture":None,"fission":None}
    file = open(i + "_capture" + ".txt","r")
    for line in file.readlines():
        energy.append(line.split(",")[0])
        xsection.append(line.split(",")[1])
    dict[i]["capture"] = [energy,xsection]
    energy = []
    xsection = []
    file = open(i + "_fission" + ".txt","r")
    for line in file.readlines():
        energy.append(line.split(",")[0])
        xsection.append(line.split(",")[1])
    dict[i]["fission"] = [energy,xsection]      
#dict["U_235"]["capture"][0] gives the energy list of U_235 for capture
#dict["U_235"]["fission"][1] gives the xsection list of U_235 for fission
plt.plot(dict["U_238"]["capture"][0][1::],dict["U_238"]["capture"][1][1::])
plt.yscale("log")
plt.xscale("log")
plt.ylabel("Cross Section(b)")
plt.xlabel("Incedent Neutron Energy(eV)")