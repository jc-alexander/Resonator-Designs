import subprocess

def calc_cap():
    fname = "cap_output.txt"

    file = open(fname,"w")
    file.truncate(0)
    file.close()

    #subprocess.run(["cd C:/Users/alexa/OneDrive/Documents/PhD/PHD Phase/Year 1/Resonator Designs/"],shell=True)
    subprocess.run(["cscript","fcdriv.vbs",">","cap_output.txt"],shell=True)

    file = open(fname,"r")
    lines=file.readlines()

    cap = lines[3]
    cap = cap.replace('\n','')
    cap = float(cap)
    file.close()
    return cap

def calc_ind():
    fname = "ind_output.txt"

    file = open(fname,"w")
    file.truncate(0)
    file.close()

    subprocess.run(["cscript","fhdriv.vbs",">","ind_output.txt"],shell=True)

    file = open(fname,"r")
    lines=file.readlines()

    ind = lines[3]
    ind = ind.replace('\n','')
    ind = float(ind)
    file.close()
    return ind
