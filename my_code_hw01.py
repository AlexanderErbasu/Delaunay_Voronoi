#-- my_code_hw01.py
#-- GEO1015.20019--hw01
#-- [YOUR NAME]
#-- [YOUR STUDENT NUMBER] 
#-- [YOUR NAME]
#-- [YOUR STUDENT NUMBER] 

import random #can I do this?
import numpy.linalg as m
import numpy as np

"""
You can add any new functions to this unit, but do not import new units.

You can add new methods to the DT class, but the functions that already exist
must have the same name/structure/input/output.

You need to complete the 2 functions:
  1. insert_one_point(self, x, y)
  2. get_voronoi_edges(self)

The data structure that must be used is:
    pt = [x, y]
    r = [pt1, pt2, pt3, neighbour1, neighbour2, neighbour3]
"""

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def toList(self):
        return [self.x,self.y]

    def __str__(self):
        return "%s, %s" %(self.x, self.y)

class Triangle:
    def __init__(self,a,b,c,t1,t2,t3):
        self.points = [a, b, c]  #t1 oppos a, t2 oppos b...
        self.neigh = [t1, t2, t3]

    def __str__(self):
        strg = str(id(self))+" "
        for elem in self.points:
            strg+= "("
            strg+= str(elem)
            strg+= " "
            strg+= ")"
        strg+= "|"

        for elem in self.neigh:
            if elem != -1:
                strg+= str(id(elem))
                strg+= " "
            else:
                strg+= str(-1)
                strg+= " "

        return strg

class DT:
    def __init__(self):
        self.trs = []
        #- create infinite triangle
        #- create 3 vertices
        # self.pts.append([-10000, -10000])
        # self.pts.append([10000, -10000])
        # self.pts.append([0, 10000])
        #- create one triangle
        big_triangle = Triangle(Point(-10000, -10000), Point(10000, -10000), Point(0, 10000),-1,-1,-1)
        self.trs.append(big_triangle)

    def number_of_points(self):
        return len(self.trs*3)

    def number_of_triangles(self):
        return len(self.trs)

    def get_delaunay_vertices(self):
        pts = []
        for tr in self.trs:
            a = tr.points[0] #modified
            b = tr.points[1]
            c = tr.points[2]
            pts.append(a.toList())
            pts.append(b.toList())
            pts.append(c.toList())
        return pts

    def get_delaunay_edges(self): #function used to display the edges between points?
        edges = []
        for tr in self.trs:
            a = tr.points[0].toList() #modified
            b = tr.points[1].toList()
            c = tr.points[2].toList()
            edges.append(a)
            edges.append(b)
            edges.append(a)
            edges.append(c)
            edges.append(b)
            edges.append(c)
        return edges

    def orientation(self,a,b,p):
        matrix= np.matrix([[a.x,a.y,1],[b.x,b.y,1],[p.x,p.y,1]])
        return m.det(matrix)

    def opposite_edge(self, i):
        switcher = {
        0: [1,2],
        1: [2,0],
        2: [0,1]
        }

        return switcher[i]

    def find_opposite_point(self, tr_init, tr_target):
        for i in range(3):
            match = False
            for j in range(3):
                if( tr_init.points[j] == tr_target.points[i]):
                    match = True
                    break
            if match:
                continue            
            return [tr_target.points[i], i] #return the point and its position

    def get_neighbour_of_point(self, triang, point):
        for i in range(3):
            if triang.points[i] == point:
                return triang.neigh[i]

    def get_index_of_point_from_neighbour(self, triang, neigh):
        for i in range(3):
            if triang.neigh[i] == neigh:
                return i

    def check_delumany(self, triang, point):
        matrix= np.matrix([[triang.points[0].x,triang.points[0].y,triang.points[0].x**2 + triang.points[0].y**2,1],
                        [triang.points[1].x,triang.points[1].y,triang.points[1].x**2 + triang.points[1].y**2,1],
                        [triang.points[2].x,triang.points[2].y,triang.points[2].x**2 + triang.points[2].y**2,1],
                        [point.x,point.y,point.x**2 + point.y**2,1]])
        return m.det(matrix)

    def get_voronoi_edges(self):
        """
        !!! TO BE COMPLETED AND MODIFIED !!!

        The returned list contains only points ([x,y]), the first 2 are one edge, 
        the following 2 are another edge, and so on.

        Thus for 2 edges, one betwen a and b, and the other between c and d:
        edges = [ [x1, y1], [x2, y2], [x43, y43], [x41, y41]]
        """
        #-- this is a dummy example that shows 2 lines in the area
        edges = []
        edges.append([100, 100])
        edges.append([200, 300])
        edges.append([200, 300])
        edges.append([450, 450])
        return edges

    def insert_one_point(self, x, y):
        point = Point(x,y)
        #FINDING THE TRIANGLE WHERE THE POINT IS LOCATED
        #selecting a random triangle from the list of triangles:
        start_triang = random.choice(self.trs)

        #use the walk algorithm to go to the triangle where the point is contained:
        destination_triang = None
        while destination_triang == None:
            visited_edges = 0
            for i in range(3):
                #print("we entered loop with index", i)
                if start_triang.neigh[i] != -1: #if we get to the border of the big triangle, there's no need to check
                    opposite = self.opposite_edge(i)
                    #print("opposite?",str(opposite))
                    if(self.orientation(start_triang.points[opposite[0]],start_triang.points[opposite[1]],point)) < 0:
                        #print("we entered here!!!")
                        start_triang = start_triang.neigh[i]
                        break
                visited_edges+=1
                #print("visited edges",str(visited_edges))
            if visited_edges==3:
                #print("3!!!!!")
                destination_triang = start_triang
        
        print("found triangle: ", str(destination_triang))
        #SPLIT THE TRIANGLE INTO 3, WITH P IN THE MIDDLE (ALSO, REMOVE THE INITIAL TRIANGLE FROM THE LIST)
        self.trs.remove(destination_triang)

        #destination triang -> points = [a,b,c]  neighbours = [neigh_a,neigh_b,neigh_c]
        #t1 -> [a,b,p][t2,t3,neigh_c]
        #t2 -> [b,c,p][t3,t1,neigh_a]
        #t3 -> [c,a,p][t1,t2,neigh_b]
        #keep p always in the last position
        t1 = Triangle(destination_triang.points[0], destination_triang.points[1], point, -1, -1, -1)
        t2 = Triangle(destination_triang.points[1], destination_triang.points[2], point, -1, -1, -1)
        t3 = Triangle(destination_triang.points[2], destination_triang.points[0], point, -1, -1, -1)

        #set first two neighbours
        t1.neigh[0] = t2
        t1.neigh[1] = t3

        t2.neigh[0] = t3
        t2.neigh[1] = t1

        t3.neigh[0] = t1
        t3.neigh[1] = t2

        t1.neigh[2] = destination_triang.neigh[2] #neighbour_c
        t2.neigh[2] = destination_triang.neigh[0] #neigh_a
        t3.neigh[2] = destination_triang.neigh[1] #neigh_b

        stack = []
        stack.append(t1)
        stack.append(t2)
        stack.append(t3)
        
        #TESTING
        while len(stack) != 0:
            tr = stack.pop()
            opposite_tr = tr.neigh[2] #p is always on the third position at this point
            if(opposite_tr == -1):
                self.trs.append(tr)

                continue
            
            print("given triangle:", str(tr))
            print("opposite triangle", str(opposite_tr))
            opposite_point = self.find_opposite_point(tr,opposite_tr) #has the point and its position in our triangle data structure
            print(str(opposite_point))
            #we have two situations:
            #the newly created triangle is indeed Delaunay -> add the new triangle to the list of triangles
            #& modify the neightbour of the opposite triangle with the new one
            #it is NOT Delaunay: remove from the list of triangles the opposite triangle, create two new triangles (with the edge flipped)
            #and add them to the list of triangles
            if(self.check_delumany(opposite_tr,opposite_point[0]) > 0): #the point is inside the circumcircle
                self.trs.remove(opposite_tr)
                #we have two triangles:
                #main_t = [a,b,p][t2,t3,neigh_c]
                #neigh_t = we have the position of opposite of p
                #=====>
                print("triangle creation not delu")
                neigh_a_opps = self.get_neighbour_of_point(opposite_tr, tr.points[0])
                neigh_b_opps = self.get_neighbour_of_point(opposite_tr, tr.points[1])

                neigh_a_init = self.get_neighbour_of_point(tr, tr.points[0])
                neigh_b_init = self.get_neighbour_of_point(tr, tr.points[1])

                t1 = Triangle(point, opposite_point[0], tr.points[0], 
                    neigh_b_opps, neigh_b_init,-1)
                t2 = Triangle(point, opposite_point[0], tr.points[1], 
                    neigh_a_opps, neigh_a_init ,-1)
                
                index_neigh_a_opps = self.get_index_of_point_from_neighbour(neigh_a_opps, opposite_tr)
                neigh_a_opps.neigh[index_neigh_a_opps] = t2

                index_neigh_b_opps = self.get_index_of_point_from_neighbour(neigh_b_opps, opposite_tr)
                neigh_b_opps.neigh[index_neigh_b_opps] = t1

                index_neigh_a_init = self.get_index_of_point_from_neighbour(neigh_a_init, tr)
                neigh_a_init.neigh[index_neigh_a_init] = t2

                index_neigh_b_init = self.get_index_of_point_from_neighbour(neigh_b_init, tr)
                neigh_b_init.neigh[index_neigh_b_init] = t1

                t1.neigh[2] = t2
                t2.neigh[2] = t1

                self.trs.append(t1)
                self.trs.append(t2)
            else: #our triangle is delunay, so we can just add it to the list of triangles, and modify the
                  #neightbouring triangle to include this as its neighbour on the found position
                  #also, add the current popped triangle to the list of triangles
                  opposite_tr.neigh[opposite_point[1]] = tr
                  self.trs.append(tr)        


        for trig in self.trs:
            print(trig)
        print()
        # self.trs.append(t1)
        # self.trs.append(t2)
        # self.trs.append(t3)
            

    
