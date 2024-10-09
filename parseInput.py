def parse_input_file(file_path):
    with open(file_path, 'r') as file:
        # Read start and goal coordinates
        start_end = list(map(int, file.readline().split()))
        start = (start_end[0], start_end[1])
        end = (start_end[2], start_end[3])

        # Initialize the grid
        grid = []

        # Read the grid
        for _ in range(30):
            row = list(map(int, file.readline().split()))
            grid.append(row)

        # Reverse the grid to match the coordinate system
        grid.reverse()

    return start, end, grid

