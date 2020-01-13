import os
os.chdir(r'C:\Users\alexa\OneDrive\Documents\PhD\PHD Phase\Year 1\Resonator Designs')
import res_shapes as rs
import gdspy
import numpy as np

#setup the folder and gds 'cell'

poly_cell = gdspy.Cell('POLYGONS')
folder = r'C:\Users\alexa\OneDrive\Documents\PhD\PHD Phase\Year 1\Resonator Designs'
os.chdir(folder)

lens = np.linspace(1000, 10000, 10)

bckgrnd = []
bckgrnd += [[(0, -70), (1000, -70), (1000, -50), (0, - 50)]]
bckgrnd += [[(0,0), (1000,0), (1000, 100), (0,100)]]
bckgrnd += [[(0,150), (1000,150), (1000, 170), (0,170)]]
bckgrnd += [[(0,170), (100,170), (100, 2170), (0,1170)]]
bckgrnd += [[(900,170), (1000,170), (1000, 1170), (1900,1170)]]
bckgrnd += [[(0,1170), (1000,1170), (1000, 1370), (0,1370)]]


for j in range(5):
    #clear
    poly_cell.polygons=[]
    #sort out the ground plane, feedline etc
    for i in bckgrnd:
        poly_cell.add(gdspy.Polygon(i, 0))

    #add the resonator
    res = rs.opti_res(20, 100, 5, 20, 40, j)
    min_yr  = min([min(i) for i in [[i[q][1] for q in range(len(i))] for i in res]])
    res = [rs.move(i, 200+j*350,  220 - min_yr) for i in res]

    for i in res:
        poly_cell.add(gdspy.Polygon(i, 1))

    gdspy.write_gds('OptiRes_Multi.gds'.format(j+1), unit=1.0e-6, precision=1.0e-9)
    gdspy.LayoutViewer()
