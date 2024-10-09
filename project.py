from parseInput import parse_input_file
from AStar import AStar, format_output

def main():
    # Parse input
    start_state, goal_state, grid = parse_input_file('input.txt')

    # Set the k value for angle cost calculation
    k = 0.5  # You can adjust this value as needed

    # Run A* algorithm
    depth, nodes_expanded, path = AStar(k, start_state, goal_state, grid)

    # Format and print output
    if path:
        output = format_output(depth, nodes_expanded, path, start_state, goal_state, grid)
        print(output)
        with open('output.txt', 'w') as file:
            file.write(output)
    else:
        print("No path found")

if __name__ == "__main__":
    main()
