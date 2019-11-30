#-- my_code_hw01.py
#-- GEO1015.20019--hw01
#-- [YOUR NAME]
#-- [YOUR STUDENT NUMBER] 
#-- [YOUR NAME]
#-- [YOUR STUDENT NUMBER] 

import random as rnd
import numpy as np
import numpy.linalg as m

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

class DT:
    def __init__(self):
        self.pts = []
        self.trs = []
        #- create infinite triangle
        #- create 3 vertices
        self.pts.append([-10000, -10000])
        self.pts.append([10000, -10000])
        self.pts.append([0, 10000])
        #- create one triangle
        self.trs.append([0, 1, 2, -1, -1, -1])

    def number_of_points(self):
        return len(self.pts)

    def number_of_triangles(self):
        return len(self.trs)

    def get_delaunay_vertices(self):
        return self.pts

    def get_delaunay_edges(self):
        edges = []
        for tr in self.trs:
            a = self.pts[tr[0]]
            b = self.pts[tr[1]]
            c = self.pts[tr[2]]
            edges.append(a)
            edges.append(b)
            edges.append(a)
            edges.append(c)
            edges.append(b)
            edges.append(c)
        return edges

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
    
    def opposite_edge(self, i):
        switcher = {
        0: [1,2],
        1: [2,0],
        2: [0,1]
        }

        return switcher[i]

    def orientation(self, triang ,edge, point_ind):
        matrix= np.matrix([[self.pts[triang[edge[0]]][0],self.pts[triang[edge[0]]][1],1],
                        [self.pts[triang[edge[1]]][0],self.pts[triang[edge[1]]][1],1],
                        [self.pts[point_ind][0],self.pts[point_ind][1],1]])
        return m.det(matrix)

    def walk(self, point_ind):
        #get a random triangle from the list of triangles as a starting point
        start_triang_ind = rnd.randint(0,len(self.trs)-1)
        dest_triang_ind = None
        while dest_triang_ind == None:
            visited_edges = 0
            for i in range(3,6):
                opposite_edge = self.opposite_edge(i-3)
                if self.orientation(self.trs[start_triang_ind], opposite_edge, point_ind) < 0:
                    start_triang_ind = self.trs[start_triang_ind][i]
                    break
                visited_edges += 1
            if visited_edges == 3:
                dest_triang_ind = start_triang_ind

        return dest_triang_ind
    
    def return_opposite_point_ind(self, initial_trg_ind, search_trg_ind):
        init = []
        init.append(self.trs[initial_trg_ind][0])
        init.append(self.trs[initial_trg_ind][1])
        init.append(self.trs[initial_trg_ind][2])

        neigh = []
        neigh.append(self.trs[search_trg_ind][0])
        neigh.append(self.trs[search_trg_ind][1])
        neigh.append(self.trs[search_trg_ind][2])

        for i in neigh:
            if i not in init:
                return i



    def circumcirlce(self, initial_trg_ind, search_trg_ind):
        """This function is used to check if the point in the search_trg_ind lies inside the circumcircle of initial_trg"""
        #check which is the opposite point in the neighbouring triangle:
        opposite_point_ind = self.return_opposite_point_ind(initial_trg_ind, search_trg_ind)
        ax = self.pts[self.trs[initial_trg_ind][0]][0]
        ay = self.pts[self.trs[initial_trg_ind][0]][1]

        bx = self.pts[self.trs[initial_trg_ind][1]][0]
        by = self.pts[self.trs[initial_trg_ind][1]][1]

        cx = self.pts[self.trs[initial_trg_ind][2]][0]
        cy = self.pts[self.trs[initial_trg_ind][2]][1]

        px = self.pts[opposite_point_ind][0]
        py = self.pts[opposite_point_ind][1]

        matrix= np.matrix([[ax, ay, ax**2 + ay**2, 1],
                          [bx, by, bx**2 + by**2, 1],
                          [cx, cy, cx**2 + cy**2, 1],
                          [px, py, px**2 + py**2, 1]])
        
        print(m.det(matrix))
        return m.det(matrix)
    
    def find_neighbour_of_point(self, trg_ind, point_ind):
        """ Searches for the position of the point (as we may not know exactly in the list where it is)
            And it returns the index of its oposite triangle"""
        for i in range(3):
            if self.trs[trg_ind][i] == point_ind:
                return self.trs[trg_ind][i+3]

    def find_location_of_neighbour(self, trg_ind, neigh_ind):
        print("trg ind", trg_ind, "neigh ind", neigh_ind)
        for i in range(3,6):
            if self.trs[trg_ind][i] == neigh_ind:
                print("index here", i)
                return i

    def insert_one_point(self, x, y):
        """
        !!! TO BE COMPLETED !!!
        """
        self.pts.append((x,y))
        point_ind = len(self.pts) - 1

        # find the triangle where the point exists: (walk algorithm)
        target_t_ind = self.walk(point_ind)

        #create 3 new triangles from this triangle
        #self.trs[target_t] = [ind_point_1, ind_point_2, ind_point_3, ind_neigh_t_1, ind_neigh_t_2, ind_neigh_t_3] =>
        #t1 = [point, ind_point_2, ind_point_3, ind_neigh_t_1, t2, t3]
        #t2 = [point, ind_point_1, ind_point_3, ind_neigh_t_2, t1, t3]
        #t3 = [point, ind_point_1, ind_point_2, ind_neigh_t_3, t1, t2]
        #t1 will receive the index of target_t
        #t2 and t3 will receive the indecies of len(self.pts) and len(self.pts) + 1 respectively
        t1_ind = target_t_ind
        t2_ind = len(self.trs)
        t3_ind = len(self.trs) + 1

        print(t1_ind)
        print(t2_ind)
        print(t3_ind)
        
        t1 = [point_ind, self.trs[target_t_ind][1], self.trs[target_t_ind][2], 
            self.trs[target_t_ind][3], t2_ind, t3_ind]
        t2 = [point_ind, self.trs[target_t_ind][0], self.trs[target_t_ind][2],
            self.trs[target_t_ind][4], t1_ind, t3_ind]
        t3 = [point_ind, self.trs[target_t_ind][0], self.trs[target_t_ind][1],
            self.trs[target_t_ind][5], t1_ind, t2_ind]

        self.trs[target_t_ind] = t1
        self.trs.append(t2)
        self.trs.append(t3)

        #triangles verification
        stack = []
        stack.append(t1_ind)
        stack.append(t2_ind)
        stack.append(t3_ind)

        while len(stack) != 0:
            current_t_ind = stack.pop()
            print(self.trs)
            print(current_t_ind)
            #get adjescent triangle -> the first neightbours
            adj_t_ind = self.trs[current_t_ind][3]
            if(adj_t_ind == -1):
                continue
            else:            
                opposite_point_ind = self.return_opposite_point_ind(current_t_ind, adj_t_ind)
                if (self.circumcirlce(current_t_ind, adj_t_ind) > 0): #it is delaunay
                    self.trs[adj_t_ind][opposite_point_ind+3] = current_t_ind
                else:
                    #the edge should be flipped
                    #we create two new triangles:
                    #current_t = [point, ind_point_1, ind_point_2, adj_t, neigh_curr_point_1, neigh_curr_point_2]
                    #oppo_t = [point, ind_point_1, ind_point_2, adj_t, neigh_curr_point_1, neigh_curr_point_2]
                    #neigh_t = we have the position of opposite of p
                    #=====>
                    print("here we are")
                    neigh_curr_a_ind = self.find_neighbour_of_point(current_t_ind,self.trs[current_t_ind][1])
                    negih_curr_b_ind = self.find_neighbour_of_point(current_t_ind,self.trs[current_t_ind][2])

                    neigh_adj_a_ind = self.find_neighbour_of_point(adj_t_ind,self.trs[current_t_ind][1])
                    neigh_adj_b_ind = self.find_neighbour_of_point(adj_t_ind,self.trs[current_t_ind][2])

                    print("here we are", neigh_curr_a_ind, negih_curr_b_ind, neigh_adj_a_ind, neigh_adj_b_ind)

                    new_t1 = [point_ind, opposite_point_ind, self.trs[current_t_ind][1], 
                                neigh_adj_b_ind, negih_curr_b_ind, -1]
                    new_t2 = [point_ind, opposite_point_ind, self.trs[current_t_ind][2],
                                neigh_adj_a_ind, neigh_curr_a_ind, -1]

                    new_t1[5] = new_t2
                    new_t2[5] = new_t1

                    self.trs[current_t_ind] = new_t1
                    self.trs.append(new_t2)
                    
                    a = self.find_location_of_neighbour(negih_curr_b_ind,current_t_ind)
                    b = self.find_location_of_neighbour(neigh_adj_b_ind,adj_t_ind)
                    c = self.find_location_of_neighbour(neigh_curr_a_ind,current_t_ind)
                    d = self.find_location_of_neighbour(neigh_adj_a_ind,adj_t_ind)

                    if a != -1 and a is not None:
                        self.trs[negih_curr_b_ind][self.find_location_of_neighbour(negih_curr_b_ind,current_t_ind)] = current_t_ind

                    if b != -1 and b is not None:
                        self.trs[neigh_adj_b_ind][self.find_location_of_neighbour(neigh_adj_b_ind,adj_t_ind)] = current_t_ind

                    if c != -1 and c is not None:
                        self.trs[neigh_curr_a_ind][self.find_location_of_neighbour(neigh_curr_a_ind,current_t_ind)] = len(self.trs) -1

                    if d != -1 and d is not None:
                        self.trs[neigh_adj_a_ind][self.find_location_of_neighbour(neigh_adj_a_ind,adj_t_ind)] = len(self.trs) -1
                    
                    stack.append(current_t_ind)
                    stack.append(len(self.trs) -1)

                    







         

