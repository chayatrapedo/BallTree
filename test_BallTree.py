import pytest
import sys
import math
import random
from BallTree import * 

# fake ball tree class to test the 
class FakeBallTree(object):
    
    # store data points tuples in dictionary 
    def __init__(self, points):
        dictPoints = {}
        for point in points:
            dictPoints[point[0]] = point[1]
        self.points = dictPoints
        
    def getSize(self): return len(self.points)
    
    # find numNearest nearest neighbors to the tuple of d-dimensional coordinates. 
    def nearestNeighbors(self, point, numNearest=1):
        
        # a point can only have neighbors if it's the same dimensions
        # as the other keys in the tree
        keys = list(self.points.keys())
        if len(point) != len(keys[0]): return None
        
        # empty list to track numNearest nearest neighbors
        inDistOrder = []
        if numNearest < 1: return inDistOrder
        
        # append closest keys to preliminary answer list based on distance
        for key in keys:
            # fill the list with the first numNearest keys
            dist = FakeBallTree.__squareDist(point, key)
            if dist != 0: inDistOrder += [(dist, key)]
        
        # sort so the answer can be compared with the BallTree
        inDistOrder.sort()
               
        # create ans list with tuples key, data
        ans = [elem[1] for elem in inDistOrder]
        return ans[:numNearest]
        
    # returns a tuple of the key and the data if it's in the BallTree  
    def find(self, key):
        if key in self.points: return self.points[key]
        return None
    
    # find number of neighbors whose distance to the query point is 
    # within the given radius 
    def countRadius(self, point, rad):
        
        # a point can only have neighbors if it's in the tree
        keys = list(self.points.keys())
        if len(point) != len(keys[0]): return None
        
        # empty list to track numNearest nearest neighbors
        withinRad = []
        if numNearest <= 0: return withinRad
        
        # append closest keys to preliminary answer list based on distance
        for key in keys:
            # fill the list with the first numNearest keys
            dist = FakeBallTree.__squareDist(point, key)
            if dist <= (rad**2): withinRad += [key]
        
        # sort so the answer can be compared with the BallTree
        withinRad.sort()
               
        return withinRad    
        
    def __squareDist(start, end):
    
        dist = 0
    
        for i in range(len(start)): # the amount of dimensions
            dist += ((start[i] - end[i]) ** 2)
    
        return dist    
    
    
############ CONSTRUCTING BALL TREE ########################################

# Reapeatedly tests constructing the ball tree with randomly generated int-based keys 
# in creating a small-size data set with small dimensions, and likewise for
# medium and large
# The Ball Tree is verified to be constructed correctly based on the size of the
# data, fake tree, and Ball Tree staying the same and being able to find the data
# for each point in the data set
def test_construct_ints(): 
    
    # test on multiple data sets
    for i in range(10):
        
        # small, medium, and large sets of points in respective dimensions
        s = generatePoints(random.randint(2,4), 10, False, -1000, 1000)
        m = generatePoints(random.randint(5,7), 50, False, -1000, 1000)
        l = generatePoints(random.randint(8,10), 200, False, -1000, 1000)
        
        # creating real and fake tree for each    
        sTree = BallTree(s)
        fsTree = FakeBallTree(s)
        
        mTree = BallTree(m)
        fmTree = FakeBallTree(m)
        
        lTree = BallTree(l)
        flTree = FakeBallTree(l)
        
        # check sizes are all the same
        assert sTree.getSize() == len(s) and sTree.getSize() == fsTree.getSize()
        assert mTree.getSize() == len(m) and mTree.getSize() == fmTree.getSize()
        assert lTree.getSize() == len(l) and  lTree.getSize() == flTree.getSize()
        
        # check that all the points exist in both and can be found with correct data
        for point in s:
            assert sTree.find(point[0]) == point[1]
            assert sTree.find(point[0]) == fsTree.find(point[0])
            
        for point in m:
            assert mTree.find(point[0]) == point[1]
            assert mTree.find(point[0]) == fmTree.find(point[0])
            
        for point in l:
            assert lTree.find(point[0]) == point[1]
            assert lTree.find(point[0]) == flTree.find(point[0])         


# Same test as above with floats
def test_construct_floats(): 
    
    # test on multiple data sets
    for i in range(10):
        
        # small, medium, and large sets of points in respective dimensions
        s = generatePoints(random.randint(2,4), 10, True, -1000, 1000)
        m = generatePoints(random.randint(5,7), 50, True, -1000, 1000)
        l = generatePoints(random.randint(8,10), 200, True, -1000, 1000)
        
        # creating real and fake tree for each    
        sTree = BallTree(s)
        fsTree = FakeBallTree(s)
        
        mTree = BallTree(m)
        fmTree = FakeBallTree(m)
        
        lTree = BallTree(l)
        flTree = FakeBallTree(l)
        
        # check sizes are all the same
        assert sTree.getSize() == len(s) and sTree.getSize() == fsTree.getSize()
        assert mTree.getSize() == len(m) and mTree.getSize() == fmTree.getSize()
        assert lTree.getSize() == len(l) and  lTree.getSize() == flTree.getSize()
        
        # check that all the points exist in both and can be found with correct data
        for point in s:
            assert sTree.find(point[0]) == point[1]
            assert sTree.find(point[0]) == fsTree.find(point[0])
            
        for point in m:
            assert mTree.find(point[0]) == point[1] 
            assert mTree.find(point[0]) == fmTree.find(point[0])
            
        for point in l:
            assert lTree.find(point[0]) == point[1] 
            assert lTree.find(point[0]) == flTree.find(point[0])    

# Same tests as above, but the amount, dimensionality, float/int-ness of the points
# are completely random. Tests are repeated 10X more
def test_construct_random_torture(): 
        
    # test on multiple data sets
    for i in range(100):
        
        # randomly choosing dimensionality, size, float/int, large range 
        p = generatePoints(random.randint(2,10), random.randint(10, 1000),\
                           random.choice([False,True]), -10000, 10000)
        
        # creating real and fake tree for each    
        t = BallTree(p)
        ft = FakeBallTree(p)
        
        # check sizes are all the same
        assert t.getSize() == len(p) and t.getSize() == ft.getSize()
        
        # check that all the points exist in both and are found with correct data
        for point in p:
            assert t.find(point[0]) == point[1] 
            assert t.find(point[0]) == ft.find(point[0])


############ BALL TREE FIND ################################################

# Note: Because the tests above verified that find() works for points that are 
# inserted, these tests try to "break" find
            
# Tests that find will return None if the query point is of a lesser dimension
# than the other points in the tree
def test_find_less_dimensions(): 
    
    # three different randomly-generated Ball Trees
    for i in range(3):
        
        dim = random.randint(2,10)
        dType = random.choice([True, False])
        p = generatePoints(dim, random.randint(10, 100),\
                           dType, -10000, 10000)        
                
        t = BallTree(p)
        
        # randomly generated too-small tuples
        for i in range(5):
            k = generateKey(dim-1, dType)
            assert t.find(k) == None
            
        # truncate a point in the points so it's 1 dimension less (it is a part of
        # of of the existing points)
        for i in range(5):
            k, d = random.choice(p)
            k = k[:-1]
            assert t.find(k) == None
    
# Tests that find will return None if the query point is of a higher dimension
# than the other points in the tree
def test_find_more_dimensions(): 
    
    # three different randomly-generated Ball Trees
    for i in range(3):
        
        dim = random.randint(2,10)
        dType = random.choice([True, False])
        p = generatePoints(dim, random.randint(10, 100),\
                           dType, -10000, 10000)        
                
        t = BallTree(p)
        
        # randomly generated too-big tuples
        for i in range(5):
            k = generateKey(dim + random.randint(1,3), dType)
            assert t.find(k) == None
            
        # expansion of a point in the points so it's 1-3 dimensions greater 
        # (one of the existing points is a part of it)
        for i in range(5):
            k, data = random.choice(p)
            # add another position, value doesn't matter
            for i in range(random.randint(1,3)): k += k[0], 
            assert t.find(k) == None

# Find is calculated based on distance, so the float/int type should not matter 
# if you're searching so long as the values are the same
def test_find_data_types(): 
    
    # three different randomly-generated int Ball Trees
    for i in range(3):
        
        # create a tree of ints
        dim = random.randint(2,10)
        p = generatePoints(dim, random.randint(10, 100),\
                           False, -10000, 10000)        
        
        t = BallTree(p)   
    
        for i in range(5):
            
            # create a float-version of the key
            k, data = random.choice(p) 
            kf = tuple()
            for i in range(len(k)):
                kf += float(k[i]),
            
            assert t.find(kf) == data and t.find(kf) == t.find(k) 
            
        # three different randomly-generated float Ball Trees
        for i in range(3):
            
            # create a tree of ints of floats
            dim = random.randint(2,10)
            
            p = []
            
            for i in range(random.randint(10, 100)):
                point = tuple()
                
                for i in range(dim):
                    point += float(random.randint(-10000,10000)),
                
                entry = point, random.random(),  
                p += [entry]
                                
            t = BallTree(p)   
        
            for i in range(5):
                
                # create a float-version of the key
                k, data = p.pop()
                kf = tuple()
                for i in range(len(k)):
                    kf += int(k[i]),
                
                assert t.find(kf) == data and t.find(kf) == t.find(k)    
           
# tries to find points that are the same dimension that were never inserted 
def test_find_never_inserted(): 
    
    # test 3 different ball trees
    for i in range(3):
        
        # generate tree
        dim = random.randint(2,10)
        dType = random.choice([True, False])
        p = generatePoints(dim, random.randint(10, 100),\
                           dType, -10000, 10000)        
        
        # just the keys
        p_keys = [point[0] for point in p]
        
        t = BallTree(p)       
    
        i = 0
        while i < 10:
            # generate random key of same dimensions
            k = generateKey(dim, dType)
            
            # if it's not in the keys, try to find it
            if k not in p_keys:
                assert t.find(k) == None
                i += 1
            

# randomly pick any of these tests
def test_find_torture():
    
    for i in range(20):
        n = random.randint(1, 1000)
        if n % 4 == 0: test_find_more_dimensions()
        elif n % 4 == 1: test_find_more_dimensions()
        elif n % 4 == 2: test_find_data_types()
        else: test_find_never_inserted()
        

############ NEAREST NEIGHBOR SEARCH #######################################

# points that are being searched for must have the same dimensions as the points
# in the tree if the key's dimensions don't match the tree
def test_nns_imposter():

    # three different randomly-generated Ball Trees
    for i in range(3):
        
        dim = random.randint(2,10)
        dType = random.choice([True, False])
        p = generatePoints(dim, random.randint(10, 100),\
                           dType, -10000, 10000)        
                
        t = BallTree(p)
        
        # randomly generated too-small and too-big tuples
        for i in range(5):
            k1 = generateKey(dim-1, dType)
            k2 = generateKey(dim+1, dType)
            assert t.nearestNeighbors(k1, random.randint(2,5)) == None
            assert t.nearestNeighbors(k2, random.randint(2,5)) == None
            
    
# Tests that find will return None if the query point is of a higher dimension
# than the other points in the tree
def test_find_more_dimensions(): 
    
    # three different randomly-generated Ball Trees
    for i in range(3):
        
        dim = random.randint(2,10)
        dType = random.choice([True, False])
        p = generatePoints(dim, random.randint(10, 100),\
                           dType, -10000, 10000)        
                
        t = BallTree(p)
        
        # randomly generated too-big tuples
        for i in range(5):
            k = generateKey(dim + random.randint(1,3), dType)
            assert t.find(k) == None
            
        # expansion of a point in the points so it's 1-3 dimensions greater 
        # (one of the existing points is a part of it)
        for i in range(5):
            k, data = random.choice(p)
            # add another position, value doesn't matter
            for i in range(random.randint(1,3)): k += k[0], 
            assert t.find(k) == None
            
# returns empty list for n=0 nearest neighbors
def test_nns_zero(): 
    
    for i in range(5):
    
        # generate random tree 
        p = generatePoints(random.randint(2,10), random.randint(10, 1000),\
                           random.choice([False,True]), -10000, 10000) 
        
        t = BallTree(p)
        
        # pick a random query point
        key, data = random.choice(p)
        
        assert t.nearestNeighbors(key, 0) == []    
    

# returns empty list for n<0 nearest neighbors
def test_nns_negative(): 
    
    for i in range(5):
    
        # generate random tree 
        p = generatePoints(random.randint(2,10), random.randint(10, 1000),\
                           random.choice([False,True]), -10000, 10000) 
        
        t = BallTree(p)
        
        # pick a random query point
        key, data = random.choice(p)
        
        # pick random negative amount of nearest neighbors
        assert t.nearestNeighbors(key, random.randint(-100, -1)) == []    

# returns closest point for n=1 nearest neighbors
def test_nns_one(): 
    
    for i in range(5):
    
        # generate random tree 
        p = generatePoints(random.randint(2,10), random.randint(10, 1000),\
                           random.choice([False,True]), -10000, 10000) 
        
        t, ft = BallTree(p), FakeBallTree(p)
        
        # pick a random query point
        key, data = random.choice(p)
        
        # pick random negative amount of nearest neighbors
        assert len(t.nearestNeighbors(key, 1)) == 1    
        assert t.nearestNeighbors(key, 1) == ft.nearestNeighbors(key, 1)    

# returns n closest points where n < size of Ball Tree
def test_nns_small(): 
    
    for i in range(5):
    
        # generate random tree 
        p = generatePoints(random.randint(2,10), random.randint(10, 1000),\
                           random.choice([False,True]), -10000, 10000) 
        
        t, ft = BallTree(p), FakeBallTree(p)
        
        # pick a random query point
        key, data = random.choice(p)
        
        # random number of neighbors, less than size of Ball Tree
        n = random.randint(2, len(p) - 1)
        
        t_ans, ft_ans = t.nearestNeighbors(key, n), ft.nearestNeighbors(key, n)
        
        # make sure the amount of neighbors requested is the amount returned
        assert len(t_ans) == n  
        assert len(t_ans) == len(ft_ans)
        assert t.nearestNeighbors(key, n) == ft.nearestNeighbors(key, n)    

# returns n-1 points when n = size of the Ball Tree and the key is in the tree
def test_nns_same_size_in_tree(): 
    
    for i in range(5):
        
        # pick random size for tree
        size = random.randint(10, 1000)
    
        # generate random tree 
        p = generatePoints(random.randint(2,10), size,\
                           random.choice([False,True]), -10000, 10000) 
        
        t, ft = BallTree(p), FakeBallTree(p)
        
        # pick a random query point from within the tree
        key, data = random.choice(p)
                
        # amount of neighbors MUST be size - 1 because the point is IN the tree
        assert key not in t.nearestNeighbors(key, size)
        assert len(t.nearestNeighbors(key, size)) == size - 1
        assert len(t.nearestNeighbors(key, size)) == len(ft.nearestNeighbors(key, size))
        assert t.nearestNeighbors(key, size) == ft.nearestNeighbors(key, size)  
        
# returns n points when n = size of the Ball Tree and the key isn't in the tree
def test_nns_same_size_random(): 
    
    for i in range(5):
        
        # pick random size for tree
        size = random.randint(10, 1000)
    
        # generate random tree 
        p = generatePoints(random.randint(2,10), size,\
                           random.choice([False,True]), -10000, 10000) 
        
        t, ft = BallTree(p), FakeBallTree(p)
        
        # pick a random query point from within the tree
        key, data = random.choice(p)
        
        # amount of neighbors MUST be size - 1 because the point is IN the tree
        assert key not in t.nearestNeighbors(key, size)
        assert len(t.nearestNeighbors(key, size)) == size - 1
        assert len(t.nearestNeighbors(key, size)) == len(ft.nearestNeighbors(key, size))
        assert t.nearestNeighbors(key, size) == ft.nearestNeighbors(key, size)    

# returns n-1 points when n > size of the Ball Tree
def test_nns_max_amount(): 
    
    for i in range(5):
        
        # pick random size for tree
        size = random.randint(10, 1000)
    
        # generate random tree 
        p = generatePoints(random.randint(2,10), size,\
                           random.choice([False,True]), -10000, 10000) 
        
        t, ft = BallTree(p), FakeBallTree(p)
        
        # pick a random query point
        key, data = random.choice(p)
        
        # random number of neighbors, greater than size of Ball Tree
        n = random.randint(size+1, size+100)
        
        # amount of neighbors MUST be size - 1
        assert len(t.nearestNeighbors(key, size)) == size - 1    
        assert t.nearestNeighbors(key, size) == ft.nearestNeighbors(key, size)     

# randomly ensures correct Ball Tree behavior
def test_nss_torture():
    
    for i in range(20):
        
        # pick random size for tree
        size = random.randint(10, 1000)
    
        # generate random tree 
        p = generatePoints(random.randint(2,10), size,\
                           random.choice([False,True]), -10000, 10000) 
        
        t, ft = BallTree(p), FakeBallTree(p)
        
        # pick a random query point
        key, data = random.choice(p)
        
        # random number of neighbors, greater than size of Ball Tree
        n = random.randint(-100, size+100)
        
        # answer lists to compare
        t_ans, ft_ans = t.nearestNeighbors(key, n), ft.nearestNeighbors(key, n)
        
        # amount of neighbors MUST be size - 1
        if n < 1: assert t_ans == []
        elif n < size: 
            assert len(t_ans) == n  
            assert len(t_ans) == len(ft_ans)            
        else: 
            assert len(t_ans) == size - 1    
        assert t_ans == ft_ans
        
############ WITHIN RADIUS #################################################

# if the radius is 0 or less, return None
def test_bad_radius(): 
    
    for i in range(5):
    
        # generate random tree 
        p = generatePoints(random.randint(2,10), random.randint(10, 1000),\
                           random.choice([False,True]), -10000, 10000) 
        
        t = BallTree(p)
        
        # pick a random query point
        key, data = random.choice(p)
        
        # pick random negative amount of nearest neighbors
        assert t.countRadius(key, random.randint(-100, 0)) == None
        
# points that are being searched for must have the same dimensions as the points
# in the tree if the key's dimensions don't match the tree
def test_bad_radius_key(): 

    # three different randomly-generated Ball Trees
    for i in range(3):
        
        dim = random.randint(2,10)
        dType = random.choice([True, False])
        p = generatePoints(dim, random.randint(10, 100),\
                           dType, -10000, 10000)        
                
        t = BallTree(p)
        
        # randomly generated too-small and too-big tuples, random radius
        for i in range(5):
            k1 = generateKey(dim-1, dType)
            k2 = generateKey(dim+1, dType)
            assert t.countRadius(k1, random.randint(2,5)) == None
            assert t.countRadius(k2, random.randint(2,5)) == None
            
# test a radius that will return a lot of points (densely populated tree, big radius)
def test_large_radius_large_tree(): 
    
    # three different randomly-generated Ball Trees
    for i in range(3):
        
        dim = random.randint(2,10)
        dType = random.choice([True, False])
        # generate a densely populated tree, a lot of points with a small range for values 
        p = generatePoints(dim, random.randint(50, 100),\
                           dType, 0, 30)        
                
        t, f = BallTree(p), FakeBallTree(p)
        
        # test with a randomly generated key within same constraints
        for i in range(5):
            key = generateKey(dim-1, dType, 0, 30)
            # large radius
            radius = random.randint(30, 50)
            assert t.countRadius(key, radius) == f.countRadius(key, radius)
    
# test a radius that will return a lot of points (densely populated tree, small radius)
def test_small_radius_large_tree(): 
    
    # three different randomly-generated Ball Trees
    for i in range(3):
        
        dim = random.randint(2,10)
        dType = random.choice([True, False])
        # generate a densely populated tree, a lot of points with a small range for values 
        p = generatePoints(dim, random.randint(50, 100),\
                           dType, 0, 30)        
                
        t, f = BallTree(p), FakeBallTree(p)
        
        # test with a randomly generated key within same constraints
        for i in range(5):
            key = generateKey(dim-1, dType, 0, 30)
            # small radius
            radius = random.randint(1, 15)
            assert t.countRadius(key, radius) == f.countRadius(key, radius)    

# test a radius that will return a lot of points (sparesly populated tree, big radius)
def test_large_radius_small_tree(): 
    
    # three different randomly-generated Ball Trees
    for i in range(3):
        
        dim = random.randint(2,10)
        dType = random.choice([True, False])
        # generate a sparsely populated tree, a lot of points with a small range for values 
        p = generatePoints(dim, random.randint(50, 100),\
                           dType, -10000, 10000)        
                
        t, f = BallTree(p), FakeBallTree(p)
        
        # test with a randomly generated key within same constraints
        for i in range(5):
            key = generateKey(dim-1, dType, 0, 30)
            # large radius (bigger because tree is more spare)
            radius = random.randint(5000, 10000)
            assert t.countRadius(key, radius) == f.countRadius(key, radius) 

# test a radius that will return a lot of points (sparsely populated tree, small radius)
def test_small_radius_small_tree(): 
    
    # three different randomly-generated Ball Trees
    for i in range(3):
        
        dim = random.randint(2,10)
        dType = random.choice([True, False])
        # generate a sparsely populated tree, a lot of points with a small range for values 
        p = generatePoints(dim, random.randint(50, 100),\
                           dType, -10000, 10000)        
                
        t, f = BallTree(p), FakeBallTree(p)
        
        # test with a randomly generated key within same constraints
        for i in range(5):
            key = generateKey(dim-1, dType, 0, 30)
            # small radius (bigger because tree is more spare)
            radius = random.randint(500, 800)
            assert t.countRadius(key, radius) == f.countRadius(key, radius) 
    
# randomly choose any of these tests
def test_radius_torture(): pass

for i in range(20):
    n = random.randint(1, 1000)
    if n % 6 == 0: test_small_radius_large_tree()
    elif n % 6 == 1: test_bad_radius_key()
    elif n % 6 == 2: test_large_radius_large_tree() 
    elif n % 6 == 3: test_large_radius_small_tree()
    elif n % 6 == 4: test_small_radius_small_tree()
    elif n % 6 == 5: test_small_radius_small_tree()
    else: test_bad_radius()


pytest.main(["-v", "-s", "test_BallTree.py"])

