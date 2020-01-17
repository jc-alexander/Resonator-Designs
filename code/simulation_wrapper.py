from qsd_gpm.remote_interface import remote_interface
from postprocess import postprocess
from preprocess import preprocess
import os

def changeparamsfile(paramfile,w,r,t,pen,omega,Z):
    f = open(paramfile,'w')
    f.write('w = {}\n \
             r = {}\n \
             t = {}\n \
             pen = {}\n \
             omega = {}\n \
             Z = {}\n \
             '.format(w_ind,r,t,pen,omega,Z))
    f.close()

def within_frequency_bounds(frequency, clock_transition, leeway):
    return (frequency > (clock_transition-leeway)) and (frequency < (clock_transition+leeway))

def dist_from_clock(frequency, clock_transition):
    distance = abs(frequency-clock_transition)
    return distance

def simulation_wrapper_noparams(host, COMSOL_model, paramfile):
    #CST

    #Preprocessing - calculate current distribution
    current_density_file, paramfile, frequency = preprocess(paramfile)
    if frequency > 6.5e09 and frequency < 7.5e09:
        return 0 # Negative as want to optimize against this
    else:
        return -dist_from_clock(frequency, 7.03e09)
        # #COMSOL simulation
        # remote_interface(host, COMSOL_model, paramfile, current_density_file)
        # #Postprocess - generate g_ens and pi_fidelity
        # file_gens2_number = os.getcwd() + '/downloads/exports/g_ens2_number.csv'
        # g_ens, FWHM = postprocess(file_gens2_number)
        # return (g_ens, FWHM)

def simulation_wrapper(host, COMSOL_model, paramfile, w, t, l, pen, omega, gap_cap, w_cap, l_cap, w_mesa, h_mesa, gap_ind):
    changeparamsfile(paramfile, w, t, l, pen, omega, gap_cap, w_cap, l_cap, w_mesa, h_mesa, gap_ind)
    g_ens = simulation_wrapper_noparams(host, COMSOL_model, paramfile)
    return g_ens

if __name__ == "__main__":
    host = 'monaco'
    COMSOL_model = 'ART_res.mph'
    # paramfile = 'paramlist.txt'
    # current_density_file = "current_density.csv"
    file_gens2 = os.getcwd() + '/downloads/exports/g_ens2.csv'
    file_gens2_number = os.getcwd() + '/downloads/exports/g_ens2_number.csv'
    file_N = os.getcwd() + '/downloads/exports/N.csv'
    gens, FWHM = simulation_wrapper_noparams(host, COMSOL_model, "cpw_parameters.txt")
    print(gens)
