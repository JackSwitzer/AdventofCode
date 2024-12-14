import re
from itertools import count

def parse_input(puzzle_input):
    """Parse the input data, filtering out invalid or blank lines."""
    return [
        [int(x) for x in re.findall(r'(-?\d+)', line)]
        for line in puzzle_input.split('\n') if line.strip()
    ]

def load_robots(filename):
    """
    Load the robot positions and velocities from the given file.
    Each line is of the form: p=x,y v=dx,dy
    Returns a list of (x, y, dx, dy).
    """
    robots = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Example line: p=0,4 v=3,-3
            # We'll parse it out:
            parts = line.split()
            # parts[0] should be like p=0,4
            # parts[1] should be like v=3,-3
            pos_str = parts[0][2:]  # remove 'p='
            vel_str = parts[1][2:]  # remove 'v='
            x_str, y_str = pos_str.split(',')
            dx_str, dy_str = vel_str.split(',')
            x, y = int(x_str), int(y_str)
            dx, dy = int(dx_str), int(dy_str)
            robots.append((x, y, dx, dy))
    return robots

def step_robots(robots, width, height, steps=1):
    """
    Advance the robots by 'steps' time units.
    The field wraps at width (x-direction) and height (y-direction).
    robots is a list of tuples (x, y, dx, dy).
    Returns a new list of updated robot positions/velocities.
    """
    new_robots = []
    for (x, y, dx, dy) in robots:
        # Move forward steps times:
        # (x + steps*dx) mod width, (y + steps*dy) mod height
        x_new = (x + steps*dx) % width
        y_new = (y + steps*dy) % height
        new_robots.append((x_new, y_new, dx, dy))
    return new_robots

def count_quadrants(robots, width, height):
    """
    Count how many robots fall into each of the four quadrants after dividing the space exactly in half:
    The space is width by height.
    The vertical dividing line is at x = width//2
    The horizontal dividing line is at y = height//2
    Robots exactly on these dividing lines do not count towards any quadrant.
    
    Quadrants (if we view top-left as (0,0)):
    
        Q2 | Q1
       ------------
        Q3 | Q4
    
    Return (count_Q1, count_Q2, count_Q3, count_Q4).
    """
    mid_x = width // 2
    mid_y = height // 2

    Q1 = Q2 = Q3 = Q4 = 0
    for (x, y, dx, dy) in robots:
        if x == mid_x or y == mid_y:
            # On a dividing line, ignore
            continue
        if x > mid_x and y < mid_y:
            Q1 += 1
        elif x < mid_x and y < mid_y:
            Q2 += 1
        elif x < mid_x and y > mid_y:
            Q3 += 1
        elif x > mid_x and y > mid_y:
            Q4 += 1
    return (Q1, Q2, Q3, Q4)

def bounding_box_area(robots):
    """
    Compute the bounding box area of all robot positions (ignoring wrap-around for this calculation).
    This helps detect when they form a pattern (usually a minimal bounding box).
    """
    xs = [r[0] for r in robots]
    ys = [r[1] for r in robots]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    width = (max_x - min_x + 1)
    height = (max_y - min_y + 1)
    return width * height, min_x, max_x, min_y, max_y

def find_easter_egg_time(original_robots, width, height, max_search=200000):
    """
    Find the earliest time where robots form the "Easter egg" pattern.
    We assume this corresponds to when the bounding box of the points is minimal.
    
    We'll simulate forward and track the bounding box area.
    Once we find a minimal area that then starts to increase, we consider that the minimal point in time.
    """
    robots = [r for r in original_robots]  # copy
    best_time = 0
    best_area = None

    # We'll try a simple hill-climbing approach:
    # Move forward in time, track area. Once area starts increasing after a minimum, stop.
    # For safety, we impose a max_search limit.
    
    # Initialize
    current_area, _, _, _, _ = bounding_box_area(robots)
    best_area = current_area
    best_time = 0

    increasing_streak = 0
    time = 0

    while time < max_search:
        time += 1
        robots = step_robots(robots, width, height, steps=1)
        current_area, _, _, _, _ = bounding_box_area(robots)
        if current_area < best_area:
            best_area = current_area
            best_time = time
            increasing_streak = 0
        else:
            increasing_streak += 1
            # If area keeps increasing for a while after a minimum, we can guess we've passed the pattern.
            # One increment might not be conclusive, but let's break if we see a consistent increase.
            if increasing_streak > 5:  # arbitrary buffer
                break

    return best_time

def main():
    # Parameters from the puzzle statement:
    WIDTH = 101
    HEIGHT = 103
    
    robots = load_robots("/mnt/data/14.txt")

    # Part 1:
    # After exactly 100 seconds:
    after_100 = step_robots(robots, WIDTH, HEIGHT, steps=100)
    Q1, Q2, Q3, Q4 = count_quadrants(after_100, WIDTH, HEIGHT)
    safety_factor = Q1 * Q2 * Q3 * Q4
    print("Part 1 Safety Factor:", safety_factor)

    # Part 2:
    # Find the earliest time where the Easter egg pattern emerges:
    # We'll attempt the bounding box minimal area approach.
    easter_egg_time = find_easter_egg_time(robots, WIDTH, HEIGHT)
    print("Part 2 Earliest Easter Egg Time:", easter_egg_time)

if __name__ == "__main__":
    main()
