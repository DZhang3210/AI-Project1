from parseInput import parse_input_file
from AStar import AStar, format_output
from files.vis import plot_maze

def main():
    #index of the input file
    index = 2
    # Set the k value for angle cost calculation
    k = 4  # You can adjust this value as needed

    # Parse input
    start_state, goal_state, grid = parse_input_file('inputs/input'+str(index)+'.txt')

    # Run A* algorithm
    result = AStar(k, start_state, goal_state, grid)

    if result:
        depth, nodes_expanded, path, action_sequence = result
        # Format and print output
        output = format_output(depth, nodes_expanded, path, start_state, goal_state, grid, action_sequence)
        
        # Write full output to output1-k.txt
        with open(f'outputs/output{index}-{k}.txt', 'w') as file:
            file.write(output)
        
        # Extract the maze portion from output1-k.txt
        with open(f'outputs/output{index}-{k}.txt', 'r') as file:
            lines = file.readlines()
            maze_output = ''.join(lines[3:])  # Start from the 4th line to the end
        
        # Write the extracted maze to output1-k-maze.txt
        with open(f'outputs/output{index}-{k}-maze.txt', 'w') as file:
            file.write(maze_output)
        
        # Call the visualization function
        plot_maze(f'outputs/output{index}-{k}-maze.txt')
    else:
        print("No path found")

if __name__ == "__main__":
    main()
