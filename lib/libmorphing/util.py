import numpy as np


def get_points_in_triangulation(triangle, triangulation):
    """
    Retrieves a list of points that are within the bounds of a triangle.

    Args:
      - triangle: The 3x2 matrix of points which are the vertices of the triangle.
      - triangulation: The scipy.spatial.Delaunay triangulation.

    Returns:
      - Array of points
    """
    xs = list()
    ys = list()
    for vertex in triangle[triangulation.simplices][0]:
        xs.append(vertex[0])
        ys.append(vertex[1])
    points = list()
    for x in range(int(min(xs)), int(max(xs)) + 1):
        for y in range(int(min(ys)), int(max(ys)) + 1):
            simplices = triangulation.find_simplex(np.array([(x, y)]))
            if simplices[0] != -1:
                points.append([x, y])
    return np.array(points)
