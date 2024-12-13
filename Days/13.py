# Import the necessary classes and functions
from collections import defaultdict

class FencePosition:
    Up = 0
    Down = 1
    Left = 2
    Right = 3

class Fences:
    def __init__(self, merge_fences):
        # horizontal: keyed by (position, i), stores list of (j_start, j_end)
        # vertical: keyed by (position, j), stores list of (i_start, i_end)
        self.horizontal = defaultdict(list)
        self.vertical = defaultdict(list)
        self.merge_fences = merge_fences

    def clear(self):
        self.horizontal.clear()
        self.vertical.clear()

    def add_horizontal(self, position, i, j):
        fences = self.horizontal[(position, i)]
        if self.merge_fences:
            # Try to merge contiguous segments
            p_left = None
            p_right = None
            for idx, (start, end) in enumerate(fences):
                if end == j:
                    p_left = idx
                if start == j + 1:
                    p_right = idx
            if p_left is not None and p_right is not None:
                # Merge two segments
                start, _ = fences[p_left]
                _, end = fences[p_right]
                fences[p_left] = (start, end)
                del fences[p_right]
            elif p_left is not None:
                # Extend left segment
                start, _ = fences[p_left]
                fences[p_left] = (start, j + 1)
            elif p_right is not None:
                # Extend right segment
                _, end = fences[p_right]
                fences[p_right] = (j, end)
            else:
                fences.append((j, j + 1))
        else:
            fences.append((j, j + 1))

    def add_vertical(self, position, i, j):
        fences = self.vertical[(position, j)]
        if self.merge_fences:
            p_above = None
            p_below = None
            for idx, (start, end) in enumerate(fences):
                if end == i:
                    p_above = idx
                if start == i + 1:
                    p_below = idx
            if p_above is not None and p_below is not None:
                # Merge
                start, _ = fences[p_above]
                _, end = fences[p_below]
                fences[p_above] = (start, end)
                del fences[p_below]
            elif p_above is not None:
                start, _ = fences[p_above]
                fences[p_above] = (start, i + 1)
            elif p_below is not None:
                _, end = fences[p_below]
                fences[p_below] = (i, end)
            else:
                fences.append((i, i + 1))
        else:
            fences.append((i, i + 1))

    def add(self, position, i, j):
        if position == FencePosition.Up:
            self.add_horizontal(position, i, j)
        elif position == FencePosition.Down:
            self.add_horizontal(position, i + 1, j)
        elif position == FencePosition.Left:
            self.add_vertical(position, i, j)
        elif position == FencePosition.Right:
            self.add_vertical(position, i, j + 1)

    def count(self):
        # Just count the number of segments stored
        hcount = sum(len(f) for f in self.horizontal.values())
        vcount = sum(len(f) for f in self.vertical.values())
        return hcount + vcount

def read_garden(filename):
    garden = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                garden.append(list(line))
    return garden

def total_price(garden, merge_fences):
    nrows = len(garden)
    ncols = len(garden[0]) if nrows > 0 else 0
    visited = [[False]*ncols for _ in range(nrows)]
    to_visit = []
    fences = Fences(merge_fences)

    price = 0
    for j in range(ncols):
        for i in range(nrows):
            if visited[i][j]:
                continue
            region = garden[i][j]
            fences.clear()
            to_visit.clear()
            to_visit.append((i, j))
            area = 0
            while to_visit:
                ci, cj = to_visit.pop()
                if visited[ci][cj]:
                    continue
                visited[ci][cj] = True
                area += 1
                neighbors = [
                    (FencePosition.Up, ci-1, cj),
                    (FencePosition.Down, ci+1, cj),
                    (FencePosition.Left, ci, cj-1),
                    (FencePosition.Right, ci, cj+1),
                ]
                for pos, ni, nj in neighbors:
                    if ni < 0 or nj < 0 or ni >= nrows or nj >= ncols or garden[ni][nj] != region:
                        # fence boundary
                        fences.add(pos, ci, cj)
                    else:
                        if not visited[ni][nj]:
                            to_visit.append((ni, nj))
            price += area * fences.count()
    return price

# Read the garden from the uploaded 12.txt file
file_path = "/mnt/data/12.txt"
garden = read_garden(file_path)

# Part 1: No bulk discount
part1_answer = total_price(garden, merge_fences=False)

# Part 2: With bulk discount
part2_answer = total_price(garden, merge_fences=True)

part1_answer, part2_answer
