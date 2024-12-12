from PY_utils import Parser, GridProcessor
import numpy as np
from typing import Tuple, Set

def solve(input_text: str) -> Tuple[str, str]:
    # Parse input using new Parser class
    parser = Parser()
    grid = parser.parse_grid(input_text, as_type=str)
    
    # Create grid processor for finding regions
    grid_proc = GridProcessor(grid)
    
    # Find all regions using the grid processor
    regions = []
    visited = set()
    
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if (y, x) not in visited and grid[y, x] != '.':
                plant_type = grid[y, x]
                region = grid_proc.find_regions(
                    condition=lambda val: val == plant_type,
                    diagonal=False,
                    min_size=1
                )[0]  # Take first region found
                regions.append((plant_type, region))
                visited.update(region)

    # Calculate prices for both parts
    total_price1 = 0
    total_price2 = 0
    
    for plant_type, region in regions:
        area = len(region)
        perimeter = calculate_perimeter(grid, region)
        sides = calculate_sides(grid, region)
        
        total_price1 += area * perimeter
        total_price2 += area * sides
    
    return str(total_price1), str(total_price2)

def calculate_perimeter(grid: np.ndarray, region: Set[Tuple[int, int]]) -> int:
    """Calculate perimeter of a region"""
    perimeter = 0
    height, width = grid.shape
    
    for y, x in region:
        # Check all four sides
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = y + dy, x + dx
            # Count edge if out of bounds or different region
            if (ny < 0 or ny >= height or 
                nx < 0 or nx >= width or 
                (ny, nx) not in region):
                perimeter += 1
                
    return perimeter

def calculate_sides(grid: np.ndarray, region: Set[Tuple[int, int]]) -> int:
    """
    Calculate number of sides according to Part 2 rules:
    1. Each straight section counts as ONE side
    2. Inner holes add their complete perimeter as sides
    3. Diagonal connections don't join sides
    4. Each indent creates new sides
    """
    if len(region) == 1:
        return 4

    # Create binary grid for this region
    min_y = min(y for y, x in region)
    max_y = max(y for y, x in region)
    min_x = min(x for y, x in region)
    max_x = max(x for y, x in region)
    height = max_y - min_y + 3
    width = max_x - min_x + 3
    binary_grid = np.zeros((height, width), dtype=bool)
    
    # Fill region
    for y, x in region:
        binary_grid[y - min_y + 1, x - min_x + 1] = True

    # Count sides by following the boundary
    sides = 0
    visited_edges = set()
    
    def trace_boundary(y: int, x: int, coming_from: str) -> None:
        nonlocal sides
        start = (y, x)
        direction = coming_from
        
        while True:
            # Check all four directions: right, down, left, up
            directions = [
                ((y, x+1), "right", "left"),
                ((y+1, x), "down", "up"),
                ((y, x-1), "left", "right"),
                ((y-1, x), "up", "down")
            ]
            
            found_next = False
            for (ny, nx), next_dir, from_dir in directions:
                # Skip if we just came from this direction
                if direction == next_dir:
                    continue
                
                # Check if this is a valid cell in our region
                if (0 <= ny < height and 
                    0 <= nx < width and 
                    binary_grid[ny, nx]):
                    
                    # If we're changing direction, we've found a new side
                    edge = (min(y, ny), min(x, nx), 
                           max(y, ny), max(x, nx))
                    if edge not in visited_edges:
                        visited_edges.add(edge)
                        sides += 1
                    
                    # Move to next cell
                    y, x = ny, nx
                    direction = from_dir
                    found_next = True
                    break
            
            if not found_next or (y, x) == start:
                break

    # Start tracing from leftmost point of topmost row
    for y in range(height):
        for x in range(width):
            if binary_grid[y, x]:
                trace_boundary(y, x, "left")
                return sides

    return sides

def test_solution():
    """Test all cases from the problem description"""
    test_cases = [
        ("Original Example", """
AAAA
BBCD
BBCC
EEEC
""".strip(), "80"),
        
        ("O and X Example", """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
""".strip(), "436"),
        
        ("E Shape", """
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
""".strip(), "236"),
        
        ("A with holes", """
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
""".strip(), "368")
    ]
    
    for name, input_text, expected_part2 in test_cases:
        print(f"\nTesting {name}:")
        _, part2 = solve(input_text)
        assert part2 == expected_part2, f"Expected {expected_part2}, got {part2}"
        print(f"✓ Passed: {part2}")

if __name__ == "__main__":
    #test_solution()
    
    # Solve actual input
    parser = Parser()
    input_text = parser.load_file(12)
    part1, part2 = solve(input_text)
    print(f"\nPart 1: {part1}")
    print(f"Part 2: {part2}")
