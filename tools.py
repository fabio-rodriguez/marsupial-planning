import math
import matplotlib.pyplot as plt
import numpy as np

from scipy.spatial import ConvexHull


def slope(P1, P2):
    x1, y1 = P1
    x2, y2 = P2

    return (y2-y1)/(x2-x1) if x2 != x1 else float('inf')


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