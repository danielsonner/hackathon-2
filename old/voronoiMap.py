import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi
import random
import math

"""
borrowing much code from http://stackoverflow.com/questions/20515554/colorize-voronoi-diagram
"""
def main():
   NUM_COUNTRIES = 42
   MIN_WATER_AREA = .04
   NUM_PLAYERS = 7
   seedNum = int(random.random()*2000)
   # make up random data points
   np.random.seed(seedNum)
   points = np.random.rand(NUM_COUNTRIES, 2)
   points = sorted(points,key=lambda l:math.sqrt(l[0]**2+l[1]**2), reverse=False)

   # compute Voronoi tesselation
   vor = Voronoi(points)

   # plot
   regions, vertices = voronoi_finite_polygons_2d(vor)
   #print "--"
   #print regions
   #print "--"
   #print vertices

   # colorize
   i = 0
   colors = ['red','green','DarkRed','SandyBrown','Orchid','Gold', 'black', 'white']
   for region in regions:
       polygon = vertices[region]
       index = min(int(i//math.ceil(NUM_COUNTRIES//float(NUM_PLAYERS))),NUM_PLAYERS-1)
       print index
       fillColor = colors[index]
       # fill in with water if polygon over certain size and not supply center
       print polygonArea(polygon,vor)
       if polygonArea(polygon,vor) > MIN_WATER_AREA and i%4 != 0:
         fillColor = 'blue'
       plt.fill(*zip(*polygon), alpha=0.4, color=fillColor)
       i += 1

   # add points for supply centers, just for now let's try every 4 pts
   for i in range(len(points)):
     if i%4 == 0:
       point = points[i]
       plt.plot(point[0],point[1],'ko')
   plt.xlim(vor.min_bound[0] - 0.1, vor.max_bound[0] + 0.1)
   plt.ylim(vor.min_bound[1] - 0.1, vor.max_bound[1] + 0.1)
   plt.show()

"""
c/o http://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
"""
def polygonArea(corners, vor):
    # calc the x and y min and max for the bounds
    xmin = vor.min_bound[0] - 0.1
    xmax = vor.max_bound[0] + 0.1
    ymin = vor.min_bound[1] - 0.1
    ymax = vor.max_bound[1] + 0.1
    
    n = len(corners) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        # bound the xmin and max the the seeable screen as defined by vor
        area += min(xmax, max(xmin, corners[i][0])) * max(ymin, min(ymax, corners[j][1]))
        area -= min(xmax, max(xmin, corners[j][0])) * max(ymin, min(ymax, corners[i][1]))
    area = abs(area) / 2.0
    return area

"""
c/o http://code.activestate.com/recipes/578275-2d-polygon-area/
"""  
def poly_area2D(poly):
    total = 0.0
    N = len(poly)
    for i in range(N):
        v1 = poly[i]
        v2 = poly[(i+1) % N]
        total += v1[0]*v2[1] - v1[1]*v2[0]
    return abs(total/2)

def voronoi_finite_polygons_2d(vor, radius=None):
  """
  Reconstruct infinite voronoi regions in a 2D diagram to finite
  regions.

  Parameters
  ----------
  vor : Voronoi
      Input diagram
  radius : float, optional
      Distance to 'points at infinity'.

  Returns
  -------
  regions : list of tuples
      Indices of vertices in each revised Voronoi regions.
  vertices : list of tuples
      Coordinates for revised Voronoi vertices. Same as coordinates
      of input vertices, with 'points at infinity' appended to the
      end.

  """

  if vor.points.shape[1] != 2:
      raise ValueError("Requires 2D input")

  new_regions = []
  new_vertices = vor.vertices.tolist()

  center = vor.points.mean(axis=0)
  if radius is None:
      radius = vor.points.ptp().max()

  # Construct a map containing all ridges for a given point
  all_ridges = {}
  for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
      all_ridges.setdefault(p1, []).append((p2, v1, v2))
      all_ridges.setdefault(p2, []).append((p1, v1, v2))

  # Reconstruct infinite regions
  for p1, region in enumerate(vor.point_region):
      vertices = vor.regions[region]

      if all(v >= 0 for v in vertices):
          # finite region
          new_regions.append(vertices)
          continue

      # reconstruct a non-finite region
      ridges = all_ridges[p1]
      new_region = [v for v in vertices if v >= 0]

      for p2, v1, v2 in ridges:
          if v2 < 0:
              v1, v2 = v2, v1
          if v1 >= 0:
              # finite ridge: already in the region
              continue

          # Compute the missing endpoint of an infinite ridge

          t = vor.points[p2] - vor.points[p1] # tangent
          t /= np.linalg.norm(t)
          n = np.array([-t[1], t[0]])  # normal

          midpoint = vor.points[[p1, p2]].mean(axis=0)
          direction = np.sign(np.dot(midpoint - center, n)) * n
          far_point = vor.vertices[v2] + direction * radius

          new_region.append(len(new_vertices))
          new_vertices.append(far_point.tolist())

      # sort region counterclockwise
      vs = np.asarray([new_vertices[v] for v in new_region])
      c = vs.mean(axis=0)
      angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])
      new_region = np.array(new_region)[np.argsort(angles)]

      # finish
      new_regions.append(new_region.tolist())

  return new_regions, np.asarray(new_vertices)

  
if __name__ == "__main__":
  main()