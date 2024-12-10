def read_map(filename):
    with open(filename) as f:
        return [list(map(int, line.strip())) for line in f]

def get_neighbors(x, y, height, width):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    neighbors = []
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < height and 0 <= new_y < width:
            neighbors.append((new_x, new_y))
    return neighbors

def count_reachable_nines(topo_map, start_x, start_y):
    height = len(topo_map)
    width = len(topo_map[0])
    visited = set()
    reachable_nines = set()
    
    def dfs(x, y, current_height):
        if topo_map[x][y] == 9:
            reachable_nines.add((x, y))
            return
        
        visited.add((x, y))
        for nx, ny in get_neighbors(x, y, height, width):
            if (nx, ny) not in visited and topo_map[nx][ny] == current_height + 1:
                dfs(nx, ny, current_height + 1)
        visited.remove((x, y))
    
    dfs(start_x, start_y, 0)
    return len(reachable_nines)

def count_distinct_paths(topo_map, start_x, start_y):
    height = len(topo_map)
    width = len(topo_map[0])
    visited = set()
    path_count = 0
    
    def dfs(x, y, current_height):
        nonlocal path_count
        if topo_map[x][y] == 9:
            path_count += 1
            return
        
        visited.add((x, y))
        for nx, ny in get_neighbors(x, y, height, width):
            if (nx, ny) not in visited and topo_map[nx][ny] == current_height + 1:
                dfs(nx, ny, current_height + 1)
        visited.remove((x, y))
    
    dfs(start_x, start_y, 0)
    return path_count

def solve(filename):
    topo_map = read_map(filename)
    height = len(topo_map)
    width = len(topo_map[0])
    total_score_part1 = 0
    total_score_part2 = 0
    
    # Find all trailheads (positions with height 0)
    for x in range(height):
        for y in range(width):
            if topo_map[x][y] == 0:
                score1 = count_reachable_nines(topo_map, x, y)
                score2 = count_distinct_paths(topo_map, x, y)
                total_score_part1 += score1
                total_score_part2 += score2
    
    return total_score_part1, total_score_part2

if __name__ == "__main__":
    part1, part2 = solve("Data/10.txt")
    print(f"Part 1 - The sum of all trailhead scores is: {part1}")
    print(f"Part 2 - The sum of all trailhead ratings is: {part2}")
