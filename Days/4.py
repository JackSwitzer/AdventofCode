import re

def read_input(file_path):
    with open(file_path, 'r') as file:
        return [list(line.strip()) for line in file.readlines()]

def find_xmas(grid):
    def match(matrix, pattern, width):
        matches = 0
        for i in range(len(matrix) - width + 1):
            for j in range(len(matrix[i]) - width + 1):
                block = "".join(matrix[i + d][j:j + width] for d in range(width))
                matches += bool(re.match(pattern, block))
        return matches

    # Convert grid to list of strings
    matrix = ["".join(row) for row in grid]
    count = 0
    
    # Check all 4 rotations
    for rotation in range(4):
        # Count horizontal XMAS
        count += sum(row.count("XMAS") for row in matrix)
        # Count diagonal XMAS
        count += match(matrix, r"X.{4}M.{4}A.{4}S", 4)
        # Rotate the grid
        matrix = ["".join(row[::-1]) for row in zip(*matrix)]
    
    return count

def find_x_mas(grid):
    def match(matrix, pattern, width):
        matches = 0
        for i in range(len(matrix) - width + 1):
            for j in range(len(matrix[i]) - width + 1):
                block = "".join(matrix[i + d][j:j + width] for d in range(width))
                matches += bool(re.match(pattern, block))
        return matches

    # Convert grid to list of strings
    matrix = ["".join(row) for row in grid]
    count = 0
    
    # Check all 4 rotations
    for rotation in range(4):
        count += match(matrix, r"M.M.A.S.S", 3)
        # Rotate the grid
        matrix = ["".join(row[::-1]) for row in zip(*matrix)]
    
    return count

def main():
    grid = read_input('Data/4.txt')
    part1_result = find_xmas(grid)
    part2_result = find_x_mas(grid)
    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()
