import os
from Res_Shapes.res_shapes import resonators as rs
from Res_Shapes.res_shapes import shape_functions
import gdspy
import numpy as np

#parameters (um)
w = 800
l_arm = 750
w_cap = 10
gap = 20
n = 6
r = 25
w_ind = 10
o_gap = 10
y0 = 0
x0 = 0
h = 0.05

#[1078.70563062  593.23851316   12.03210642   23.25091154   10.05007889
#   23.30964139   22.05411696   18.86348486]

print("Overlap = {} \n".format(2*l_arm-w))

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

#for gap in np.linspace(5,25,5):
#clear
#poly_cell.polygons=[]
#sort out the ground plane, feedline etc
#for i in bckgrnd:
#    poly_cell.add(gdspy.Polygon(i, 0))

#add the resonator
#res = rs.interdig_optires(w,l_arm, w_cap, gap, n, r, w_ind,o_gap)
#w = [1000,1050,1100,750,800,850,300,350,400]
w = [300,1000,750,350,1050,800,400,1100,850]
l_arm = [250,950,700,300,1000,750,350,1050,800]

y0=0
N=0
for j in range(3):
    for k in range(3):
        res = rs.interdig_optires(w[N],l_arm[N],w_cap,gap,n,r,w_ind,o_gap)
        min_yr = min([min(i) for i in [[i[q][1] for q in range(len(i))] for i in res]])
        max_yr = max([max(i) for i in [[i[q][1] for q in range(len(i))] for i in res]])

        #res = [rs.move(i, 450,  220 - min_yr) for i in res]
        res = [shape_functions.move(i, -w_box/2 + w_cell/2 + k*w_cell - w[N]/2, w_box/2 - j*w_cell - w_cell/2 - max_yr/2) for i in res]

        for i in res:
            poly_cell.add(gdspy.Polygon(i, 1))

        N=N+1

gdspy.write_gds('test_optires.gds')#%gap, unit=1.0e-6, precision=1.0e-9)

gdspy.LayoutViewer()
