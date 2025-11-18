# animatedsolver
A python program using search techniques to solve a maze

## Search Algorithms:

- Breadth-First Search (BFS) - Guarantees shortest path, explores level by level
- Depth-First Search (DFS) - Explores deeply first, may not find shortest path
- A Search* - Optimal pathfinding using Manhattan distance heuristic
- Greedy Best-First Search - Uses heuristic only, faster but not always optimal

## Capabilities:

- Reads maze from a text file (maze1.txt provided as an example)
- Displays the original maze
- Shows the solution path marked with dots (·)
- Compares performance metrics: path length, nodes explored, execution time
- Option to compare all algorithms at once

## Animated Algorithm Execution:

Watch the algorithm explore the maze in real-time
The current node being explored is marked with ◉
Previously explored nodes appear as ░
The algorithm name is displayed at the top in a nice border

## Animation Options:

At startup, you're asked if you want animation (y/n)
You can customize the animation delay (default 0.05 seconds)
Faster animations for quick overview, slower for detailed study

## Skip Animation Anytime:

Press Ctrl+C during animation to skip and see final results immediately
The program will continue without animation

## Visual Indicators:

◉ = Current position being explored (only during animation)

· = Final solution path

░ = Explored but not in final path

A = Start, B = End

X = Walls

## Statistics:

All statistics tables are shown after animation completes
You can see both the animated exploration AND the final comparison

The animation really helps visualize how different algorithms explore the maze:

BFS: You'll see a wave expanding uniformly
DFS: Watch it dive deep into one path before backtracking
A*: See it intelligently move toward the goal
Greedy: Notice how it rushes toward the target

Greedy: Notice how it rushes toward the target

Try it with different delay values to see the algorithms in action!
