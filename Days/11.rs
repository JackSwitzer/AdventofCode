use std::fs;
use std::collections::HashMap;

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

#[derive(Debug, Clone, Copy, Hash, Eq, PartialEq)]
struct Stone {
    value: u64
}

impl Stone {
    fn evolve(&self) -> (Stone, Option<Stone>) {
        if self.value == 0 {
            return (Stone { value: 1 }, None);
        }
        
        let mut n = self.value;
        let mut digit_count = 0;
        while n > 0 {
            digit_count += 1;
            n /= 10;
        }
        
        if digit_count % 2 == 0 && digit_count > 0 {
            let divisor = 10_u64.pow((digit_count / 2) as u32);
            let left = self.value / divisor;
            let right = self.value % divisor;
            (Stone { value: left }, Some(Stone { value: right }))
        } else {
            (Stone { value: self.value * 2024 }, None)
        }
    }
}

fn process_stones(input: &str, steps: usize) -> usize {
    let mut stones: HashMap<Stone, usize> = input
        .split_whitespace()
        .filter_map(|s| s.parse::<u64>().ok())
        .map(|n| (Stone { value: n }, 1))
        .collect();
    
    let mut new_stones = HashMap::new();
    
    for _ in 0..steps {
        for (stone, &count) in &stones {
            let (evolved, maybe_split) = stone.evolve();
            
            *new_stones.entry(evolved).or_insert(0) += count;
            if let Some(split) = maybe_split {
                *new_stones.entry(split).or_insert(0) += count;
            }
        }
        
        std::mem::swap(&mut stones, &mut new_stones);
        new_stones.clear();
    }
    
    stones.values().sum()
}

fn main() -> Result<()> {
    let input = fs::read_to_string("Data/11.txt")?;
    
    println!("Part 1: {}", process_stones(&input, 25));
    println!("Part 2: {}", process_stones(&input, 75));
    
    Ok(())
} 