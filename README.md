# Python Ball Tree Class

A ball tree is a data structure used to organize points in a multidimensional space. It is useful for nearest neighbor searches and other proximity-based algorithms. Ball trees can efficiently conduct nearest-neighbor searches.


## Implementation

`BallTree(list points | str filename)`

Constructs Ball Tree from a list of points or from a .csv file 

If you're importing data from a CSV, it must have `data` in the first column, and the subsequent columns will be turned into the tuple for the `point` key. 

- Ball Tree:  `point`: (1,2,3,4), `data`: 0.314159265
- CSV  File: 0.314159265, 1, 2, 3, 4

> NOTE: It is the user's responsibility to ensure that the keys in the entries are all the same length. The Ball Tree will throw an error if the keys are of different lengths.

`getSize(self)`

Returns amount of points stored in the Ball Tree

`getRadius(self)`

Returns the radius of the root of the ball tree

`getDepth(self)`

&nbsp;&nbsp;&nbsp;&nbsp;Returns the height of Ball Tree including the root

`display(self)`

Displays a table of every Ball and its attributes (`data`, `radius`, `dim` of greatest spread and split, `depth`, and `pivot` point). Leaf nodes will always have a `radius` of 0 and `dim` of -1).

`find(self, tuple point)` 

Returns data associated with the query point; if not in the tree, returns `None`

`nearestNeighbors(self, tuple point, int nNeighbors)` 

Returns a list of the `nNeighbors` nearest points to `point` 

`countRadius(tuple point, float radius)` 

Returns a list of the points that are within `radius` distance to `point` 

`export(self, str filename)` 

Exports the points and data to a CSV file 

## References and Resources
- [Wikipedia Article](https://en.wikipedia.org/wiki/Ball_tree#:~:text=In%20computer%20science%2C%20a%20ball,a%20nested%20set%20of%20balls.)
- [Ball tree and KD Tree Algorithms](https://medium.com/@geethasreemattaparthi/ball-tree-and-kd-tree-algorithms-a03cdc9f0af9)


## License
The MIT License (MIT)

Copyright (c) 2024 Chaya Trapedo

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
