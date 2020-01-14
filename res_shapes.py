import numpy as np

def move(shape, dx, dy):
    return [(i[0] + dx, i[1] + dy) for i in shape]

def flip(shape, axis='y'):
    if axis =='y':
        return [(i[0], -i[1]) for i in shape]
    elif axis =='x':
        return [(-i[0], i[1]) for i in shape]

def circ_arc(r, x0, y0, n=50, theta0=0, thetaf=np.pi/2):
    '''
    List of tuples giving x, y coords of a circular arc from theta_0 to theta_f
    with centre at (x0, y0) and radius r.
    '''
    return [(r*np.cos(i) + x0, r*np.sin(i) + y0) for i in np.linspace(theta0, thetaf, n)]

def halfarc(r, w, x0, y0, orientation='E', npoints=40):
    '''
    List of tuples.
    A half circle trench of width w, the inner side of which is a circle with
    radius r and centre (x0, y0). Different orientations of points of compass
    with 'N' meaning that the semicircle is an arc that looks like a rainbow.
    '''
    if orientation == 'N':
        t0=0
        tf=np.pi
    elif orientation == 'E':
        t0=-np.pi/2
        tf=np.pi/2
    elif orientation == 'W':
        t0=np.pi/2
        tf=3*np.pi/2
    elif orientation == 'S':
        t0=np.pi
        tf=2*np.pi

    inner = circ_arc(r, x0, y0, n=npoints, theta0=t0, thetaf=tf)
    outer = circ_arc(r + w, x0, y0, n=npoints, theta0=t0, thetaf=tf)[::-1]

    return inner + outer

def halfarc_trench(r, width, gap, x0, y0, orient='E', npoints=40):
    inside = halfarc(r, gap, x0, y0, orientation=orient, npoints=npoints)
    outside = halfarc(r + gap + width, gap, x0, y0, orientation=orient, npoints=npoints)
    return [inside, outside]

def quarterarc(r, w, x0, y0, orientation='NE', npoints=20):
    if orientation == 'NE':
        t0=0
        tf=np.pi/2
    elif orientation == 'SE':
        t0=3*np.pi/2
        tf=2*np.pi
    elif orientation == 'SW':
        t0=np.pi
        tf=3*np.pi/2
    elif orientation == 'NW':
        t0=np.pi/2
        tf=np.pi

    inner = circ_arc(r, x0, y0, theta0=t0, thetaf=tf, n=npoints)
    outer = circ_arc(r + w, x0, y0, theta0=t0, thetaf=tf, n=npoints)[::-1]

    return inner + outer

def arbarc(r, w, x0, y0, t0, tf, npoints=20):
    inner = circ_arc(r, x0, y0, theta0=t0, thetaf=tf, n=npoints)
    outer = circ_arc(r + w, x0, y0, theta0=t0, thetaf=tf, n=npoints)[::-1]

    return inner + outer

def quarterarc_trench(r, width, gap, x0, y0, orient='NE', npoints=20):
    inside = quarterarc(r, gap, x0, y0, orientation=orient, npoints=npoints)
    outside = quarterarc(r + gap + width, gap, x0, y0, orientation=orient, npoints=npoints)
    return [inside, outside]

def rect(w, l, x0, y0):
    '''
    List of tuples
    Recangle of width and length w and l with bottom left corner at (x0, y0).
    '''
    return [(x0, y0), (x0 + w, y0), (x0 + w, y0 + l), (x0, y0 + l)]

def straight_trench(l, gap, w, x0, y0, orientation='H'):
    if orientation == 'H':
        return [rect(l, gap, x0, y0), rect(l, gap, x0, y0 + gap + w)]
    if orientation == 'V':
        return [rect(gap, l, x0, y0), rect(gap, l, x0 + gap + w, y0)]

def thinning_trench(w1, w2, gap, x0, y0, orientation='V'):
    '''
    list of list of tuples
    '''
    w1 = float(w1)
    w2 = float(w2)
    if w1 > w2:
        d1 = [(x0, y0), (x0, y0 +  w1), (x0 + gap, y0 + w1), (x0 + gap + (w1 - w2)/2, y0)]
        d2 = [(x0 + w1 + 2*gap, y0), (x0 + w1 + 2*gap, y0 +  w1), (x0 + w1 + gap, y0 + w1), (x0 + gap + (w1 - w2)/2 + w2, y0)]
    else:
        d1 = [(x0, y0 - w2), (x0, y0 ), (x0 + gap + (w2 - w1)/2, y0 ), (x0 + gap , y0 - w2)]
        d2 = [(x0 + w2 + 2*gap, y0 - w2), (x0 + w2 + gap, y0 - w2), (x0 + gap + (w2 - w1)/2 + w1, y0), (x0 + w2 +2*gap, y0)]
    return [d1, d2]

def thinning_trench_style_2(w1, w2, rat, x0, y0, H):
    '''
    list of list of tuples
    '''
    w1 = float(w1)
    w2 = float(w2)
    d1 = [(x0, y0), (x0 + w1*rat, y0), (x0 + w1*(rat + .5) - w2*.5, y0 + H), (x0 + w1*(rat + .5) - w2*(rat + .5), y0 + H)]
    d2 = [(x0 + w1*(1 + rat), y0), (x0 + w1*(1 + 2*rat), y0), (x0 + w1*(rat + .5) + w2*(rat + .5), y0 + H), (x0 + w1*(rat + .5) + w2*.5, y0 + H)]
    return [d1, d2]

def quarterwave(w, gap, nturns, lcap, lmeander, r, tail=True, ltail=100,
                constriction=True, constrictionw=1, constrictionr=.5, spacer=5,
                SQUID=True, SQUID_H=2, SQUID_r = .8, SQUID_constriction=0.5,
                flip_y='False', d_dots=5, SQUID_con_H=.2):
    '''
    List of list of list of tuples.
    There are two lists denoting different parts of the resonator. One list is
    the capacitor, meanders and part of the tail. Second list contains the fine
    shapes. This allows these to be saved to different laye
    '''
    cap = straight_trench(lcap, gap, w, gap, 0) + [rect(gap, 2*gap + w, 0, 0)]
    remove = [rect(gap + d_dots, 2*gap + w + 2*d_dots, - d_dots, -d_dots)]
    remove += [rect(lcap, 2*(gap + d_dots) + w, gap, -d_dots)]
    arccentre = [gap + lcap, -r]
    meanders = []
    for turn in range(nturns):
        if turn%2 == 0:
            o = 'E'
            meanders += halfarc_trench(r, w, gap, arccentre[0], arccentre[1], orient=o)
            remove += [halfarc(r - d_dots, w + 2*gap + 2*d_dots, arccentre[0], arccentre[1], orientation=o)]
            meanders += straight_trench(lmeander, gap, w, arccentre[0] - lmeander, arccentre[1] - r - 2*gap - w)
            remove += [rect(lmeander, 2*gap + w + 2*d_dots, arccentre[0] - lmeander, arccentre[1] - r - 2*gap - w - d_dots)]
            arccentre = [arccentre[0] - lmeander, arccentre[1] - 2*r - 2*gap - w]
        elif turn%2 == 1:
            o = 'W'
            meanders += halfarc_trench(r, w, gap, arccentre[0], arccentre[1], orient=o)
            remove += [halfarc(r - d_dots, w + 2*gap + 2*d_dots, arccentre[0], arccentre[1], orientation=o)]
            meanders += straight_trench(lmeander, gap, w, arccentre[0], arccentre[1] -r -2*gap - w)
            remove += [rect(lmeander, 2*gap + w + 2*d_dots, arccentre[0], arccentre[1] -r -2*gap - w - d_dots)]
            arccentre = [arccentre[0] + lmeander, arccentre[1] - 2*r - 2*gap - w]
    tail_shapes = []
    fine_shapes = []
    if tail == True:
        if nturns%2 == 0:
            o = 'NE'
        elif nturns%2 == 1:
            o = 'NW'
        if constriction == True:
            tail_shapes += quarterarc_trench(r, w, gap, arccentre[0], arccentre[1], orient=o)
            remove += [quarterarc(r - d_dots, 2*gap + w + 2*d_dots, arccentre[0], arccentre[1], orientation=o)]
            if o =='NE':
                tail_shapes += straight_trench(1, gap + float(w - constrictionw)/2, constrictionw, arccentre[0] + r, arccentre[1] -  1 - w - spacer, orientation='V')
                fine_shapes += straight_trench(ltail*constrictionr, gap + float(w - constrictionw)/2, constrictionw, arccentre[0] + r, arccentre[1] -  ltail*constrictionr - w - spacer, orientation='V')
                fine_shapes += straight_trench(spacer, gap, w, arccentre[0] + r, arccentre[1] - spacer, orientation='V')
                fine_shapes += thinning_trench(w, constrictionw, gap, arccentre[0] + r, arccentre[1] - w  - spacer)
                fine_shapes += thinning_trench(constrictionw, w, gap, arccentre[0] + r, arccentre[1] - w - ltail*constrictionr  - spacer)
                fine_shapes += straight_trench(ltail*(1-constrictionr), gap, w, arccentre[0] + r, arccentre[1] -  ltail - 2*w  - spacer, orientation='V')
                remove += [rect(2*gap + w + 2*d_dots, ltail + spacer + 2*w + d_dots, arccentre[0] + r - d_dots, arccentre[1] -  ltail - 2*w  - spacer - d_dots)]
                # if SQUID == True:
                #     fine_shapes += straight_trench(squid_loop, (w - squid_loop - 2*constriction)/2., w - (w - squid_loop - 2*constriction), squid_loop, arccentre[0] + r, arccentre[1] -  ltail - 2*w  - spacer + squid_loop, orientation='V')
                #     fine_shapes += rect(squid_loop, squid_loop, arccentre[0] + r + gap + w/2 - squid_loop/2, arccentre[1] -  ltail - 2*w  - spacer + squid_loop)
            elif o =='NW':
                tail_shapes += straight_trench(1, gap + float(w - constrictionw)/2, constrictionw, arccentre[0] - r - 2*gap -w, arccentre[1] -  1 - w  - spacer, orientation='V')
                fine_shapes += straight_trench(ltail*constrictionr, gap + float(w - constrictionw)/2, constrictionw, arccentre[0] - r - 2*gap -w, arccentre[1] -  ltail*constrictionr - w  - spacer, orientation='V')
                fine_shapes += straight_trench(spacer, gap, w, arccentre[0] - r - 2*gap -w, arccentre[1] - spacer, orientation='V')
                fine_shapes += thinning_trench(w, constrictionw, gap, arccentre[0] - r - 2*gap -w, arccentre[1] - w  - spacer)
                fine_shapes += thinning_trench(constrictionw, w, gap, arccentre[0] - r - 2*gap -w, arccentre[1] - w - ltail*constrictionr  - spacer)
                fine_shapes += straight_trench(ltail*(1-constrictionr), gap, w, arccentre[0] - r - 2*gap -w, arccentre[1] -  ltail- 2*w  - spacer, orientation='V')
                remove += [rect(2*gap + w + 2*d_dots, ltail + spacer + 2*w + d_dots, arccentre[0] - r - 2*gap -w - d_dots, arccentre[1] -  ltail- 2*w  - spacer - d_dots)]
                # if SQUID == True:
                #     fine_shapes += straight_trench(squid_loop, (w - squid_loop - 2*constriction)/2., w - (w - squid_loop - 2*constriction), squid_loop, arccentre[0] - r - 2*gap -w, arccentre[1] -  ltail - 2*w  - spacer + squid_loop, orientation='V')
                #     fine_shapes += rect(squid_loop, squid_loop, arccentre[0] - r - 2*gap -w + gap + w/2 - squid_loop/2, arccentre[1] -  ltail - 2*w  - spacer + squid_loop)
        else:
            tail_shapes += quarterarc_trench(r, w, gap, arccentre[0], arccentre[1], orient=o)

            remove += [quarterarc(r - d_dots, 2*gap + w + 2*d_dots, arccentre[0], arccentre[1], orientation=o)]
            if o =='NE':
                # if SQUID == True:
                #     fine_shapes += [rect()]
                tail_shapes += straight_trench(1, gap, w, arccentre[0] + r, arccentre[1] - 1, orientation='V')
                fine_shapes += straight_trench(ltail, gap, w, arccentre[0] + r, arccentre[1] - ltail, orientation='V')
                remove += [rect(2*gap + w + 2*d_dots, ltail + d_dots, arccentre[0] + r - d_dots,  arccentre[1] -  ltail - d_dots)]
            elif o =='NW':
                # if SQUID == True:
                #
                #     fine_shapes += [rect(SQUID_r*w, SQUID_H, arccentre[0] - r - gap -w + .5*(w - w*SQUID_r), arccentre[1] - ltail + 10)]
                #     fine_shapes += straight_trench(SQUID_con_H, .25*(w -SQUID_r*w -  2*SQUID_constriction), SQUID_constriction, arccentre[0] - r - gap -w, arccentre[1] - ltail + 10 + 0.5*SQUID_H, orientation='V')
                #     fine_shapes += straight_trench(SQUID_con_H, .25*(w -SQUID_r*w -  2*SQUID_constriction), SQUID_constriction, arccentre[0] - r - gap + .5*(-w +SQUID_r*w), arccentre[1] - ltail + 10 + 0.5*SQUID_H, orientation='V')
                fine_shapes += straight_trench(ltail, gap, w, arccentre[0] - r - 2*gap -w, arccentre[1] - ltail, orientation='V')
                tail_shapes += straight_trench(1, gap, w, arccentre[0] - r - 2*gap -w, arccentre[1] - 1, orientation='V')
                remove += [rect(2*gap + w + 2*d_dots, ltail + d_dots, arccentre[0] - r - d_dots- 2*gap -w,  arccentre[1] -  ltail - d_dots)]
        if SQUID == True:
            if o =='NE':
                print('Sorry - Oscar was lazy and has not coded this yet')
            elif o =='NW':
                if SQUID == True:
                    fine_shapes += [rect(SQUID_r*w, SQUID_H, arccentre[0] - r - gap -w + .5*(w - w*SQUID_r), arccentre[1] - ltail + 10)]
                    fine_shapes += straight_trench(SQUID_con_H, .25*(w -SQUID_r*w -  2*SQUID_constriction), SQUID_constriction, arccentre[0] - r - gap -w, arccentre[1] - ltail + 10 + 0.5*SQUID_H, orientation='V')
                    fine_shapes += straight_trench(SQUID_con_H, .25*(w -SQUID_r*w -  2*SQUID_constriction), SQUID_constriction, arccentre[0] - r - gap + .5*(-w +SQUID_r*w), arccentre[1] - ltail + 10 + 0.5*SQUID_H, orientation='V')


    else:
        pass
    cap = [move(i, 0, -2*gap - w) for i in cap]
    meanders = [move(i, 0, -2*gap - w) for i in meanders]
    tail_shapes = [move(i, 0, -2*gap - w) for i in tail_shapes]
    fine_shapes = [move(i, 0, -2*gap - w) for i in fine_shapes]
    remove = [move(i, 0, -2*gap -w) for i in remove]
    if flip_y == 'True':
        cap = [flip(i) for i in cap]
        meanders = [flip(i) for i in meanders]
        tail_shapes = [flip(i) for i in tail_shapes]
        fine_shapes = [flip(i) for i in fine_shapes]
        remove = [flip(i) for i in remove]
    return [cap + meanders + tail_shapes, fine_shapes, remove]

def antidot_array(x0, y0, X, Y, w, s, n):
    return [[(ii*(s + w) + x0, jj*(s + w) + y0), (ii*(s + w) + w + x0, jj*(s + w) + y0),
               (ii*(s + w) + w + x0, jj*(s + w) + w + y0), (ii*(s + w) + x0, jj*(s + w) + w + y0)]
               for ii in np.arange(-n, X/(s+w) + n, 1)
               for jj in np.arange(-n, Y/(s+w) + n, 1)]

def dot_line(x0, y0, L, w, s, orientation='V'):
    if orientation =='V':
        return [[(x0 - w/2, jj*(s+w) + y0),(x0 + w/2, jj*(s+w) + y0),
                  (x0 + w/2, jj*(s+w)+w + y0),(x0 - w/2, jj*(s+w)+w + y0)]
                  for jj in np.arange(0, L/(s+w), 1)]
    else:
        print('Oscar is lazy and has not added functionality for other orientations')

def dot_ring(x0, y0, gap, w, r):
    n_holes = int(np.pi*2*r/(gap+w))
    dtheta = 2*np.pi/(n_holes)
    thetas = np.arange(n_holes)*dtheta
    holes = [[(x0 + r*np.cos(i) - w/2, y0 + r*np.sin(i) - w/2),
              (x0 + r*np.cos(i) + w/2, y0 + r*np.sin(i) - w/2),
              (x0 + r*np.cos(i) + w/2, y0 + r*np.sin(i) + w/2),
              (x0 + r*np.cos(i) - w/2, y0 + r*np.sin(i) + w/2)] for i in thetas]
    return holes


def feedline(cc, rat, r, W, H, bond, d_dots, straight=False):
    if straight == False:
        #deltaL
        dL = [rect(bond*(1 + 2*rat), bond*rat, 0, 0)]
        dL += straight_trench(bond, bond*rat, bond, 0, bond*rat, orientation='V')
        dL += thinning_trench_style_2(bond, cc, rat, 0, bond*(1+rat), bond)

        #deltaR
        dR = [rect(bond*(1 + 2*rat), bond*rat, cc*(1 + 2*rat) + W + 2*r, 0)]
        dR += straight_trench(bond, bond*rat, bond, cc*(1 + 2*rat) + W + 2*r, bond*rat, orientation='V')
        dR += thinning_trench_style_2(bond, cc, rat, cc*(1 + 2*rat) + W + 2*r, bond*(1+rat), bond)

        #narrow - shapes start on left and move along feedline
        narrow = straight_trench(H, cc*rat, cc, bond*(rat + .5) - cc*(rat + .5), bond*(2 + rat), orientation='V')
        narrow += quarterarc_trench(r, cc, cc*rat, r+ bond*(rat + .5) + cc*(rat + .5), bond*(2 + rat) + H, orient='NW')
        narrow += straight_trench(W, cc*rat, cc, r+ bond*(rat + .5) + cc*(rat + .5), bond*(2 + rat) + H + r, orientation='H')
        narrow += quarterarc_trench(r, cc, cc*rat, r+ W + bond*(rat + .5) + cc*(rat + .5) , bond*(2 + rat) + H, orient='NE')
        narrow += straight_trench(H, cc*rat, cc, bond*(rat + .5) + cc*(rat + .5) + W + 2*r, bond*(2 + rat), orientation='V')

        #shapes to remove antidots from
        #dl
        remove = [rect(bond*(1 + 2*rat) + 2*d_dots, bond*(rat + 1) + d_dots, -d_dots , -d_dots)]
        remove += [[(-d_dots, bond*(rat + 1)), (bond*(1 + 2*rat) + d_dots, bond*(rat + 1)), (bond*(rat + .5) + cc*(rat + .5) + d_dots, bond*(rat + 2)), (bond*(rat + .5) - cc*(rat + .5) - d_dots, bond*(rat + 2))]]

        #dr
        remove += [rect(bond*(1 + 2*rat) + 2*d_dots,  bond*(rat + 1) + d_dots, cc*(1 + 2*rat) + W + 2*r -d_dots, -d_dots)]
        remove += [[(cc*(1 + 2*rat) + W + 2*r - d_dots, bond*(rat + 1)), (d_dots + cc*(1 + 2*rat) + W + 2*r + bond*(1 + 2*rat), bond*(rat + 1)), (d_dots + cc*(1 + 2*rat) + W + 2*r + bond*(rat + .5) + cc*(rat + .5), bond*(rat + 2)), (cc*(1 + 2*rat) + W + 2*r +bond*(rat + .5) - cc*(rat + .5) - d_dots, bond*(rat + 2))]]

        #narrow quarterarc(r, w, x0, y0, orientation='NE')
        remove += [rect(cc*(1 + 2*rat) + 2*d_dots, H, bond*(rat + .5) - cc*(rat + .5) - d_dots, bond*(2 + rat))]
        remove += [quarterarc(r - d_dots, cc*(1 + 2*rat) + 2*d_dots, r+ bond*(rat + .5) + cc*(rat + .5), bond*(2 + rat) + H, orientation='NW')]
        remove += [rect(W, cc*(1 + 2*rat) + 2*d_dots, r+ bond*(rat + .5) + cc*(rat + .5), bond*(2 + rat) + H + r - d_dots)]
        remove += [quarterarc(r - d_dots, cc*(1 + 2*rat) + 2*d_dots, r+ W + bond*(rat + .5) + cc*(rat + .5) , bond*(2 + rat) + H, orientation='NE')]
        remove += [rect(cc*(1 + 2*rat) + 2*d_dots, H, bond*(rat + .5) + cc*(rat + .5) + W + 2*r - d_dots, bond*(2 + rat))]

        return [dL + dR + narrow, remove]

    if straight == True:
        dL = [rect(bond*rat, bond, -bond*rat, 0)]
        dL += [rect(bond*(rat+1), bond*rat, -bond*rat, -bond*rat)]
        dL += [rect(bond*(rat+1), bond*rat, -bond*rat, bond)]
        dL += [[(bond, - bond*rat), (bond, 0), (2*bond, (bond - cc)/2), (2*bond, (bond - cc)/2 - cc*rat)],
               [(bond, bond), (bond,  bond*(1+rat)), (2*bond, (bond + cc)/2 + cc*rat), (2*bond, (bond  + cc)/2)]]

        dR = [rect(bond*rat, bond, W, 0)]
        dR += [rect(bond*(rat+1), bond*rat, W-bond, -bond*rat)]
        dR += [rect(bond*(rat+1), bond*rat, W-bond, bond)]
        dR += [[(W - bond, - bond*rat), (W - bond, 0), (W - 2*bond, (bond - cc)/2), (W - 2*bond, (bond - cc)/2 - cc*rat)],
               [(W - bond, bond), (W - bond,  bond*(1+rat)), (W - 2*bond, (bond + cc)/2 + cc*rat), (W - 2*bond, (bond  + cc)/2)]]

        straight = [rect(W - 4*bond, cc*rat,  2*bond, (bond - cc)/2 - cc*rat)]
        straight += [rect(W - 4*bond, cc*rat,  2*bond, (bond + cc)/2)]

        remove = [rect(bond*(1 + rat) + d_dots, bond*(1 + 2*rat) + 2*d_dots,-bond*rat - d_dots,-bond*rat - d_dots)]
        remove += [rect(bond*(1 + rat) + d_dots, bond*(1 + 2*rat) + 2*d_dots,W - bond,-bond*rat - d_dots)]
        remove += [rect(W - 4*bond, cc*(1 + 2*rat) + 2*d_dots, 2*bond, (bond - cc)/2 - cc*rat - d_dots)]
        remove += [[(bond, -bond*rat - d_dots), (bond, bond*(1+rat) + d_dots), (2*bond, bond/2 + cc*(2*rat+1)/2 + d_dots), (2*bond, (bond - cc)/2 - cc*rat - d_dots)]]
        remove += [[(W - bond, -bond*rat - d_dots), (W - bond, bond*(1+rat) + d_dots), (W - 2*bond, (bond)/2 + cc*(2*rat+1)/2 + d_dots), (W - 2*bond, (bond - cc)/2 - cc*rat - d_dots)]]

        return [dL + dR + straight, remove]

def quarterwave_inverted(w, gap, nturns, lcap, lmeander, r, tail=True, ltail=100,
                constriction=True, constrictionw=1, constrictionr=.5, spacer=5,
                SQUID=True, squid_loop=2, squid_constriction=0.5,
                flip_y='True', npoints=16):
    '''
    List of list of list of tuples.
    There are two lists denoting different parts of the resonator. One list is
    the capacitor, meanders and part of the tail. Second list contains the fine
    shapes. This allows these to be saved to different laye
    '''
    remove = [rect(gap, 2*gap + w , 0, 0)]
    coarse = [rect(lcap, w, gap, gap)]
    remove += [rect(lcap, 2*(gap) + w, gap, 0)]
    coarse += [rect(lcap, w, gap, gap)]
    arccentre = [gap + lcap, -r]
    for turn in range(nturns):
        if turn%2 == 0:
            o = 'E'
            coarse += [halfarc(r + gap, w, arccentre[0], arccentre[1], orientation=o, npoints=npoints)]
            remove += [halfarc(r, w + 2*gap, arccentre[0], arccentre[1], orientation=o, npoints=npoints)]
            coarse += [rect(lmeander, w, arccentre[0] - lmeander, arccentre[1] - r - gap - w)]
            remove += [rect(lmeander, 2*gap + w, arccentre[0] - lmeander, arccentre[1] - r - 2*gap - w)]
            arccentre = [arccentre[0] - lmeander, arccentre[1] - 2*r - 2*gap - w]
        elif turn%2 == 1:
            o = 'W'
            coarse += [halfarc(r + gap, w, arccentre[0], arccentre[1], orientation=o, npoints=npoints)]
            remove += [halfarc(r , w + 2*gap, arccentre[0], arccentre[1], orientation=o, npoints=npoints)]
            coarse += [rect(lmeander, w,arccentre[0], arccentre[1] -r -gap - w)]
            remove += [rect(lmeander, 2*gap + w , arccentre[0], arccentre[1] -r -2*gap - w )]
            arccentre = [arccentre[0] + lmeander, arccentre[1] - 2*r - 2*gap - w]
    fine = []
    if tail == True:
        if nturns%2 == 0:
            o = 'NE'
        elif nturns%2 == 1:
            o = 'NW'
        if constriction == True:
            coarse += [quarterarc(r + gap, w, arccentre[0], arccentre[1], orientation=o, npoints=npoints)]
            remove += [quarterarc(r , 2*gap + w , arccentre[0], arccentre[1], orientation=o, npoints=npoints)]
            if o =='NE':
                fine += [rect(w, ltail*constrictionr, arccentre[0] + r + gap, arccentre[1] -  ltail*constrictionr - spacer)]
                #fine_shapes += straight_trench(ltail*constrictionr, gap + float(w - constrictionw)/2, constrictionw, arccentre[0] + r, arccentre[1] -  ltail*constrictionr - w - spacer, orientation='V')
                fine += [rect(w, spacer, arccentre[0] + r + gap, arccentre[1] - spacer)]
                #fine_shapes += straight_trench(spacer, gap, w, arccentre[0] + r, arccentre[1] - spacer, orientation='V')
                fine += [[(arccentre[0] + r + gap, arccentre[1] - spacer - ltail*constrictionr), (arccentre[0] + r + gap + w, arccentre[1] - spacer - ltail*constrictionr), (arccentre[0] + r + gap + w*.5 + constrictionw*.5, arccentre[1] - spacer - (w - constrictionw)*.5  - ltail*constrictionr), (arccentre[0] + r + gap + w*.5 - constrictionw*.5,arccentre[1] - spacer - (w - constrictionw)*.5 - ltail*constrictionr)]]
                #fine_shapes += thinning_trench(w, constrictionw, gap, arccentre[0] + r, arccentre[1] - w  - spacer)
                fine += [[(arccentre[0] + r + gap + w*.5 - constrictionw*.5, arccentre[1] - spacer - ltail), (arccentre[0] + r + gap + w*.5 + constrictionw*.5, arccentre[1] - spacer - ltail), (arccentre[0] + r + gap + w, arccentre[1] - spacer - (w - constrictionw)*.5 - ltail), (arccentre[0] + r + gap,arccentre[1] - spacer - (w - constrictionw)*.5 - ltail)]]
                #fine_shapes += thinning_trench(constrictionw, w, gap, arccentre[0] + r, arccentre[1] - w - ltail*constrictionr  - spacer)
                fine += [rect(constrictionw, ltail*(1-constrictionr), arccentre[0] + r + gap + .5*(w - constrictionw), arccentre[1] - spacer - ltail*(1-constrictionr))]
                #fine_shapes += straight_trench(ltail*(1-constrictionr), gap, w, arccentre[0] + r, arccentre[1] -  ltail - 2*w  - spacer, orientation='V')
                remove += [rect(2*gap + w , ltail + spacer + 2*w , arccentre[0] + r, arccentre[1] -  ltail - 2*w  - spacer)]
                print('even number of turns in res cst not well tested ')
                # if SQUID == True:
                #     fine_shapes += straight_trench(squid_loop, (w - squid_loop - 2*constriction)/2., w - (w - squid_loop - 2*constriction), squid_loop, arccentre[0] + r, arccentre[1] -  ltail - 2*w  - spacer + squid_loop, orientation='V')
                #     fine_shapes += rect(squid_loop, squid_loop, arccentre[0] + r + gap + w/2 - squid_loop/2, arccentre[1] -  ltail - 2*w  - spacer + squid_loop)
            elif o =='NW':
                fine += [rect(w, ltail*constrictionr, arccentre[0] - r - gap -w, arccentre[1] -  ltail*constrictionr - spacer)]
                # fine_shapes += straight_trench(ltail*constrictionr, gap + float(w - constrictionw)/2, constrictionw, arccentre[0] - r - 2*gap -w, arccentre[1] -  ltail*constrictionr - w  - spacer, orientation='V')
                fine += [rect(w, spacer,arccentre[0] - r - gap -w, arccentre[1] - spacer)]
                # fine_shapes += straight_trench(spacer, gap, w, arccentre[0] - r - 2*gap -w, arccentre[1] - spacer, orientation='V')
                fine += [[(arccentre[0] - r - gap -w, arccentre[1] -  ltail*constrictionr - spacer), (arccentre[0] - r - gap , arccentre[1] -  ltail*constrictionr  - spacer), (arccentre[0] - r - gap - 0.5*(w - constrictionw), arccentre[1] -  ltail*constrictionr  - spacer- (w - constrictionw)*.5), (arccentre[0] - r - gap - 0.5*(w + constrictionw), arccentre[1] -  ltail*constrictionr  - spacer- (w - constrictionw)*.5)]]
                fine += [[(arccentre[0] - r - gap - 0.5*(w + constrictionw), arccentre[1] -  ltail - w  - spacer + 0.5*(w + constrictionw)), (arccentre[0] - r - gap - 0.5*(w - constrictionw) , arccentre[1] -  ltail - w  - spacer + 0.5*(w + constrictionw)), (arccentre[0] - r - gap, arccentre[1] -  ltail - w  - spacer + constrictionw), (arccentre[0] - r - gap -w, arccentre[1] -  ltail - w  - spacer + constrictionw)]]
                #fine_shapes += thinning_trench(w, constrictionw, gap, arccentre[0] - r - 2*gap -w, arccentre[1] - w  - spacer)
                # fine_shapes += thinning_trench(constrictionw, w, gap, arccentre[0] - r - 2*gap -w, arccentre[1] - w - ltail*constrictionr  - spacer)
                fine += [rect(constrictionw, ltail*(1-constrictionr), arccentre[0] - r - gap -0.5*(w + constrictionw) , arccentre[1] -  ltail - w  - spacer + 0.5*(w + constrictionw))]
                # fine_shapes += straight_trench(ltail*(1-constrictionr), gap, w, arccentre[0] - r - 2*gap -w, arccentre[1] -  ltail- 2*w  - spacer, orientation='V')
                fine += [rect(w, w + constrictionw, arccentre[0] - r - gap - w, arccentre[1] -  ltail- 2*w  - spacer)]
                remove += [rect(2*gap + w, ltail + spacer + 2*w, arccentre[0] - r - 2*gap -w , arccentre[1] -  ltail- 2*w  - spacer )]
                # if SQUID == True:
                #     fine_shapes += straight_trench(squid_loop, (w - squid_loop - 2*constriction)/2., w - (w - squid_loop - 2*constriction), squid_loop, arccentre[0] - r - 2*gap -w, arccentre[1] -  ltail - 2*w  - spacer + squid_loop, orientation='V')
                #     fine_shapes += rect(squid_loop, squid_loop, arccentre[0] - r - 2*gap -w + gap + w/2 - squid_loop/2, arccentre[1] -  ltail - 2*w  - spacer + squid_loop)
        else:
            print("You need to update res_shapes to include this without fine shapes.\
            You can probably hack this by setting the widths of the constriction\
            and the central conductor to being the same.\
            Past Oscar didn't test this.\
            Sorry.")
            # coarse += quarterarc(r + gap, w, gap, arccentre[0], arccentre[1], orientation=o)
            # if o =='NE':
            #     ail_shapest += straight_trench(ltail, gap, w, arccentre[0] + r, arccentre[1] - ltail, orientation='V')
            # elif o =='NW':
            #     tail_shapes += straight_trench(ltail, gap, w, arccentre[0] - r - 2*gap -w, arccentre[1] - ltail, orientation='V')


    else:
        pass
    coarse = [move(i, 0, -2*gap - w) for i in coarse]
    fine = [move(i, 0, -2*gap - w) for i in fine]
    remove = [move(i, 0, -2*gap -w) for i in remove]
    if flip_y == 'True':
        coarse = [flip(i) for i in coarse]
        fine = [flip(i) for i in fine]
        remove = [flip(i) for i in remove]
    return [coarse, fine, remove]

def hw_sim(cc, gap, r, lcap, lstart, c_gap, npts=16):
    #arm in
    shapes = [rect(lcap, cc, 0, 0)]
    shapes += [rect(lstart, cc, lcap+c_gap, 0)]
    remove = [rect(lcap + lstart + c_gap, cc + 2*gap, 0, -gap)]
    #turn down
    shapes += [quarterarc(r, cc, lcap + lstart + c_gap, - r, orientation='NE', npoints=npts)]
    remove += [quarterarc(r - gap, cc + 2*gap, lcap + lstart + c_gap, - r, orientation='NE', npoints=npts)]
    #half arc back up
    shapes += [halfarc(r, cc, lcap + lstart + c_gap + cc + 2*r, -r, orientation='S', npoints=npts)]
    remove += [halfarc(r - gap, cc + 2*gap, lcap + lstart + c_gap + cc + 2*r, -r, orientation='S', npoints=npts)]
    #middle vertical
    shapes += [rect(cc, 2*r, lcap + lstart + c_gap + cc + 3*r, -r)]
    remove += [rect(cc + 2*gap, 2*r, lcap + lstart + c_gap + cc + 3*r - gap, -r)]
    #half arc back down
    shapes += [halfarc(r, cc, lcap + lstart + c_gap + 2*cc + 4*r, r, orientation='N', npoints=npts)]
    remove += [halfarc(r - gap, cc + 2*gap, lcap + lstart + c_gap + 2*cc + 4*r, r, orientation='N', npoints=npts)]
    #turn to horizontal
    shapes += [quarterarc(r, cc, lcap + lstart + c_gap + 3*cc + 6*r, r, orientation='SW', npoints=npts)]
    remove += [quarterarc(r - gap, cc + 2*gap, lcap + lstart + c_gap + 3*cc + 6*r, r, orientation='SW', npoints=npts)]
    #arm out
    shapes += [rect(lcap, cc, lcap + lstart + c_gap + 3*cc + 6*r + lstart + c_gap, -cc)]
    shapes += [rect(lstart, cc, lcap + lstart + c_gap + 3*cc + 6*r, -cc)]
    remove += [rect(lcap + lstart + c_gap, cc + 2*gap, lcap + lstart + c_gap + 3*cc + 6*r, -gap - cc)]
    L = 2*lcap + 2*lstart + 2*c_gap + 3*cc + 6*r
    H = 2*(2*r + cc + gap)
    return [shapes, remove, L, H]

def alignment_mark(x0,y0,w,l):
    x0=float(x0)
    y0=float(y0)
    shapes = []
    shapes += [rect(l, w, x0 + .55*w , y0-.5*w)]
    shapes += [rect(l, w, x0 - .55*w-l, y0-.5*w)]
    shapes += [rect(w, l, x0 - .5*w, y0+.55*w )]
    shapes += [rect(w, l, x0 - .5*w, y0-.55*w - l)]
    shapes += [rect(.45*w,.45*w,x0-.5*w, y0-.5*w)]
    shapes += [rect(.45*w,.45*w,x0-.5*w, y0 +.05*w)]
    shapes += [rect(.45*w,.45*w,x0 +.05*w, y0 -.5*w)]
    shapes += [rect(.45*w,.45*w,x0 + .05*w, y0+.05*w)]
    shapes += [rect(.05, .05, x0-.025, y0-.025)]
    return shapes

def DC_contacts(x0, y0, w, l, bond, contacts=4):
    x0 = float(x0)
    y0 = float(y0)
    LH = []
    RH = []
    LH += [rect(bond, bond, x0, y0)]
    LH += [rect(2*bond, w, x0, y0 + bond)]
    RH += [rect(2*bond, w, x0 + 2*bond + l, y0 + bond)]
    RH += [rect(bond, bond, x0 + 3*bond + l, y0)]
    if contacts == 4:
        LH += [rect(bond, bond, x0, y0 + bond + w + 10)]
        LH += [rect(.5*bond, 10, x0 + bond, y0 + bond + w + 10)]
        LH += [rect(10, 20, x0 + 1.5*bond, y0 + bond + w)]
        RH += [rect(10, 20, x0 + 2.5*bond + l - 10, y0 + bond + w)]
        RH += [rect(.5*bond, 10, x0 + 2.5*bond + l, y0 + bond + w + 10)]
        RH += [rect(bond, bond, x0 + 3*bond + l, y0 + bond + w + 10)]
    return [LH, RH]

def cross(x0, y0, w, l):
    shapes = []
    shapes +=[rect(w, 2*l, x0-.5*w, y0-l)]
    shapes +=[rect(2*l, w, x0-l, y0-.5*w)]
    return shapes

def DC_contacts_etch(x0, y0, w, l, bond, gap, contacts=4):
    x0 = float(x0)
    y0 = float(y0)
    shapes = []
    shapes += [rect(4*bond + l + 4*gap, gap, 0, 0)]
    shapes += [rect(gap, bond, 0, gap)]
    shapes += [rect(bond*2 + gap*3, gap, 0, gap + bond)]
    shapes += [rect(gap, bond - w, bond + gap, gap + w)]
    shapes += [rect(bond - gap, gap, bond + 2* gap, gap + w)]
    shapes += [rect(gap, bond, 2*bond + 2*gap, gap + w)]
    shapes += [rect(l - 2*gap, gap, 2*bond + 3*gap, gap + w)]
    shapes += [rect(gap, bond, 2*bond + gap + l, gap + w)]
    shapes += [rect(2*bond + 2*gap, gap, 2*bond + 2*gap + l, gap + bond)]
    shapes += [rect(gap, bond , 3*bond + 2*gap + l, gap + w)]
    shapes += [rect(gap, bond + w , 4*bond + 3*gap + l, gap)]
    shapes += [rect(bond - gap, gap, 2*bond + 3*gap+ l, gap + w)]

    shapes = [move(i, x0, y0) for i in shapes]

    return shapes

def TRII(w_cap, w_in, l_in, gap):
    shapes = []
    shapes += [rect(l_in + 2*w_cap + gap, w_cap, 0, 0)]
    shapes += [rect(w_cap, l_in + 3*w_cap - gap - w_in, l_in + 2*w_cap + gap, 0)]
    shapes += [rect(w_cap, l_in + 2*w_cap + gap, 0, w_cap)]
    shapes += [rect(l_in + w_cap, w_in, w_cap, l_in + 3*w_cap- w_in + gap)]
    shapes += [rect(w_cap, l_in + 2*w_cap -w_in, l_in + w_cap, w_cap + gap)]
    shapes += [rect(l_in + w_cap - gap, w_cap, w_cap + gap, w_cap +gap)]
    shapes += [rect(w_cap, l_in + 2*w_cap - w_in - 2*gap, w_cap + gap, 2*w_cap +gap)]
    return shapes

def gavin_spiral(w, gap, l_straight, l_tot):
    shapes = []
    n = 0
    l = 0
    while l < l_tot:
        n += 1
        l = len_spiral(w, gap, l_straight, n)
    n -= 1 # work out how may full turns we need.
    lres = l_tot - len_spiral(w, gap, l_straight, n)
    for turn in range(1, n+1, 1):
        shapes += [rect(w, l_straight, turn*(gap + w) -w, 0)]
        shapes += [rect(w, l_straight, - turn*(gap + w) , 0)]
        shapes += [halfarc(turn*(gap + w) - w, w, 0, 0, orientation='S', npoints=16)]
        shapes += [halfarc(turn*(gap + w) -w/2 + gap/2, w, gap/2. + w/2., l_straight, orientation='N', npoints=16)]
    if lres > l_straight:
        shapes += [rect(w, l_straight, (n+1)*(gap + w) -w, 0)]
        lres -= l_straight
    else:
        shapes += [rect(w, lres, (n+1)*(gap + w) -w, l_straight - lres)]
        return shapes
    if lres > np.pi*((n+1)*(gap + w) - w):
        shapes += [halfarc((n+1)*(gap + w) - w, w, 0, 0, orientation='S', npoints=16)]
        lres -= np.pi*((n+1)*(gap + w) - w)
    else:
        t0 = lres/(np.pi*((n+1)*(gap + w) - w))*np.pi
        shapes += [arbarc((n+1)*(gap + w) - w, w, 0, 0, 0, -t0)]
        return shapes
    if lres > l_straight:
        shapes += [rect(w, l_straight, -(n+1)*(gap + w), 0)]
        lres -= l_straight
    else:
        shapes += [rect(w, lres, -(n+1)*(gap + w), 0)]
        return shapes
    t0 = lres/(np.pi*((n+1)*(gap + w) -w/2 + gap/2))*np.pi
    shapes += [arbarc((n+1)*(gap + w) -w/2 + gap/2, w, gap/2. + w/2., l_straight, np.pi, t0)]
    return shapes

def len_spiral(w, gap, l_straight, n):
    turns = np.arange(1, n+1, 1)
    turn_len = np.pi*(2*turns*(gap + w) - 3*w/2. + gap/2.)
    return 2*n*l_straight + np.sum(turn_len)

def opti_res(w_cap,l_cap_edge,gap,w_ind,r,n_turns):
    '''
    Omega Style resonator to be used with feedline
    -------------------------
    w_cap: Width of capacitor
    l_cap_edge: length of long edge of capacitor
    gap: gap between capacitor arms
    w_ind: width of inductor
    r: inner radius of omega inductor
    n_turns: number of capacitor turns
    '''

    starty = 0
    shapes = []

    #add base
    shapes += [rect(l_cap_edge/2,w_cap,0,0)]
    shapes += [rect(l_cap_edge/2,w_cap,l_cap_edge/2+gap+w_cap,0)]
    shapes += [rect(w_cap,2*w_cap,l_cap_edge/2-w_cap,w_cap)]
    shapes += [rect(w_cap,2*w_cap,l_cap_edge/2+gap+w_cap,w_cap)]
    shapes += [rect(l_cap_edge/2,w_cap,0,3*w_cap)]
    shapes += [rect(l_cap_edge/2,w_cap,l_cap_edge/2+gap+w_cap,3*w_cap)]
    shapes += [rect(w_cap,gap,0,4*w_cap)]
    shapes += [rect(l_cap_edge,w_cap,0,4*w_cap+gap)]
    shapes += [rect(w_cap,3*gap+2*w_cap,l_cap_edge+gap,4*w_cap)]
    shapes += [rect(w_cap,gap,l_cap_edge-w_cap,5*w_cap+gap)]

    #Start of capacitor section
    x_origin = 0
    y_origin = 5*w_cap + 2*gap


    for i in range(0,n_turns):
        startx = 0
        #move up in y to start next turn
        starty = y_origin + i*(4*w_cap+4*gap)
        #shapes += turn(shapes,startx,starty,w_cap,l_cap_edge,gap)

        #left capacitor arms
        shapes += [rect(l_cap_edge,w_cap,startx,starty)]
        shapes += [rect(l_cap_edge,w_cap,startx,starty+3*gap+3*w_cap)]
        #right capacitor arms
        shapes += [rect(l_cap_edge,w_cap,startx+w_cap+gap,starty+w_cap+gap)]
        shapes += [rect(l_cap_edge,w_cap,startx+w_cap+gap,starty+2*w_cap+2*gap)]
        #long side pieces
        shapes += [rect(w_cap,3*gap+2*w_cap,startx,starty+w_cap)]
        shapes += [rect(w_cap,3*gap+2*w_cap,startx+l_cap_edge+gap,starty+3*w_cap+2*gap)]
        #fill in gap pieces
        shapes += [rect(w_cap,gap,startx+w_cap+gap,starty+2*w_cap+gap)]
        shapes += [rect(w_cap,gap,startx+l_cap_edge-w_cap,starty+4*w_cap+3*gap)]


    #add top base for inductor
    starty = starty + (4*w_cap+4*gap)
    shapes += [rect(l_cap_edge,w_cap,0,starty)]
    shapes += [rect(w_cap,gap,0,starty+w_cap)]
    shapes += [rect(l_cap_edge/2,w_cap,0,starty+w_cap+gap)]
    shapes += [rect(l_cap_edge/2,w_cap,l_cap_edge/2+gap+w_cap,starty+w_cap+gap)]

    #inductor lines
    starty = starty+2*w_cap+gap
    shapes += [rect(w_ind,w_ind,l_cap_edge/2-w_ind,starty)]
    shapes += [rect(w_ind,w_ind,l_cap_edge/2+gap+w_cap,starty)]

    #Omega inductor
    omega = []
    # centre of omega
    x0 = (l_cap_edge+gap+w_cap)/2
    y0 = starty+gap+r+w_ind
    theta = (gap+w_cap)/r # Angle swept out by gap in omega
    t0 = -np.pi/2 + theta/2 # In radians
    tf = (3/2)*np.pi - theta/2
    n=16 # Number of points along each arc
    inner = [(r*np.cos(i) + x0, r*np.sin(i) + y0) for i in np.linspace(t0, tf, n)]
    outer = [((r+w_ind)*np.cos(i) + x0, (r+w_ind)*np.sin(i) + y0) for i in np.linspace(tf, t0, n)]

    shapes += [inner+outer]

    return shapes

def interdigital_capacitor(y0,l_arm,w_cap,gap,n):

    capacitor = []

    for i in range(n):
        capacitor += [rect(l_arm,w_cap,0,y0)]
        capacitor += [rect(w_cap,w_cap+2*gap,0,y0+w_cap)]
        capacitor += [rect(w_cap,w_cap+gap,l_arm+gap,y0)]
        capacitor += [rect(l_arm,w_cap,w_cap+gap,y0+w_cap+gap)]
        capacitor += [rect(w_cap,gap,l_arm+gap,y0+2*w_cap+gap)]
        y0 = y0 + (2*w_cap + 2*gap)
    return capacitor

def solidarc(x0,y0,r,w_ind,t0,tf,npoints=51):
    n=npoints
    inner = [(r*np.cos(i) + x0, r*np.sin(i) + y0) for i in np.linspace(t0, tf, n)] + [(r*np.cos(tf)+x0, r*np.sin(tf) + y0 - w_ind)]
    outer = [((r+w_ind)*np.cos(i) + x0, (r+w_ind)*np.sin(i) + y0) for i in np.linspace(tf, t0, n)] + [(r*np.cos(t0)+x0, r*np.sin(t0) + y0 - w_ind)]

    return [inner+outer]

def inerdig_optires(l_arm,w_cap,gap,n,r,w_ind):

    design = []

    design += [rect(l_arm/2,w_cap,0,0)]
    design += [rect(l_arm/2,w_cap,w_cap+gap+l_arm/2,0)]
    design += [rect(w_cap,2*w_cap,l_arm/2-w_cap,w_cap)]
    design += [rect(w_cap,2*w_cap,l_arm/2+w_cap+gap,w_cap)]
    design += [rect(l_arm/2,w_cap,0,3*w_cap)]
    design += [rect(l_arm/2,w_cap,l_arm/2+w_cap+gap,3*w_cap)]
    design += [rect(w_cap,gap,0,4*w_cap)]
    design += [rect(w_cap,gap,l_arm+gap,4*w_cap)]

    y0 = 4*w_cap + gap

    design += interdigital_capacitor(y0,l_arm,w_cap,gap,n)

    design += [rect(l_arm/2,w_cap,0,y0+n*(2*w_cap+2*gap))]
    design += [rect(l_arm/2,w_cap,w_cap+gap+l_arm/2,y0+n*(2*w_cap+2*gap))]
    design += [rect(w_ind,3*gap,l_arm/2-w_ind,y0+n*(2*w_cap+2*gap)+w_cap)]
    design += [rect(w_ind,3*gap,l_arm/2+w_cap+gap,y0+n*(2*w_cap+2*gap)+w_cap)]

    theta = (gap+w_cap)/r # Angle swept out by gap in omega
    t0 = -np.pi/2 + theta/2 # In radians
    tf = (3/2)*np.pi - theta/2
    design += solidarc((l_arm+w_cap+gap)/2,y0 + n*(2*w_cap+2*gap)+w_cap+r+w_ind,r,w_ind,t0,tf)

    return design
