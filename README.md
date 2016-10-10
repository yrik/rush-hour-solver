# Rush Hour Solver

A program to solve Rush Hour game.

**The Rush Hour game** is a board game
in general played on an n-by-n grid (in our
case 6 by 6) with various car pieces placed on
the board. These cars can be either two or
three units in length and their movement
respects their orientation (i.e. a car facing
North can move North or South) as would be
expected. There is one special car which is
colored red and is aligned with an exit space
on the border of the grid. The object of the
game is to move the other vehicles such that
the red car can escape unobstructed.

**Method to solve** is a breadth first search. 
We take intial state of the cars and generate next states,
which includes all possible moves of the cars,
for each generated state we repeat it again.
We iterate over the possible moves until red car is moved
to the exit on right side of the board.

**Demo:** [Try demo here](https://rush-hour-solver.herokuapp.com/). Note: there is a limit of max 30 sec excecution time, not all boards can be solved within this time.

Rrerequisites
---
 - Python 2.7

Usage
---

To run basic sample:
```
python solver.py
```

To run tests and more samples:
```
python tests.py
```

To run custom sample:
```
from solver import Solver

# Put your own data into `board_data` var.
# `rr` - means red car to be freed.
# Cars should use unique characters, 
# so if you have AA car, do not repeat A char again.
# Red car can have exit only on the right side of the board.
board_data = '''
    ....AA
    ..BBCC
    rr..EF
    GGHHEF
    ...IEF
    ...IJJ
'''

solver = Solver()
solver.load_data(board_data)
print 'Loaded data'
print solver.format_data(solver.cars)
print 'Looking for solution.. (may take several secods)'
moves = solver.solve()
print solver.format_steps(solver.cars, moves)
```

