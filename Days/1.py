def solve_part1():
    # Read the input file and split into two lists
    with open('Data/1.txt') as f:
        left_nums = []
        right_nums = []
        for line in f:
            left, right = map(int, line.strip().split())
            left_nums.append(left)
            right_nums.append(right)
    
    # Sort both lists
    left_nums.sort()
    right_nums.sort()
    
    # Calculate total distance
    total_distance = sum(abs(l - r) for l, r in zip(left_nums, right_nums))
    
    return total_distance

def solve_part2():
    # Read the input file and split into two lists
    with open('Data/1.txt') as f:
        left_nums = []
        right_nums = []
        for line in f:
            left, right = map(int, line.strip().split())
            left_nums.append(left)
            right_nums.append(right)
    
    # Count occurrences in right list
    right_counts = {}
    for num in right_nums:
        right_counts[num] = right_counts.get(num, 0) + 1
    
    # Calculate similarity score
    total_score = sum(num * right_counts.get(num, 0) for num in left_nums)
    
    return total_score

print(solve_part1())
print(solve_part2())


