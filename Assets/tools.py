import numpy as np

def catmullRomSplineInterpolation(P0, P1, P2, P3, t):
    t2 = t * t
    t3 = t2 * t
    point = 0.5 * ((2 * P1) +
                    (-P0 + P2) * t +
                    (2*P0 - 5*P1 + 4*P2 - P3) * t2 +
                    (-P0 + 3*P1 - 3*P2 + P3) * t3)
    return point

def catmullRomSpline(P0, P1, P2, P3, numPoints=100):
    points = []
    for t in np.linspace(0, 1, numPoints):
        points.append(catmullRomSplineInterpolation(P0, P1, P2, P3, t))
    return points

def catmullRomChain(points, numPointsPerSegment=100):
    splinePoints = []
    for i in range(len(points) - 3):
        P0, P1, P2, P3 = points[i:i+4]
        splinePoints.extend(catmullRomSpline(P0, P1, P2, P3, numPointsPerSegment))
    return np.array(splinePoints)
