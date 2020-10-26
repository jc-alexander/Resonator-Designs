import os
os.chdir(r'C:\Users\alexa\OneDrive - University College London\PhD\PHD Phase\Year 1\Resonator Designs')
import res_shapes as rs
import gdspy
import numpy as np

#parameters (um)
w = 10
gap = 20
l_straight = 500
l_tot = 10000

#setup the folder and gds 'cell'

poly_cell = gdspy.Cell('POLYGONS')
folder = r'C:\Users\alexa\OneDrive - University College London\PhD\PHD Phase\Year 1\Resonator Designs'
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


l_tots = np.array([5000,5250,5500,
        8000,8250,8500,
        10000,10250,10500])
def len_spiral(w, gap, l_straight, n):
    turns = np.arange(1, n+1, 1)
    turn_len = np.pi*(2*turns*(gap + w) - 3*w/2. + gap/2.)
    return 2*n*l_straight + np.sum(turn_len)
ns = []
l = 0
for l_tot in l_tots:
    n=0
    while l < l_tot:
        n += 1
        l = len_spiral(w, gap, l_straight, n)
    n -= 1 # work out how may full turns we need.
    lres = l_tot - len_spiral(w, gap, l_straight, n)
    ns.append(n)
y0=0
N=0

ws = 0
box_num=0
for j in range(3):
    for k in range(3):
        res = rs.gavin_spiral(w, gap, l_straight, l_tots[box_num])
        min_yr = min([min(i) for i in [[i[q][1] for q in range(len(i))] for i in res]])
        max_yr = max([max(i) for i in [[i[q][1] for q in range(len(i))] for i in res]])

        #res = [rs.move(i, 450,  220 - min_yr) for i in res]
        res = [rs.move(i, -w_box/2 + w_cell/2 + k*w_cell, w_box/2 - j*w_cell - w_cell/2 - max_yr/2-min_yr/2) for i in res]

        for i in res:
            poly_cell.add(gdspy.Polygon(i, 1))

        N=N+1
        box_num+=1

gdspy.write_gds('test_spiral.gds')#%gap, unit=1.0e-6, precision=1.0e-9)

gdspy.LayoutViewer()
