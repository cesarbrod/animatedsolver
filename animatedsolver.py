#!/home/brod/scripts/venv/bin/python

from collections import deque
import heapq
import time
import sys
import os

class Maze:
    def __init__(self, filepath):
        """Load maze from text file."""
        self.maze = []
        self.start = None
        self.end = None
        
        with open(filepath, 'r') as f:
            for i, line in enumerate(f):
                row = list(line.rstrip('\n'))
                self.maze.append(row)
                
                # Find start (A) and end (B) positions
                for j, cell in enumerate(row):
                    if cell == 'A':
                        self.start = (i, j)
                    elif cell == 'B':
                        self.end = (i, j)
        
        self.rows = len(self.maze)
        self.cols = len(self.maze[0]) if self.rows > 0 else 0
        
        if not self.start or not self.end:
            raise ValueError("Maze must contain 'A' (start) and 'B' (end) positions")
    
    def is_valid(self, pos):
        """Check if position is valid and not a wall."""
        r, c = pos
        return (0 <= r < self.rows and 
                0 <= c < self.cols and 
                self.maze[r][c] != 'X')
    
    def get_neighbors(self, pos):
        """Get valid neighboring positions (up, down, left, right)."""
        r, c = pos
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        
        for dr, dc in directions:
            new_pos = (r + dr, c + dc)
            if self.is_valid(new_pos):
                neighbors.append(new_pos)
        
        return neighbors
    
    def display(self, path=None, visited=None, current=None, algorithm_name=""):
        """Display the maze with optional path, visited nodes, and current position."""
        path_set = set(path) if path else set()
        visited_set = set(visited) if visited else set()
        
        # Clear screen and move cursor to top
        print("\033[2J\033[H", end='')
        
        # Display algorithm name at the top
        if algorithm_name:
            print(f"╔{'═' * 58}╗")
            print(f"║ {algorithm_name:^56} ║")
            print(f"╚{'═' * 58}╝")
            print()
        
        for i, row in enumerate(self.maze):
            line = ""
            for j, cell in enumerate(row):
                pos = (i, j)
                if cell == 'A' or cell == 'B':
                    line += cell
                elif pos == current:
                    line += '◉'  # Current position being explored
                elif pos in path_set:
                    line += '·'  # Mark final path
                elif pos in visited_set:
                    line += '░'  # Mark explored nodes
                else:
                    line += cell
            print(line)
        print()
    
    def display_final(self, path=None, visited=None):
        """Display final result without clearing screen."""
        path_set = set(path) if path else set()
        visited_set = set(visited) if visited else set()
        
        for i, row in enumerate(self.maze):
            line = ""
            for j, cell in enumerate(row):
                pos = (i, j)
                if cell == 'A' or cell == 'B':
                    line += cell
                elif pos in path_set:
                    line += '·'  # Mark final path
                elif pos in visited_set:
                    line += '░'  # Mark explored nodes
                else:
                    line += cell
            print(line)
        print()


class PathSolver:
    def __init__(self, maze, animate=False, delay=0.05):
        self.maze = maze
        self.animate = animate
        self.delay = delay
    
    def bfs(self):
        """Breadth-First Search - finds shortest path."""
        start_time = time.time()
        queue = deque([(self.maze.start, [self.maze.start])])
        visited = {self.maze.start}
        all_visited = [self.maze.start]
        nodes_explored = 0
        
        while queue:
            current, path = queue.popleft()
            nodes_explored += 1
            
            if self.animate:
                self.maze.display(None, all_visited, current, "Breadth-First Search (BFS)")
                time.sleep(self.delay)
            
            if current == self.maze.end:
                elapsed = time.time() - start_time
                return path, nodes_explored, elapsed, all_visited
            
            for neighbor in self.maze.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    all_visited.append(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        elapsed = time.time() - start_time
        return None, nodes_explored, elapsed, all_visited
    
    def dfs(self):
        """Depth-First Search - explores deeply first."""
        start_time = time.time()
        stack = [(self.maze.start, [self.maze.start])]
        visited = {self.maze.start}
        all_visited = [self.maze.start]
        nodes_explored = 0
        
        while stack:
            current, path = stack.pop()
            nodes_explored += 1
            
            if self.animate:
                self.maze.display(None, all_visited, current, "Depth-First Search (DFS)")
                time.sleep(self.delay)
            
            if current == self.maze.end:
                elapsed = time.time() - start_time
                return path, nodes_explored, elapsed, all_visited
            
            for neighbor in self.maze.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    all_visited.append(neighbor)
                    stack.append((neighbor, path + [neighbor]))
        
        elapsed = time.time() - start_time
        return None, nodes_explored, elapsed, all_visited
    
    def manhattan_distance(self, pos1, pos2):
        """Calculate Manhattan distance heuristic."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def a_star(self):
        """A* Search - uses heuristic for optimal pathfinding."""
        start_time = time.time()
        counter = 0
        heap = [(0, counter, self.maze.start, [self.maze.start])]
        visited = {self.maze.start: 0}
        all_visited = [self.maze.start]
        nodes_explored = 0
        
        while heap:
            f_score, _, current, path = heapq.heappop(heap)
            nodes_explored += 1
            
            if self.animate:
                self.maze.display(None, all_visited, current, "A* Search")
                time.sleep(self.delay)
            
            if current == self.maze.end:
                elapsed = time.time() - start_time
                return path, nodes_explored, elapsed, all_visited
            
            g_score = len(path) - 1
            
            for neighbor in self.maze.get_neighbors(current):
                new_g_score = g_score + 1
                
                if neighbor not in visited or new_g_score < visited[neighbor]:
                    if neighbor not in visited:
                        all_visited.append(neighbor)
                    visited[neighbor] = new_g_score
                    h_score = self.manhattan_distance(neighbor, self.maze.end)
                    new_f_score = new_g_score + h_score
                    counter += 1
                    heapq.heappush(heap, (new_f_score, counter, neighbor, path + [neighbor]))
        
        elapsed = time.time() - start_time
        return None, nodes_explored, elapsed, all_visited
    
    def greedy_best_first(self):
        """Greedy Best-First Search - uses only heuristic."""
        start_time = time.time()
        counter = 0
        heap = [(0, counter, self.maze.start, [self.maze.start])]
        visited = {self.maze.start}
        all_visited = [self.maze.start]
        nodes_explored = 0
        
        while heap:
            _, _, current, path = heapq.heappop(heap)
            nodes_explored += 1
            
            if self.animate:
                self.maze.display(None, all_visited, current, "Greedy Best-First Search")
                time.sleep(self.delay)
            
            if current == self.maze.end:
                elapsed = time.time() - start_time
                return path, nodes_explored, elapsed, all_visited
            
            for neighbor in self.maze.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    all_visited.append(neighbor)
                    h_score = self.manhattan_distance(neighbor, self.maze.end)
                    counter += 1
                    heapq.heappush(heap, (h_score, counter, neighbor, path + [neighbor]))
        
        elapsed = time.time() - start_time
        return None, nodes_explored, elapsed, all_visited


def main():
    print("=" * 60)
    print("MAZE PATH SOLVER - Multiple Search Algorithms")
    print("=" * 60)
    print("\nMaze Format:")
    print("  - Empty spaces: walkable paths")
    print("  - 'X': walls")
    print("  - 'A': start point")
    print("  - 'B': end point")
    print()
    
    # Ask for maze file
    filepath = input("Enter the path to the maze text file: ").strip()
    
    try:
        with open(filepath, 'r') as f:
            pass  # Test if file exists
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found!")
        return
    except Exception as e:
        print(f"Error opening file: {e}")
        return
    
    try:
        maze = Maze(filepath)
        print(f"\nMaze loaded successfully!")
        print(f"Dimensions: {maze.rows} x {maze.cols}")
        print(f"Start: {maze.start}, End: {maze.end}\n")
        
        print("Original Maze:")
        maze.display_final()
        
        # Ask about animation
        animate_choice = input("Do you want to see animated algorithm execution? (y/n): ").strip().lower()
        animate = animate_choice == 'y'
        
        animation_delay = 0.05
        if animate:
            try:
                delay_input = input("Enter animation delay in seconds (default 0.05, press Enter to skip): ").strip()
                if delay_input:
                    animation_delay = float(delay_input)
            except ValueError:
                print("Invalid delay, using default 0.05 seconds")
                animation_delay = 0.05
        
        solver = PathSolver(maze, animate=animate, delay=animation_delay)
        
        algorithms = {
            '1': ('Breadth-First Search (BFS)', solver.bfs),
            '2': ('Depth-First Search (DFS)', solver.dfs),
            '3': ('A* Search', solver.a_star),
            '4': ('Greedy Best-First Search', solver.greedy_best_first),
            '5': ('Compare All Algorithms', None)
        }
        
        while True:
            print("\n" + "=" * 60)
            print("Select a search algorithm:")
            for key, (name, _) in algorithms.items():
                print(f"  {key}. {name}")
            print("  0. Exit")
            print("=" * 60)
            
            choice = input("\nYour choice: ").strip()
            
            if choice == '0':
                print("Exiting. Goodbye!")
                break
            
            if choice not in algorithms:
                print("Invalid choice. Please try again.")
                continue
            
            if choice == '5':
                # Compare all algorithms
                print("\n" + "=" * 60)
                print("COMPARING ALL ALGORITHMS")
                print("=" * 60)
                
                results = []
                for key in ['1', '2', '3', '4']:
                    name, func = algorithms[key]
                    if animate:
                        print(f"\nAnimating: {name}")
                        print("Press Ctrl+C to skip animation...\n")
                        time.sleep(1)
                    
                    try:
                        path, nodes, elapsed, all_visited = func()
                        results.append((name, path, nodes, elapsed, all_visited))
                        
                        if animate:
                            time.sleep(1)  # Pause between algorithms
                    except KeyboardInterrupt:
                        # User skipped animation, continue with non-animated version
                        print("\n\nAnimation skipped. Running without animation...")
                        solver_no_anim = PathSolver(maze, animate=False)
                        func_no_anim = getattr(solver_no_anim, func.__name__)
                        path, nodes, elapsed, all_visited = func_no_anim()
                        results.append((name, path, nodes, elapsed, all_visited))
                
                # Clear screen for final results
                if animate:
                    print("\033[2J\033[H", end='')
                
                # Show statistics table
                print("\n" + "=" * 60)
                print("ALGORITHM COMPARISON - STATISTICS")
                print("=" * 60)
                print(f"\n{'Algorithm':<30} | {'Path Length':<12} | {'Nodes Explored':<15} | {'Time (s)':<12}")
                print("-" * 78)
                
                for name, path, nodes, elapsed, _ in results:
                    path_len = str(len(path)) if path else "No path"
                    print(f"{name:<30} | {path_len:<12} | {nodes:<15} | {elapsed:.6f}")
                
                # Show visualizations for all algorithms
                print("\n" + "=" * 60)
                print("VISUAL COMPARISON")
                print("=" * 60)
                print("\nLegend:")
                print("  A = Start point")
                print("  B = End point")
                print("  · = Final solution path")
                print("  ░ = Explored nodes (not in final path)")
                print("  X = Walls")
                print("    = Unexplored walkable areas")
                
                for name, path, nodes, elapsed, all_visited in results:
                    print(f"\n{'-' * 60}")
                    print(f"{name}")
                    print(f"{'-' * 60}")
                    if path:
                        visited_not_in_path = [v for v in all_visited if v not in path]
                        maze.display_final(path, visited_not_in_path)
                    else:
                        print("No path found!")
                        maze.display_final(None, all_visited)
                
            else:
                name, func = algorithms[choice]
                print(f"\n{'=' * 60}")
                print(f"Running: {name}")
                print(f"{'=' * 60}")
                
                if animate:
                    print("\nPress Ctrl+C to skip animation...\n")
                    time.sleep(1)
                
                try:
                    path, nodes_explored, elapsed, all_visited = func()
                except KeyboardInterrupt:
                    print("\n\nAnimation skipped. Running without animation...")
                    solver_no_anim = PathSolver(maze, animate=False)
                    func_no_anim = getattr(solver_no_anim, func.__name__)
                    path, nodes_explored, elapsed, all_visited = func_no_anim()
                
                # Clear screen for final results
                if animate:
                    print("\033[2J\033[H", end='')
                
                # Show statistics table
                print(f"\n{'Algorithm':<30} | {'Path Length':<12} | {'Nodes Explored':<15} | {'Time (s)':<12}")
                print("-" * 78)
                path_len = str(len(path)) if path else "No path"
                print(f"{name:<30} | {path_len:<12} | {nodes_explored:<15} | {elapsed:.6f}")
                
                if path:
                    print(f"\n✓ Path found!")
                    print(f"\nLegend:")
                    print(f"  A = Start, B = End")
                    print(f"  · = Final solution path")
                    print(f"  ░ = Explored nodes (not in final path)")
                    print(f"\nMaze with exploration visualization:")
                    visited_not_in_path = [v for v in all_visited if v not in path]
                    maze.display_final(path, visited_not_in_path)
                else:
                    print(f"\n✗ No path found!")
                    print(f"\nMaze showing explored areas:")
                    maze.display_final(None, all_visited)
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()