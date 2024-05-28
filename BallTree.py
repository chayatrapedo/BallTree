"""
I, Chaya Trapedo, hereby certify that this program is solely the result of my own work and 
is in compliance with the Academic Integrity policy of the course syllabus and 
the academic integrity policy of the CS department.

About This Ball Tree Implementation: 

* Ball Tree does not support duplicate keys

* Leaf size is one point and cannot be changed

* CSV must have data in the first column, and the subsequent columns will be turned
  into data. It will be written in the same way:
       
                 Ball Tree                             CSV File
  E.G. Key (1,2,3,4), Data (0.31415927)   <->    0.31415927, 1, 2, 3, 4
  
  NOTE: It is the user's responsibility to ensure that the keys in the entries are 
  all the same length. The Ball Tree will not work if the keys are of different lengths.

"""

import math
import random
import heapq

# "Nodes" that support the underlying structure of the Ball Tree
class Ball(object):

    def __init__(self, pivot, data, rad, dim): 
        self.pivot = pivot      # tuple of points
        self.data = data        # data associated with original key
        self.square_rad = rad   # distance between pivot and its furthest subpoint
        self.dim = dim          # the dimension of the data that the roots subpoints
                                # were split on for this depth
        self.leftChild = None   # reference to left Ball child, resursively assigned
                                # in construction method
        self.rightChild = None  # reference to right Ball child, resursively assigned
                                # in construction method

# Class that arranges Ball objects to operate as a Ball Tree
class BallTree(object):
    
    # Ball Tree accessors
    def getSize(self): return self.__size           # amount of nodes in Ball Tree
    def getRadius(self): return math.sqrt(self.__root.square_rad) # radius of root

    
    # Creates a ball tree from tuples of key/data pairs or a CSV file (*under the 
    # correct conditions)
    def __init__(self, points):
        
        self.__size = 0
        
        # if the Ball Tree is initialized with a file name, the data in the CSV
        # needs to be converted to a list of tuples
        if type(points) == type(""): 
            
            if not points.endswith(".csv"):
                print("Must be a .csv file.")
                return
            # convert the points into a points file
            imported = BallTree.__fromFile(points)
            # initialize the tree with the imported points
            self.__root = self.__constructBallTree(imported) 
            
        else: # the ball tree can be constructed with points because it's already a tuple list
            self.__root = self.__constructBallTree(points)   
    
    
    # Recursive construction algorithim for the ball tree
    # Input is a list of point/data tuples that have not already turned into nodes
    def __constructBallTree(self, points):
               
        # If there's only one point in the input list (this will be a leaf node)
        if len(points) == 1:
            
            # initialize a new ball
            b = Ball(points[0][0], points[0][1], 0, -1) # radius of 0 for leaf node
                                                               # dim of spread is -1 (no other points to compare)
            self.__size += 1                               # increment size whenever a new Ball is created
            
            return b # returns to its parent one layer up
                
        else:
            # calculate the dimension of greatest spread among the points
            maxDim = BallTree.__dimGreatestSpread(points)
            
            # find the pivot point for the new Ball based on the dimension of greatest spread
            pivot, data = BallTree.__pivotPoint(points, maxDim)
            
            # initialize lists of points for that will be passed to the left and right children, 
            # and start tracking the radius
            l, r = [],[]
            rad = 0 
            
            # go through all the points to sort to left or right children           
            for point in points:
                
                # not passing a pivot to its children 
                if point[0] != pivot: 
                    
                    # store largest distance between the current point and pivot
                    # as the radius
                    rad = max(rad, BallTree.__squareDist(point[0], pivot))
                    
                    # assign each point to left child or right child if its 
                    # less than or greater than the value of the pivot point on 
                    # the dimension of maximum spread
                    if point[0][maxDim] < pivot[maxDim]: l.append(point)
                    else: r.append(point)
                    
            
            # initialize new Ball
            b = Ball(pivot, data, rad, maxDim)
            self.__size += 1
            
            # create its children based on the l and r lists
            if len(l) > 0: b.leftChild = self.__constructBallTree(l)
            if len(r) > 0: b.rightChild = self.__constructBallTree(r)
            
            return b # return reference of root node to the init
        
    # takes a list of tuples of the tuple keys, data
    # address for list of 2 or greater, one or less
    def __dimGreatestSpread(points): 
        
        # determine number of dimensions by via length of the tuple "points" key
        nDims = len(points[0][0]) - 1
        
        # initialize lists to negative and positive infinities to determine the 
        # min and max values of each dimension in the keys
        listMins, listMaxs = [math.inf] * nDims, [-math.inf] * nDims

        for key in points: 
            
            for i in range(nDims):
                
                # store the minumum and maximums of each dimension                
                if key[0][i] < listMins[i]: listMins[i] = key[0][i]
                if key[0][i] > listMaxs[i]: listMaxs[i] = key[0][i]
        
        # the difference between mins and maxs is the spread, keep track of max spread
        # and the dimension in which it is found
                
        # initialize variable in dimension 0 with a fence-post approach
        maxSpread = abs(listMaxs[0] - listMins[0])
        mDim = 0
        
        # check against the rest of the dimnesions
        for i in range(1, nDims):
            spread = abs(listMaxs[i] - listMins[i])
            if spread > maxSpread:
                maxSpread = spread
                mDim = i
                
        return mDim
            
    # find pivot using the median of 3
    def __pivotPoint(keys, dim): 
        
        # get the first, last, and middle keys
        left = keys[0]
        right = keys[-1]
        pivot = keys[len(keys)//2]

        # select pivot using median of three 
        if pivot[0][dim] < left[0][dim]: pivot, left = left, pivot
        if right[0][dim] < left[0][dim]: right, left = left, right
        if pivot[0][dim] < right[0][dim]: right, pivot = pivot, right
        
        return pivot
    
    # returns the data at the queried point
    def find(self, key):
        return self.__findData(key, self.__root)
    
    # recursively searches for the queried point and returns its data or None
    def __findData(self, key, b):
        
        if not b: return None
        
        # return data if point is found
        if key == b.pivot: return b.data
        
        # if the current point has no children, the point isn't in this recursive
        # descent
        if not b.leftChild and not b.rightChild: return None
        
        # if the key inputed is not the same dimensions as the keys in the tree
        # it's not going to be in the tree
        if len(key) != len(b.pivot): return None
        
        # compare the value of the search key on the Balls's dimension of split
        # to the value of the value of the pivot on the dimension, and recurse to 
        # the left or right based on if it's greater or less than the pivot, mirroring
        # the construction algorithm
        if key[b.dim] < b.pivot[b.dim]: return self.__findData(key, b.leftChild)
        else: return self.__findData(key, b.rightChild)    

    # wrapper class; extracts just points from a list of distances and points
    def nearestNeighbors(self, point, k=1):
        
        # point must be of the same dimensions of the tree to be searchable
        if len(point) != len(self.__root.pivot): return None
        
        nearestNeighors = [ ]
        if k < 1: return nearestNeighors # need to search for at least 1 neighbor

        
        # recursively search for k nearest neighbors
        ans = self.__knn(point, k, [], self.__root)
        
        # put answers in order of closest distance (un-heapify)
        # sort so the answer can be compared with the Fake BallTree        
        ans.sort()
        
        # extract just the points for answer
        nearestNeighors = [node[1] for node in ans]
        
        return nearestNeighors    
    
    # recursive search for k nearest neighbors
    def __knn(self, point, k, q, b): 
        
        # distance between current point and query point
        curDist = BallTree.__squareDist(point, b.pivot)
        
        # if current node is a leaf node
        if not b.leftChild and not b.rightChild:
            
            # a point cannot be its own nearest neighbor 
            if curDist != 0:
                
                # accumulate k distances 
                if len(q) < k: heapq.heappush(q, (curDist, b.pivot))
                else: 
                    # if the length exceeds k, save k smallest distances 
                    heapq.heappush(q, (curDist, b.pivot))
                    q = heapq.nsmallest(k, q)
            return q
                
        # a point cannot be its own nearest neighbor         
        if curDist != 0:
            
            # accumulate k distances
            if len(q) < k: heapq.heappush(q, (curDist, b.pivot))
            else: 
                # if the length exceeds k, save k smallest distances 
                heapq.heappush(q, (curDist, b.pivot))
                q = heapq.nsmallest(k, q)
        
        # if the children exist, check their pivots' distances
        if b.leftChild: q = self.__knn(point, k, q, b.leftChild)
        if b.rightChild: q = self.__knn(point, k, q, b.rightChild)
        
        return q
            
        
    # returns a list of nodes within a certain radius from a point
    def countRadius(self, point, radius):
        
        # must be a valid point and radius
        if len(point) != len(self.__root.pivot) or radius <= 0: return None
        
        withinRadius = self.__inRadius(point, radius**2, self.__root, [])
        
        # sort so the answer can be compared with the Fake BallTree
        withinRadius.sort()
        
        return withinRadius
    
    
    # recursive searches for the neighbors within sqRad of point
    def __inRadius(self, point, sqRad, b, ans):
        
        # if it's not the same point
        if point != b.pivot:  
        
            # if Ball b is a leaf-node
            if not b.leftChild and not b.rightChild: 
                
                # if the distance is within the sqRad, append 
                if BallTree.__squareDist(point, b.pivot) < sqRad:
                    ans += [b.pivot]
                    return ans
            
            # if the distance is within the sqRad, append 
            if BallTree.__squareDist(point, b.pivot) < sqRad:
                ans += [b.pivot]
            
        # call on children
        if b.leftChild: ans = self.__inRadius(point, sqRad, b.leftChild, ans)
        if b.rightChild: ans = self.__inRadius(point, sqRad, b.rightChild, ans)
        
        return ans            
           
    # converts data from a CSV to a list of tuples and data for Ball Tree construction
    def __fromFile(filename):
        
        csv = open(filename)
        ans = []
        
        for line in csv:
            
            # get rid of the new line 
            line = line.replace("\n","")
            # split entries into strings
            entrycsv = line.split(',')
            
            # the first entry will always be the data
            data = float(entrycsv[0])
            
            # the rest of the entry will become a tuple of points
            point = tuple()
            for i in range(1, len(entrycsv)):
                point += float(entrycsv[i]),
                
            # combine the point and the data, append to answer list
            entry = point, data,
            ans += [entry]
        
        csv.close()
        return ans
    
    # writes ist of tuples and data from Ball Tree to CSV file
    def __toFile(filename, export):
        
        csv = open(filename, "w")
        ans = []
        
        # for each entry
        for entry in export:
            
            # create an answer string
            line = ""
            
            # append the data to the beginning of the answer string
            line += str(entry[1])
            
            # str-ify the tuple, remove the parenthesis, and add to answer string
            # with comma at beginning new line to seperate from data and later entries
            points = str(entry[0])
            line += "," + points[1:-1] + '\n'
            
            # write line to file
            csv.write(line)
        
        # close file when done
        csv.close()   
    
    # Displays the Ball Tree and its attributes in a table 
    def display(self):
        
        print("%-11s %-11s %-10s %-15s" % ("Data:", "Radius:", "Dim. Split:", "Point:"))
        results = self.__toList(self.__root, [])
        for entry in results:
            print("%-10.5f %-10.5f %-10d %-15s" % (entry[1], math.sqrt(entry[2]), entry[3], str(entry[0])))
        
        
    # converts data from a CSV to a list of tuples and data for Ball Tree construction
    def export(self, filename=None):
        
        # if no file name is provided, will write a new file name under
        if not filename: filename = "BallTree.csv"
        toList = self.__toList(self.__root, [])  
        export = [entry[0:2] for entry in toList]
        BallTree.__toFile(filename, export)
    
        
    # converts data from a CSV to a list of tuples and data for Ball Tree construction
    def __toList(self, b, ans):
        
        if not b.leftChild and not b.rightChild:
            ans += [(b.pivot, b.data, b.square_rad, b.dim)]
            return ans
        
        ans += [(b.pivot, b.data, b.square_rad, b.dim)]
        
        if b.leftChild: ans = self.__toList(b.leftChild, ans)
        if b.rightChild: ans = self.__toList(b.rightChild, ans)
        
        return ans    
        
        
    # multi-dimensional distance formula
    def __squareDist(start, end):
    
        dist = 0
        
        # calculate the square distance based on the amount of dimensions
        for i in range(len(start)):
            dist += ((start[i] - end[i]) ** 2)
    
        return dist


# Utility Methods:

# Creates random multi-dimentional int keys and float data 
# Input: int for dimension size, int for amount of data entrys, boolean floats for
#        data type, minimum data value, maximum data value
# Output: a list of tuples of random d-dimensional keys and amt float data points in at most amt keys
def generatePoints(d, amt, floats=False, minVal=0, maxVal=1000):
    
    # dictionary of tuples as keys, random data as values
    data = []
    
    # for the amount of data requested (accounting for keys with duplicate amounts of data)
    while len(data) < amt:
        
        # create a tuple to contain each data entry
        coordinate = generateKey(d, floats, minVal, maxVal)
            
        # create the tuple of the point and data
        entry = coordinate, random.random(),
        
        # add to dictionary, without duplicates
        if entry not in data: data += [entry]
    
    return data


# randomly generate a multi-dimensional tuple key
# Input: int d for dimension size, boolean floats for data type, minimum data value, maximum data value
# Output: a tuple key of random d-dimensional values
def generateKey(d, floats, minVal=0, maxVal=1000):
    # create a tuple to contain each data entry
    coordinate = tuple()
    
    # fill the tuple with random numbers
    for i in range(d):
        # concatenate tuples to get a tuple with d items
        if floats: coordinate += random.uniform(minVal, maxVal),
        else: coordinate += random.randint(int(minVal), int(maxVal)),
         
    return coordinate


def main():
    
    # generate data - situation 0 - find() and export/display()
    points = generatePoints(6, 100, False, 1, 30)

    a = BallTree(points)
    
    # find data for a key in the tree
    key, data = points[0]
    found = a.find(key)
    print(f"Finding the data for a {key} in the tree: {found}")
    print(f"It is {found == data} that find() works")
    
    # nearestNeighbors
    numNeighbors = random.randint(5,10)
    print(f"\nThe {numNeighbors} nearest neighbors to {key} are: \n{a.nearestNeighbors(key, numNeighbors)}")
    
    # within radius
    radius = random.randint(11, 20)
    print(f"\nThe points that are within a {radius} distance from {key} are: \n{a.countRadius(key, radius)}")    
    
    
    # display to compoare to export
    print("\nTree A data (to compare with test.csv:)")
    a.display()    
    a.export("test.csv")
    
    # import points
    datasets = ["randomdata1.csv", "randomdata2.csv", "randomdata3.csv"]
    choice = random.choice(datasets)
    b = BallTree(choice)
    print(f"\nThe ball tree imported from {choice}:")
    b.display()
    
    
    
if __name__ == "__main__":
    main()