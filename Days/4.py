import numpy as np

def read_input(file_path):
    with open(file_path, 'r') as file:
        return [list(line.strip()) for line in file.readlines()]

def find_xmas(grid):
    # Function to find all occurrences of "XMAS"
    def search_word(word, x, y, dx, dy):
        for i in range(len(word)):
            if not (0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == word[i]):
                return False
            x += dx
            y += dy
        return True

    directions = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]
    count = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            for dx, dy in directions:
                if search_word("XMAS", x, y, dx, dy):
                    count += 1
    return count

def find_x_mas(grid):
    def check_leg(x, y, dx, dy):
        # Check one leg starting from the center A outward
        if not (0 <= x - dx < len(grid) and 0 <= y - dy < len(grid[0]) and 
                0 <= x + dx < len(grid) and 0 <= y + dy < len(grid[0])):
            return False
            
        chars = [
            grid[x - dx][y - dy],    # First char (M or S)
            grid[x][y],              # Center char (A)
            grid[x + dx][y + dy],    # Last char (S or M)
        ]
        
        # Debug print for almost-matches
        if chars[1] == 'A' and (chars[0] in ['M', 'S']) and (chars[2] in ['M', 'S']):
            print(f"Checking leg at ({x},{y}) dir({dx},{dy}): {''.join(chars)}")
        
        return (chars[0] == 'M' and chars[2] == 'S') or (chars[0] == 'S' and chars[2] == 'M')

    count = 0
    seen = set()  # Track unique patterns

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 'A':  # Start from center A
                # All possible leg combinations
                leg_pairs = [
                    # Diagonal pairs
                    [(1, 1), (-1, -1)],   # Down-right + Up-left
                    [(1, -1), (-1, 1)],   # Down-left + Up-right
                    [(-1, -1), (1, 1)],   # Up-left + Down-right
                    [(-1, 1), (1, -1)],   # Up-right + Down-left
                ]
                
                for d1, d2 in leg_pairs:
                    if check_leg(x, y, d1[0], d1[1]) and \
                       check_leg(x, y, d2[0], d2[1]):
                        pattern_key = tuple(sorted([
                            tuple([x, y, d1[0], d1[1]]), 
                            tuple([x, y, d2[0], d2[1]])
                        ]))
                        if pattern_key not in seen:
                            seen.add(pattern_key)
                            count += 1
                            print(f"Found X-MAS at ({x}, {y})")
                            print(f"  Leg 1: ({d1[0]}, {d1[1]})")
                            print(f"  Leg 2: ({d2[0]}, {d2[1]})")

    print(f"\nTotal unique patterns found: {count}")
    return count

def main():
    grid = read_input('Data/4.txt')
    part1_result = find_xmas(grid)
    part2_result = find_x_mas(grid)
    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()
