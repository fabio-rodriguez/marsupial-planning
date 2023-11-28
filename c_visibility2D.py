
from tools import *

# 4 for i in C.Length do
# 5 if Visible(T, C[i]) then
# 6 ML[i] = δ(T, C[i])
# 7 MC [i] = T
# 8 end
# 9 for i in C.Length do
# 10 if ML[i] ̸ = ∞ then
# 11 for j in C.Length do
# 12 P ← {MC [i], C[i], C[j]}
# 13 DT,i,j ← ML[i] + δ(C[i], C[j])
# 14 if Visible(C[i], C[j]) and IsFTT(P)
# and DT,i,j < ML[j] then
# 15 ML[j] ← DT,i,j
# 16 MC [j] ← C[i]
# 17 end
# 18 end
# 19 for i in F.Length do
# 20 for W in C ∪ {T } do
# 21 X ← GroundIntersection(W, F[i])
# 22 P ← {W, F[i], X}
# 23 if IsFTT(P) and
# Slope(W, F[i]) > Slope(MF [i], F[i]) then
# 24 MF [i] ← W
# 25 end
# 26 end
# 27 X ← OpeningBounds(C, ML, O2D )
# 28 Y ← ClosingBounds(F, MF , O2D ))
# 29 Y ← CleanClosingPoints(Y, X , MC )
# 30 L ← (X ∪ Y).SortByXAxis()
# 31 I ← GetNonCVisIntervals(L)
# 32 return I

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

    C.sort(key = lambda x : -x[1])

    ML = [float('inf')] * len(C)
    MC = [None] * len(C)
    MF = [None] * len(F)






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
        [{"vertex": (14.156, 4), "feasible": True},
        {"vertex": (14.156, 5), "feasible": True},
        {"vertex": (20, 4), "feasible": True},
        {"vertex": (20, 5), "feasible": True}],
    ]

    plot_scenario(T, Lmax, rectangles)
