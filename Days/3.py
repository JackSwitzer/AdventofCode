import re

def parse_input():
    with open('Data/3.txt', 'r') as file:
        return file.read().strip()

def solve_part1(data):
    # Find all valid mul(X,Y) patterns where X and Y are 1-3 digits
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    matches = re.finditer(pattern, data)
    
    total = 0
    for match in matches:
        x, y = map(int, match.groups())
        total += x * y
    
    return total

def solve_part2(data):
    # Find all mul instructions and do/don't controls
    mul_pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    control_pattern = r'do\(\)|don\'t\(\)'
    
    # Get all matches with their positions
    mul_matches = [(m.start(), m) for m in re.finditer(mul_pattern, data)]
    control_matches = [(m.start(), m.group()) for m in re.finditer(control_pattern, data)]
    
    # Combine and sort all matches by position
    all_matches = mul_matches + control_matches
    all_matches.sort()
    
    enabled = True
    total = 0
    
    for pos, match in all_matches:
        if isinstance(match, str):  # Control instruction
            enabled = match == 'do()'
        else:  # Multiplication instruction
            if enabled:
                x, y = map(int, match.groups())
                total += x * y
    
    return total

def main():
    data = parse_input()
    print(f"Part 1: {solve_part1(data)}")
    print(f"Part 2: {solve_part2(data)}")

if __name__ == "__main__":
    main()
