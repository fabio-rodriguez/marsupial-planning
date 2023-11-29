import math
import matplotlib.pyplot as plt
import numpy as np
import pyvisgraph as vg

from scipy.spatial import ConvexHull


def slope(P1, P2, default=float('inf')):
    if P1==None or P2==None:
        return default

    x1, y1 = P1
    x2, y2 = P2

    return (y2-y1)/(x2-x1) if x2 != x1 else default


def plot_scenario(T, Lmax, rectangles):

    plt.plot([T[0]], [T[1]], "or")
    for ri in rectangles: 
        points = np.array([p["vertex"] for p in ri])       
        hull = ConvexHull(points)

        for simplex in hull.simplices:
            plt.plot(points[simplex, 0], points[simplex, 1], 'c')

    plt.plot([T[0], math.sqrt(Lmax**2-T[1]**2)], [T[1], 0], 'b--') 
    plt.plot([0, math.sqrt(Lmax**2-T[1]**2)], [0, 0], 'k') 
    
    plt.show()


def get_visibility_graph(T, rectangles, plot_graph=False):

    polys = [[vg.Point(*T)]]
    for ri in rectangles:
        polys.append([vg.Point(*r["vertex"]) for r in ri])
            
    g = vg.VisGraph()
    g.build(polys, workers=6, status=False)

    if plot_graph:
        plot_visibility_graph(g)

    return g


def plot_visibility_graph(G):
    
    for edge in G.visgraph.edges:
        p1 = edge.p1
        p2 = edge.p2

        plt.plot([p1.x, p2.x], [p1.y, p2.y], "r--")


def euclidian_dist(V1, V2):
    return math.sqrt(sum([(v1i - v2i)**2 for v1i, v2i in zip(V1, V2)]))


def is_feasible_tight_tether(p1, p2, p3):
    
    return is_feasible_tether(p1, p2, p3) and slope(p1, p2) < slope(p2, p3) 


def is_feasible_tether(p1, p2, p3):
    
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    return x1 <= x2 <= x3 and y1 >= y2 >= y3



def ground_intersection(A, B):
    m = slope(A, B)
    n = A[1] - m*A[0]
    return (-n/m, 0) 
