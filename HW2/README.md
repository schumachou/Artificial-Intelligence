# Game-Playing Agent

## description
This project will introduce The Fruit Rage! A game that captures the nature of a zero-sum two-player game with strict limitation on allocated time for reasoning.

* At the beginning of each game, all cells are filled with fruits. Players play in turn and can pick a cell of the box in their own turn and claim all fruit of the same type, which are connected to the selected cell through horizontal and vertical paths.
* For each move the agent is rewarded a numeric value which is the square of the number of fruits claimed in that move.
* Once an agent picks the fruits from the cells, their empty place will be filled with other fruits on top of them. In this game, no fruit is added during game play. Hence, players play until all fruits have been claimed.
* the width and height of the square board (0 < n <= 26), the number of fruit types (0 < p <= 9).

## calibration
calibrate.py is used to help figure out the speed of the computer that the agent runs on. It runs before contest once and measures how long it takes to expand some fixed number of search nodes and save this into a single file called calibration.txt. When the agent runs during contest, it could then read calibration.txt in addition to reading input.txt, and use the data from calibration.txt to strategize about search depth.
