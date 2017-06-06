# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
def cross_section(isotope, decay_mode, energy):
    Data = np.loadtxt(isotope+"_"+decay_mode+".txt",delimiter = ",",skiprows=1)
    Data = np.array_split(Data,2)
    for array in Data:
        if array[0][0] > energy:
            
        
    return(Data)
#    energy_list = []
#    xsection_list = []
#    location = []
#    file = open(isotope + "_" + decay_mode + ".txt","r")
#    for line in file.readlines():
#        energy_list.append(line.split(",")[0])
#        xsection_list.append(line.split(",")[1])
#    for i in range(1, len(energy_list)):
#        if energy > float(energy_list[i]):
#            location.append(1)
#    print(len(location)-1)
#    low = float(xsection_list[len(location)-1])
#    high = float(xsection_list[len(location)])
#    return(low, high)
