#!/usr/bin/env python
import csv
import os
import numpy as np
from qsd.electromagnetics import cpw
from qsd.data_processing import setparams


setp = setparams.SetParams()
params = setp.set_params("cpw_parameters.txt")

w = params["w"]
t = params["t"]
l = params["l"]
pen = params["pen"]
omega = params["omega"]
Z = params["Z"]


x = np.linspace(-w, w, int(1e04))

# Instantiate Special CPW object
cpw = cpw.CPW(x,l,w,t,pen,Z,omega)

Js = cpw.J() #s Current density - not normalised
Jnorm = cpw.normalize_J() # Normalise
I = cpw.current(norm='no') # Find the current

# Generate a parameter list for COMSOL modelling
paramlist = setp.param_list(x,I,Jnorm,'paramlist.txt') # Generate COMSOL parameter list

currentDensityFile = str(os.getcwd() + "/current_density.csv")
np.savetxt(currentDensityFile, np.column_stack((x,Jnorm)), delimiter=",")

currentFile = str(os.getcwd() + "/current.csv")
np.savetxt(currentFile, np.column_stack((x,I)), delimiter=",")
