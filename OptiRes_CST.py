import os
os.chdir(r'C:\Users\alexa\OneDrive\Documents\PhD\PHD Phase\Year 1\Resonator Designs')
import res_shapes as rs
import gdspy
import numpy as np

#parameters (um)
w = 800
l_arm = 770
w_cap = 10
gap = 20
n = 10
r = 50
w_ind = 10
o_gap = 20

print("Overlap = {} \n".format(2*l_arm-w))

#setup the folder and gds 'cell'

poly_cell = gdspy.Cell('POLYGONS')
folder = r'C:\Users\alexa\OneDrive\Documents\PhD\PHD Phase\Year 1\Resonator Designs'
os.chdir(folder)

lens = np.linspace(1000, 10000, 10)

#ground plane + feedline
'''
bckgrnd = []
bckgrnd += [[(0, -300), (1000, -300), (1000, -50), (0, - 50)]]
bckgrnd += [[(0,0), (1000,0), (1000, 100), (0,100)]]
bckgrnd += [[(0,150), (1000,150), (1000, 170), (0,170)]]
bckgrnd += [[(0,170), (100,170), (100, 1170), (0,1170)]]
bckgrnd += [[(900,170), (900,1170), (1000, 1170), (1000,170)]]
bckgrnd += [[(0,1170), (1000,1170), (1000, 1370), (0,1370)]]
'''
#for i in bckgrnd:
#    poly_cell.add(gdspy.Polygon(i, 0))

#for gap in np.linspace(5,25,5):
#clear
poly_cell.polygons=[]
#sort out the ground plane, feedline etc
#for i in bckgrnd:
#    poly_cell.add(gdspy.Polygon(i, 0))

#add the resonator
#res = rs.interdig_optires(w,l_arm, w_cap, gap, n, r, w_ind,o_gap)
y0=0
res = rs.interdigital_capacitor(y0,w,l_arm,w_cap,gap,n)[0]
min_yr = min([min(i) for i in [[i[q][1] for q in range(len(i))] for i in res]])
max_yr = max([max(i) for i in [[i[q][1] for q in range(len(i))] for i in res]])
#res = [rs.move(i, 450,  220 - min_yr) for i in res]
res = [rs.move(i, 150 + 150,  220 - min_yr) for i in res]

for i in res:
    poly_cell.add(gdspy.Polygon(i, 1))

#y0 = max_yr - w_ind - r
#cover = rs.solidarc((l_arm+gap+w_cap)/2,y0,r,w_ind,o_gap)
#cover = [rs.move(i, 450,  220 - min_yr) for i in cover]
#cover = [rs.move(i,150 + n*150, 220 - min_yr) for i in cover]

#for i in cover:
#            poly_cell.add(gdspy.Polygon(i, 2))
#gdspy.write_gds('designs_for_fab_%d.gds'%gap, unit=1.0e-6, precision=1.0e-9)

#    poly_cell.polygons=[]
#    cap = rs.interdigital_capacitor(0,l_arm,w_cap,gap,n)
#for i in cap:
#        poly_cell.add(gdspy.Polygon(i, 1))

gdspy.write_gds('testing.gds')#%gap, unit=1.0e-6, precision=1.0e-9)

gdspy.LayoutViewer()
