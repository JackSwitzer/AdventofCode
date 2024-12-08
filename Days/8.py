from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import List, Set, Dict, Tuple


@dataclass(frozen=True)
class Point:
    x: int
    y: int


def read_file(file_path: str) -> str:
    """Read input file using pathlib."""
    return Path(file_path).read_text(encoding="utf-8")


def parse_input(advent_input: str) -> List[List[str]]:
    """Parse input string into a grid of antenna frequencies."""
    return [list(line) for line in advent_input.strip().splitlines()]


def find_antennas(grid: List[List[str]]) -> Dict[str, List[Point]]:
    """Find all antennas and group them by frequency."""
    antennas = defaultdict(list)
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char != '.':
                antennas[char].append(Point(x, y))
    return antennas


def is_collinear(p1: Point, p2: Point, p3: Point) -> bool:
    """Check if three points are collinear."""
    # Using the cross product method
    return (p2.y - p1.y) * (p3.x - p1.x) == (p3.y - p1.y) * (p2.x - p1.x)


def solve_part1(grid: List[List[str]]) -> int:
    """
    Find antinodes where one antenna is twice as far from the antinode
    as the other antenna (of the same frequency).
    """
    height = len(grid)
    width = len(grid[0])
    antennas = find_antennas(grid)
    antinodes = set()

    for frequency, points in antennas.items():
        if len(points) < 2:
            continue
            
        # Check each pair of antennas
        for i, p1 in enumerate(points):
            for p2 in points[i+1:]:
                # Calculate the vector between antennas
                dx = p2.x - p1.x
                dy = p2.y - p1.y
                
                # Calculate the unit vector (direction)
                length = (dx * dx + dy * dy) ** 0.5
                if length == 0:
                    continue
                    
                udx = dx / length
                udy = dy / length
                
                # Try points at various distances along the line
                for dist in range(-max(width, height), max(width, height)):
                    # Try both directions from each antenna
                    for antenna, direction in [(p1, 1), (p2, -1)]:
                        x = int(antenna.x + direction * dist * udx)
                        y = int(antenna.y + direction * dist * udy)
                        
                        if 0 <= x < width and 0 <= y < height:
                            point = Point(x, y)
                            dist1 = (point.x - p1.x) ** 2 + (point.y - p1.y) ** 2
                            dist2 = (point.x - p2.x) ** 2 + (point.y - p2.y) ** 2
                            
                            if dist1 > 0 and dist2 > 0:  # Avoid division by zero
                                ratio = dist1 / dist2
                                if abs(ratio - 2.0) < 0.1 or abs(ratio - 0.5) < 0.1:
                                    antinodes.add(point)

    return len(antinodes)


def solve_part2(grid: List[List[str]]) -> int:
    """
    Find antinodes at any point collinear with two antennas 
    of the same frequency.
    """
    height = len(grid)
    width = len(grid[0])
    antennas = find_antennas(grid)
    antinodes = set()

    for frequency, points in antennas.items():
        if len(points) < 2:
            continue
            
        # Check each pair of antennas
        for i, p1 in enumerate(points):
            for j, p2 in enumerate(points[i+1:], i+1):
                # Check all points in the grid for collinearity
                for y in range(height):
                    for x in range(width):
                        p = Point(x, y)
                        if is_collinear(p1, p2, p):
                            antinodes.add(p)

    return len(antinodes)


def main():
    file_input = read_file("Data/8.txt")
    grid = parse_input(file_input)
    
    print(f"Part 1: {solve_part1(grid)}")
    print(f"Part 2: {solve_part2(grid)}")


if __name__ == "__main__":
    main()