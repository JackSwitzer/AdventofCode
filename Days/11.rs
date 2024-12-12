use std::fs;
use std::collections::VecDeque;

type Stone = u64;
type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

// Pre-allocate vectors and minimize string operations
fn transform_stone(stone: Stone, output: &mut VecDeque<Stone>) {
    if stone == 0 {
        output.push_back(1);
        return;
    }
    
    // Count digits without string conversion
    let mut n = stone;
    let mut digit_count = 0;
    while n > 0 {
        digit_count += 1;
        n /= 10;
    }
    
    if digit_count % 2 == 0 && digit_count > 0 {
        // Split number mathematically instead of string operations
        let divisor = 10_u64.pow((digit_count / 2) as u32);
        let right = stone % divisor;
        let left = stone / divisor;
        output.push_back(left);
        output.push_back(right);
    } else {
        output.push_back(stone * 2024);
    }
}

fn process_stones(input: &str) -> Result<()> {
    // Parse initial stones into deque
    let mut current: VecDeque<Stone> = input
        .split_whitespace()
        .map(|s| s.parse().unwrap())
        .collect();
    
    // Start with minimal allocation
    let mut next = VecDeque::new();
    
    // Single evolution loop with prints at checkpoints
    for step in 0..=75 {
        // Print at checkpoints
        if step == 25 {
            println!("Part 1: {}", current.len());
        } else if step == 75 {
            println!("Part 2: {}", current.len());
            break;
        }
        
        // Transform stones using minimal allocation strategy
        for &stone in &current {
            transform_stone(stone, &mut next);
        }
        
        // Swap buffers for next iteration
        current = std::mem::take(&mut next);
    }
    
    Ok(())
}

fn main() -> Result<()> {
    let input = fs::read_to_string("Data/11.txt")?;
    process_stones(&input)?;
    Ok(())
} 