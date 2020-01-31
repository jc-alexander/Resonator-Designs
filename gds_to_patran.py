import numpy as np
import res_shapes as rs

def clear_file(fname):
    file = open(fname,"w")
    file.truncate(0)
    return 0

def draw_grid(fname,shape):
    file = open(fname,"w")
    n = 1
    for points in shape:
        for coords in points:
            x = coords[0]
            y = coords[1]
            file.write("GRID, {}, , {}/{}/0\n".format(n,x,y))
            n=n+1
    file.close()
    return 0

def draw_shape(fname,shape):
    file = open(fname,"w")
    a = 1
    b = 2
    c = 3
    d = 4
    n = 1
    for points in shape:
        file.write("PATCH, {}, QUAD, , {}/{}/{}/{}\n".format(n,a,b,c,d))
        a+=4
        b+=4
        c+=4
        d+=4
        n+=1

    file.write("SET, ACTIVE, NONE\n")
    file.write("PATCH, 1, PLOT\nNAME, CONDUCTOR1\nPATCH, 1, ERASE\n\nPATCH, {}, PLOT\nNAME, CONDUCTOR2\nPATCH, {}, ERASE\n".format(len(shape),len(shape)))
    file.write("SET, ACTIVE, ALL\n")
    file.close()
    return 0

def mesh_shape(shape):
    fname = "capacitor.qui"
    file = open(fname,"w")
    a = 1
    b = 2
    c = 3
    d = 4
    n = 1
    for points in shape:
        file.write("MESH, P{}T{}, QUAD/4/0, LENGTH, 1.0\n".format(a,d))
        a+=4
        b+=4
        c+=4
        d+=4
        n+=1

    file.close()
    return 0


def capacitance_setup(shape):
    fname = "capacitor.qui"
    file = open(fname,"w")
    file.truncate(0)
    file.write("0 capacitor\n")
    for points in shape:
        file.write("Q   1   {} {} 0 {} {} 0 {} {} 0 {} {} 0\n".format(points[0][0],points[0][1],
        points[1][0],points[1][1],
        points[2][0],points[2][1],
        points[3][0],points[3][1]))
    file.close()
    return 0

def inductance_setup(shape,w,h):
    fname = "inductance.inp"
    file = open(fname,"w")
    file.truncate(0)
    file.write("*INDUCTOR\n")
    file.write(".Units UM\n")
    file.write(".Default z=0 sigma=1e9\n")
    n=1
    for points in shape:
        x=points[0]
        y=points[1]
        file.write("N{} x={} y={}\n".format(n,x,y))
        n+=1
    n=1

    for points in shape[:-1]:
        file.write("E{} N{} N{} w={} h={}\n".format(n,n,(n+1),w,h))
        n+=1

    file.write(".external N{} N{}\n".format(1,int(len(shape))))
    file.write(".freq fmin=1e9 fmax=20e9 ndec=21\n")
    file.write(".end")
    file.close()

    return 0
'''
def draw_shape(shape):
    file = open("capacitor.txt","w")

    n = 1
    for i in range(shape):
        file.write("PATCH, {}, QUAD, ,{}/{}/{}/{}\n".format(n,shape[i][0],shape[i][1],shape[i][2],shape[i][3])

    return 0
'''
'''
if __name__ == "__main__":

    fname = "capacitor.qui"

    shape = rs.interdigital_capacitor(y0,w,l_arm,w_cap,gap,n)[0]

    #clear_file(fname)
    #draw_grid(fname,shape)
    #draw_shape(fname,shape)

    make_list(fname,shape)
'''
