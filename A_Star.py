import heapq

# this is just the class for the cell and only contains a init with typical a* fields
class Cell:
    def __init__(self):
        # Parent cell's row
        self.parent_i = 0
        # Parent cell's column
        self.parent_j = 0
        # h + g
        self.f = float('inf')
        # Cost from start to this cell(g)
        self.g = float('inf')
        # Heuristic cost from this cell to destination(h)
        self.h = 0

ROW = 20
COL = 20

# Checks to see if a cell is in the grid
def is_valid(row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

# Checks if a cell is unblocked
def is_unblocked(grid, row, col):
    #print(grid)
    return grid[row][col] == 1

# Checks if a cell is the destination
def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

# Calculate the heuristic value of a cell (Euclidean distance to destination)
def calculate_h_value(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

# makes a path from getting the starting cell in the form of the object above and the destination in the same format
def trace_path(cell_details, dest):
    path = []
    row = dest[0]
    col = dest[1]

    # Trace the path from destination to source using parent cells
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col

    # Add the source cell to the path
    path.append((row, col))
    # flips the path to get the path in the correct order from source to destination
    path.reverse()
    return path

# Implements the A* search algorithm
def a_star_search(grid, src, dest):
    # Checks if the source and destination are on the board
    if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
        return

    # Check if the source and destination are unblocked
    # if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
    #    print("Source or the destination is blocked")
    #    return

    # Check if we are already at the destination
    if is_destination(src[0], src[1], dest):
        print("We are already at the destination")
        return
    # initializing the grid as a 2D array of cell objects
    # Initialize a list of visited cells
    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    # Initialize the details of each cell
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    # Initialize the start cell details
    i = src[0]
    j = src[1]
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    # Initialize the list of cells to be visited with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    # Main loop
    while len(open_list) > 0:
        # get the cell with the smallest f value from the open list
        p = heapq.heappop(open_list)

        # Mark the cell as visited
        i = p[1]
        j = p[2]
        closed_list[i][j] = True

        # For each direction, check the successors
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            # If the next cell is valid, unblocked, and not visited
            if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                # If the next cell is the destination
                if is_destination(new_i, new_j, dest):
                    # Set the parent of the destination cell
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    # Trace and print the path from source to destination
                    pat = trace_path(cell_details, dest)
                    return pat # return the path
                else:
                    # Calculate the new f, g, and h values
                    g_new = cell_details[i][j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, dest)
                    f_new = g_new + h_new

                    # If the cell is not in the open list or the new f value is smaller
                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        # Add the cell to the open list
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        # Update the cell details
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

# get the directions based on the path
def get_directions(path):
    directions = []
    if path == None:
        return directions
    for i in range(len(path) - 1):
        directions.append((-(path[i][0] - path[i + 1][0]), -(path[i][1] - path[i + 1][1])))
    return directions