
from tools import *
from geom import *

def c_vis2D(T, L_max, rectangles, visibility_graph):
    ''' We are assuming that all rectangles are to the right of T
    
        rectangles = [r_1, ..., r_m]

        r_i = [p1, p2, p3, p4]
        p_j = {"vertex": coords, "feasible": bool}

        Points may be not feasible (..., False), for example when the scenario is split into right and left sides
        and the rectangle in the middle is split in two pieces and new vertex are creted. The new vertex are not 
        feasible for the catenary to hang  
    '''    
    
    C, F = get_critical_points(T, rectangles)

    ML = {ci:float('inf') for ci in C}  
    MC = {ci:None for ci in C} 
    MF = {fi:None for fi in F} 
    MFX = {fi:None for fi in F} 

    # Initiallize the arrays with ci visibles from T
    Tpoint = vg.Point(*T) 
    for edge in visibility_graph.visgraph[vg.Point(*T)]:
        adj = edge.get_adjacent(Tpoint) 
        ci = (adj.x, adj.y)
        if ci in C:
            ML[ci] = euclidian_dist(ci, T) 
            MC[ci] = T
        
    # Fill ML and MC arrays with the visible ci pairs
    C.sort(key = lambda x : -x[1])
    for ci in C:
        if ML[ci] != float('inf'):
            for edge in visibility_graph.visgraph[vg.Point(*ci)]:
                adj = edge.get_adjacent(Tpoint) 
                cj = (adj.x, adj.y)
                DTj = ML[ci] + euclidian_dist(ci, cj)
                if cj in C and is_feasible_tight_tether(T, ci, cj) and DTj < ML[cj]:
                    ML[cj] = DTj
                    MC[cj] = ci

    # Fill MF array
    for fi in F:
        for ci in C + [T]:
            X = ground_intersection(ci, fi)
            if is_feasible_tether(ci, fi, X) \
                and  vg.Point(*ci) in visibility_graph.find_visible(vg.Point(*X)) \
                and  slope(ci, fi) < slope(fi, MF[fi]):
                    MF[fi] = ci
                    MFX[fi] = X

    # Get the opening bounds
    opening = []
    for ci in C:
        if ML[ci] > Lmax:
            continue

        X = (math.sqrt((Lmax - ML[ci])**2 - ci[1]**2), 0)
        if  is_feasible_tight_tether(MC[ci], ci, X) \
            and vg.Point(*ci) in visibility_graph.find_visible(vg.Point(*X)):
                opening.append((X, ci))

    # Get and clean the closing bounds
    closing = []
    for fi in F:
        mfi = MF[fi]
        mfxi = MFX[fi]

        if mfi == None:
            continue

        for x, ci in opening:
            invalid = False

            while True:  
                print(MFX[fi], MF[fi], x, ci)
                print(doIntersect(vg.Point(*mfxi), vg.Point(*mfi), vg.Point(*x), vg.Point(*ci)))
                print()

                if doIntersect(vg.Point(*mfxi), vg.Point(*mfi), vg.Point(*x), vg.Point(*ci)):
                    if mfi == ci:
                        break

                    invalid = True
                    break

                if ci[1] >= mfi[1]:
                    break

                x = ci
                ci = MC[ci]

            if not invalid:
                closing.append((mfxi, fi))


    # Join boundary pointns and sort them by X axis
    L = [{"label": "opening", "point": x} for x, _ in opening] + [{"label": "closing", "point": x} for x, _ in closing]
    L.sort(key=lambda x: x["point"])  

    # Get non c-visible intervals
    I = []
    initial = None
    for point in L:
        if point["label"] == "opening":
            initial = point["point"]

        if point["label"] == "closing":
            I.append((initial, point["point"]))
            initial = None


    # print()
    # print("C", C)
    # print("F", F)
    # print("ML", ML)
    # print("MC", MC)
    # print("MF", MF)
    # print("MFX", MF)
    # print("opening", opening)
    # print("closing", closing)
    # print("L", L)
    # print("I", I)

    return I



def get_critical_points(T, rectangles):

    C, F = [], []
    for ri in rectangles:
        
        ri.sort(key = lambda x: x["vertex"][0] + x["vertex"][1])
        if ri[0]["feasible"]:
            C.append(ri[0]["vertex"])
        
        if ri[-1]["feasible"]:
            F.append(ri[-1]["vertex"])
        
    return C, F
        



if __name__ == "__main__":

    T = (0,30)
    Lmax = 50
    rectangles = [
        [
            {"vertex": (10, 3), "feasible": True},
            {"vertex": (10, 5), "feasible": True},
            {"vertex": (25, 3), "feasible": True},
            {"vertex": (25, 5), "feasible": True}
        ],[
            {"vertex": (5, 8), "feasible": True},
            {"vertex": (5, 10), "feasible": True},
            {"vertex": (15, 8), "feasible": True},
            {"vertex": (15, 10), "feasible": True}
        ],
    ]
    vgraph = get_visibility_graph(T, rectangles)

    # # Plot Scenario
    vgraph = get_visibility_graph(T, rectangles, plot_graph=True)
    plot_scenario(T, Lmax, rectangles)

    c_vis2D(T, Lmax, rectangles, vgraph)


    