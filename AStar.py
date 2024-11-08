import math
import heapq
#0 = RIGHT
#1 = TOP-RIGHT
#2 = UP
#3 = TOP-LEFT
#4 = LEFT
#5 = BOTTOM-LEFT
#6 = DOWN
#7 = BOTTOM-RIGHT

#calculates the angle cost given k and the initial and end states
def calculate_angle_cost(k, current_angle,  initial_state, end_state):
    dx = end_state[0] - initial_state[0]
    dy = end_state[1] - initial_state[1]
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    if(current_angle is None):
        return 0
    current_angle_diff = abs(angle_deg - current_angle)
    if current_angle_diff > 180:
        current_angle_diff = 360 - current_angle_diff
    return k * (current_angle_diff/180)

#calculates the distance cost given the current state and the neighbor
def calculate_distance_cost(current_state, neighbor):
    dx = neighbor[0] - current_state[0]
    dy = neighbor[1] - current_state[1]
    if dx != 0 and dy != 0:  # Diagonal move
        return math.sqrt(2)
    else:  # Horizontal or vertical move
        return 1

#calculates the heuristic cost given the current state and the goal state
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
    # Initialize the dictionaries
    cost = {start_state: 0}
    parent = {start_state: None}
    actions = {start_state: None}
    f_values = {start_state: 0}
    
    # Initialize the priority queue using heapq
    open_list = [(0, None, start_state)]
    #Cost, Angle, State
    heapq.heapify(open_list)
    nodes_expanded = 0
    closed = set()
    
    while open_list:
        # Get the state with lowest f-value using heappop
        current_cost, current_angle, current_state = heapq.heappop(open_list)
        
        # Skip if we've already processed this state
        if current_state in closed:
            continue
            
        closed.add(current_state)
        nodes_expanded += 1

        if current_state == goal_state:
            # Reconstruct the path and actions
            path = []
            action_sequence = []
            f_value_sequence = []  # New list to store f-values
            #while the current state is not the start state
            while current_state:
                path.append(current_state)
                if actions[current_state] is not None:
                    action_sequence.append(actions[current_state])
                    f_value_sequence.append(f_values[current_state])  # Store f-value
                current_state = parent[current_state]
            path.reverse()
            action_sequence.reverse()
            f_value_sequence.reverse()  # Reverse f-values
            # Calculate depth (path length - 1)
            depth = len(path) - 1
            
            return depth, nodes_expanded, path, action_sequence, f_value_sequence

        neighbors = get_neighbors(current_state, grid)
        
        for neighbor in neighbors:
            if neighbor in closed:
                continue
            
            
            new_cost = cost[current_state] + calculate_distance_cost(current_state, neighbor) + calculate_angle_cost(k, current_angle, current_state, neighbor)
            
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                f_value = new_cost + heuristic(neighbor, goal_state)
                # No need to manually remove old entries - just push the new one
                new_angle = math.degrees(math.atan2(neighbor[1] - current_state[1], neighbor[0] - current_state[0]))
                heapq.heappush(open_list, (f_value, new_angle, neighbor))
                parent[neighbor] = current_state
                actions[neighbor] = get_action(current_state, neighbor)  # Store the action
                f_values[neighbor] = f_value  # Store f-value

    # If no path is found
    return None, nodes_expanded, None, None, None

def format_output(depth, nodes_expanded, path, start_state, goal_state, grid, actions, f_values):
    # Print depth, nodes expanded, and actions
    output = f"{depth}\n{nodes_expanded}\n"

    # Add all actions on one line
    output += ' '.join(map(str, actions)) + '\n'
    
    # Add all f-values on the next line
    output += ' '.join(f"{f_value:.1f}" for f_value in f_values) + '\n'

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


#returns the action given the current state and the next state
def get_action(current_state, next_state):
    dx = next_state[0] - current_state[0]
    dy = next_state[1] - current_state[1]
    
    if dx == 1 and dy == 0:
        return 0  # RIGHT
    elif dx == 1 and dy == 1:
        return 1  # TOP-RIGHT
    elif dx == 0 and dy == 1:
        return 2  # UP
    elif dx == -1 and dy == 1:
        return 3  # TOP-LEFT
    elif dx == -1 and dy == 0:
        return 4  # LEFT
    elif dx == -1 and dy == -1:
        return 5  # BOTTOM-LEFT
    elif dx == 0 and dy == -1:
        return 6  # DOWN
    elif dx == 1 and dy == -1:
        return 7  # BOTTOM-RIGHT
