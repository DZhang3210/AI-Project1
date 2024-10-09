#0 = RIGHT
#1 = TOP-RIGHT
#2 = UP
#3 = TOP-LEFT
#4 = LEFT
#5 = BOTTOM-LEFT
#6 = DOWN
#7 = BOTTOM-RIGHT


import math

def calculate_angle_cost(k, initial_state, end_state):
    dx = end_state[0] - initial_state[0]
    dy = end_state[1] - initial_state[1]
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    if angle_deg > 180: angle_deg = 360 - angle_deg
    return k * (angle_deg/180)


def calculate_distance_cost(action):
    if action in [0,2,4,6]: return 1
    if action in [1,3,5,7]: return math.sqrt(2)

def heuristic(current_state, goal_state):
    # Calculate the Euclidean distance between current_state and goal_state
    dx = goal_state[0] - current_state[0]
    dy = goal_state[1] - current_state[1]
    return math.sqrt(dx**2 + dy**2)

def get_neighbors(current_state, grid):
    neighbors = []
    x, y = current_state
    directions = [
        (1, 0), (-1, 0), (0, 1), (0, -1),  # Right, Left, Down, Up
        (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonals
    ]
    
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if (0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid) and
            grid[new_y][new_x] != 1):  # Check if within bounds and not an obstacle
            neighbors.append((new_x, new_y))
    return neighbors

def AStar(k, start_state, goal_state, grid):
    # Initialize the cost dictionary and parent dictionary
    cost = {start_state: 0}
    parent = {start_state: None}
    
    # Initialize the priority queue and nodes expanded counter
    priority_queue = [(0, start_state)]
    nodes_expanded = 0

    while priority_queue:
        # Get the state with the lowest cost
        current_cost, current_state = min(priority_queue, key=lambda x: x[0])
        priority_queue.remove((current_cost, current_state))
        nodes_expanded += 1

        # Check if the current state is the goal state
        if current_state == goal_state:
            # Reconstruct the path
            path = []
            while current_state:
                path.append(current_state)
                current_state = parent[current_state]
            path.reverse()
            
            # Calculate depth (path length - 1)
            depth = len(path) - 1
            
            return depth, nodes_expanded, path

        # Get the neighbors of the current state
        neighbors = get_neighbors(current_state, grid)

        for neighbor in neighbors:
            # Calculate the cost to reach the neighbor
            new_cost = cost[current_state] + calculate_distance_cost(current_state, neighbor) + calculate_angle_cost(k, current_state, neighbor)

            # If the neighbor is not in the cost dictionary or the new cost is lower
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal_state)
                priority_queue.append((priority, neighbor))
                parent[neighbor] = current_state

    # If no path is found
    return None, nodes_expanded, None

def format_output(depth, nodes_expanded, path, start_state, goal_state, grid):
    # Print depth and nodes expanded
    output = f"{depth}\n{nodes_expanded}\n"

    # Create a copy of the grid to modify
    output_grid = [row[:] for row in grid]

    # Mark the path
    if path:
        for x, y in path:
            if (x, y) != start_state and (x, y) != goal_state:
                output_grid[y][x] = 4

    # Mark start and goal positions (overwriting path if necessary)
    output_grid[start_state[1]][start_state[0]] = 2
    output_grid[goal_state[1]][goal_state[0]] = 5

    # Convert grid to string representation
    for row in reversed(output_grid):  # Reverse to match input format
        output += ' '.join(map(str, row)) + '\n'

    return output.strip()  # Remove trailing newline







            

    

