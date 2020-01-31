import gds_to_patran
import calc_cap
import res_shapes as rs
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns

w = 1000
l_arm = 160
w_cap = 48
gap = 27
n = 5
r = 25
w_ind = 5
o_gap = 20
y0 = 0
x0 = 0
h = 0.05
'''
cap_array = []
arm_array = np.linspace(100,2000,10)
i = 0
j = 0
k=1
max_n = 100
samples = 10
freq_array = np.zeros((max_n,len(arm_array)))
ns = np.linspace(1,10,samples)

for l_arm in arm_array:
    i=0
    for n in ns:
        #print("\nCreating Design...")
        print("\n{}/{}".format(k,len(ns)*len(arm_array)))

        #print("\nCreating Design...\n")
        capacitor = rs.capacitance_calc(y0,w,l_arm,w_cap,gap,n)[0]
        inductor = rs.solidarc(x0,y0,r,w_ind,o_gap)
        inductor = inductor[0][0:int(len(inductor[0])/2)]
        #print("\nCalaculating Capacitance using Fastercap...")
        gds_to_patran.capacitance_setup(capacitor)
        cap = calc_cap.calc_cap()*1e-3
        #print("\nCapacitance is {} pF\n".format(cap*1e15))
        #print("\nCalaculating Inductance using FastHenry...")
        gds_to_patran.inductance_setup(inductor,w_ind,h)
        ind = (calc_cap.calc_ind())
        #print("\nInductance is {} nH\n".format(ind*1e9))
        f = (1/(2*np.pi))*(1/np.sqrt(cap*ind))
        f=f*1e-9
        #print("\nCalculated Frequency: {} GHz\n".format(f*1e-9))

        freq_array[i,j] = abs(5-f)
        k+=1
        i+=1
    j+=1

plt.clf()
plt.imshow(freq_array)
plt.colorbar()
plt.show()

ax = sns.heatmap(freq_array)
'''

def run_sim(w,l_arm,w_cap,gap,n,r,w_ind,o_gap,y0,x0,h):
        #print("\nCreating Design...\n")
        capacitor = rs.capacitance_calc(y0,w,l_arm,w_cap,gap,n)[0]
        inductor = rs.solidarc(x0,y0,r,w_ind,o_gap)
        inductor = inductor[0][0:int(len(inductor[0])/2)]
        #print("\nCalaculating Capacitance using Fastercap...")
        gds_to_patran.capacitance_setup(capacitor)
        cap = calc_cap.calc_cap()*1e-3
        #print("\nCapacitance is {} pF\n".format(cap*1e15))
        #print("\nCalaculating Inductance using FastHenry...")
        gds_to_patran.inductance_setup(inductor,w_ind,h)
        ind = (calc_cap.calc_ind())
        #print("\nInductance is {} nH\n".format(ind*1e9))
        f = (1/(2*np.pi))*(1/np.sqrt(cap*ind))
        f=f*1e-9
        #print("\nCalculated Frequency: {} GHz\n".format(f*1e-9))

        return abs(5-f)

if __name__ == "__main__":

    print("\nCreating Design...\n")
    capacitor = rs.capacitance_calc(y0,w,l_arm,w_cap,gap,n)[0]
    inductor = rs.solidarc(x0,y0,r,w_ind,o_gap)
    inductor = inductor[0][0:int(len(inductor[0])/2)]
    print("\nCalaculating Capacitance using Fastercap...")
    gds_to_patran.capacitance_setup(capacitor)
    cap = calc_cap.calc_cap()*1e-3
    print("\nCapacitance is {} pF\n".format(cap*1e15))
    print("\nCalaculating Inductance using FastHenry...")
    gds_to_patran.inductance_setup(inductor,w_ind,h)
    ind = (calc_cap.calc_ind())
    print("\nInductance is {} nH\n".format(ind*1e9))
    f = (1/(2*np.pi))*(1/np.sqrt(cap*ind))
    print("\nCalculated Frequency: {} GHz\n".format(f*1e-9))
