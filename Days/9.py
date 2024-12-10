def parse_disk_map(disk_map):
    return [int(x) for x in disk_map]

def create_initial_state(lengths):
    blocks = []
    file_id = 0
    
    for i, length in enumerate(lengths):
        if i % 2 == 0:  # File block
            blocks.extend([file_id] * length)
            file_id += 1
        else:  # Space
            blocks.extend(['.'] * length)
    return blocks

def find_file_bounds(blocks, file_id):
    # Find start and end positions of a file
    start = -1
    length = 0
    for i, block in enumerate(blocks):
        if block == file_id:
            if start == -1:
                start = i
            length += 1
    return start, length

def find_leftmost_space_for_file(blocks, required_length, file_start):
    # Find leftmost contiguous space that can fit the file
    current_space = 0
    space_start = -1
    
    for i in range(file_start):
        if blocks[i] == '.':
            if space_start == -1:
                space_start = i
            current_space += 1
            if current_space >= required_length:
                return space_start
        else:
            current_space = 0
            space_start = -1
    
    return -1

def compact_disk_v2(blocks, debug=False):
    if debug:
        print(f"Initial state: {blocks_to_string(blocks)}")
    
    # Get highest file ID
    max_file_id = max(block for block in blocks if block != '.')
    
    # Process files in decreasing ID order
    for file_id in range(max_file_id, -1, -1):
        # Find file bounds
        file_start, file_length = find_file_bounds(blocks, file_id)
        
        # Find leftmost suitable space
        target_pos = find_leftmost_space_for_file(blocks, file_length, file_start)
        
        # If space found, move the entire file
        if target_pos != -1:
            # Copy file to new position
            for i in range(file_length):
                blocks[target_pos + i] = file_id
            # Clear old position
            for i in range(file_start, file_start + file_length):
                blocks[i] = '.'
                
            if debug:
                print(f"Moved file {file_id}: {blocks_to_string(blocks)}")

def blocks_to_string(blocks):
    return ''.join(str(x) for x in blocks)

def calculate_checksum(blocks):
    checksum = 0
    for pos, block in enumerate(blocks):
        if block != '.':
            checksum += pos * block
    return checksum

def solve_part2(input_data, debug=False):
    if debug:
        print(f"\nSolving part 2 for input: {input_data}")
    
    lengths = parse_disk_map(input_data.strip())
    blocks = create_initial_state(lengths)
    
    if debug:
        print(f"Initial blocks: {blocks_to_string(blocks)}")
    
    compact_disk_v2(blocks, debug)
    
    checksum = calculate_checksum(blocks)
    if debug:
        print(f"Final blocks: {blocks_to_string(blocks)}")
        print(f"Checksum: {checksum}")
    
    return checksum

def test_examples():
    # Part 2 test
    print("\nTesting Part 2 example:")
    print("Initial: '00...111...2...333.44.5555.6666.777.888899'")
    print("Expected final: '00992111777.44.333....5555.6666.....8888..'")
    result = solve_part2("2333133121414131402", debug=True)
    assert result == 2858, f"Part 2 test failed. Got {result}, expected 2858"
    print("Part 2 test passed!")

if __name__ == "__main__":
    test_examples()
    
    with open("Data/9.txt") as f:
        input_data = f.read()
    result = solve_part2(input_data)
    print(f"\nPart 2 Solution: {result}")
