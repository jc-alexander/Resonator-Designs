import os
from Res_Shapes.res_shapes import resonators as rs
from Res_Shapes.res_shapes import shape_functions
import gdspy
import numpy as np


#parameters (um)
w_cap = 10
w_in  = 2
gap = 50
l_in = 500

#setup the folder and gds 'cell'

poly_cell = gdspy.Cell('POLYGONS')
folder = os.getcwd()
os.chdir(folder)

lens = np.linspace(1000, 10000, 10)

#ground plane + feedline
num_cells = 3
w_box = 3500
w_cell = w_box/num_cells

bckgrnd = [[(-2500,2500),(-2500,-2500),(2500,-2500),(2500,2500)]]

for i in range(num_cells):
    for j in range(num_cells):
        bckgrnd += [[(-w_box/2 + i*w_cell,w_box/2 - j*w_cell),\
        (-w_box/2 + i*w_cell,w_box/2 - (j+1)*w_cell),\
        (-w_box/2 + (i+1)*w_cell,w_box/2 - (j+1)*w_cell),\
        (-w_box/2 + (i+1)*w_cell,w_box/2 - (j)*w_cell)]]

for i in bckgrnd:
    poly_cell.add(gdspy.Polygon(i, 0))

l_in = [400,500,600]
gap = [25,50,75]
w = np.add(np.add(l_in,np.multiply(w_cap,3)),gap)

y0=0
N=0
for j in range(3):
    for k in range(3):
        res = rs.TRII(w_cap, w_in, l_in[j], gap[k])
        min_yr = min([min(i) for i in [[i[q][1] for q in range(len(i))] for i in res]])
        max_yr = max([max(i) for i in [[i[q][1] for q in range(len(i))] for i in res]])

        #res = [rs.move(i, 450,  220 - min_yr) for i in res]
        res = [shape_functions.move(i, -w_box/2 + w_cell/2 + k*w_cell - w[j]/2, w_box/2 - j*w_cell - w_cell/2 - max_yr/2) for i in res]

        for i in res:
            poly_cell.add(gdspy.Polygon(i, 1))

        N=N+1

gdspy.write_gds('test_TRII.gds')#%gap, unit=1.0e-6, precision=1.0e-9)

gdspy.LayoutViewer()
