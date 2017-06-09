import matplotlib.pyplot as plt
import numpy as np

def xsd(isotope):
    """
    Creates a dictionary containing both the fission and capture cross sections
    of various isotopes
    """
    
    #mo contains isotope names to be contained in the dictionary
    mo = [
        "Th_231", "Th_232", "Th_233", 
        "Pa_231", "Pa_232", "Pa_233",
        "U_232", "U_233", "U_234", "U_235", "U_236", "U_237", "U_238", "U_239",
        "Np_237", "Np_238", "Np_239", 
        "Pu_238", "Pu_239", "Pu_240",  "Pu_241", "Pu_242", "Pu_243",
        "Am_241", "Am_242_metastable", "Am_242", "Am_243", "Am_244",
        "Cm_242", "Cm_243", "Cm_244"
        ] 
    
    #Checks that input is contained in mo
    assert isotope in mo, "Isotope not considered"
    
    #d contains the fission and capture cross section information.
    d = {}
    for i in mo:
        energy = []
        xsection = []
        d[i] = {"capture":None,"fission":None}
        file = open(i + "_capture" + ".txt","r")
        for line in file.readlines()[1:]:
            energy.append(float(line.split(",")[0]))
            xsection.append(float(line.split(",")[1]))
        d[i]["capture"] = [energy,xsection]
        energy = []
        xsection = []
        file = open(i + "_fission" + ".txt","r")
        for line in file.readlines()[1:]:
            energy.append(float(line.split(",")[0]))
            xsection.append(float(line.split(",")[1]))
        d[i]["fission"] = [energy,xsection]      
    return(d)
    
def wxs(isotope,mode):
    """
    Calculates the weighted cross section for a triga reactor, as well 
    as plots cross section vs energy
    """   
    
    d = xsd(isotope)
    
    #Plots the cross section for the respective decay mode vs. energy.
    plt.plot(d[isotope][mode][0],d[isotope][mode][1])
    plt.yscale("log")
    plt.xscale("log")
    plt.ylabel("Cross Section(b)")
    plt.xlabel("Incedent Neutron Energy(eV)") 
    plt.show()
    plt.close()
    
    #Weighted cross section.
    E = np.loadtxt("energy_range")
    phi = np.loadtxt("flux")
    sigb = np.trapz(phi,E)
    sigx = np.interp(E,d[isotope][mode][0],d[isotope][mode][1])
    phisig = []
    for i in range(0,1000):
        phisig.append(phi[i]*sigx[i]) 
    sigt = np.trapz(phisig, E)
    wsig = sigt/sigb
    return(wsig)






