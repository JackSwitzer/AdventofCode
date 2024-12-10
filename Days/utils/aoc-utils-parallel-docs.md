# Advent of Code Rust Utilities Documentation - Enhanced Edition

## Table of Contents
1. [Input Parsing](#input-parsing)
2. [Parallel Operations](#parallel-operations)
3. [Grid Operations](#grid-operations)
4. [Regular Expressions](#regular-expressions)
5. [Performance Optimizations](#performance-optimizations)
6. [Common Patterns](#common-patterns)

## Input Parsing

### Regex-Based Parsing
```rust
// Define a pattern with named capture groups
let pattern = r"(?P<x>\d+),(?P<y>\d+) -> (?P<value>\w+)";

// Parse using regex
let parser = Parser::default();
let results: Vec<MyStruct> = parser.parse_with_regex(input, pattern)?;

// Example implementation
#[derive(Debug)]
struct MyStruct {
    x: i32,
    y: i32,
    value: String,
}

impl TryFrom<RegexCapture> for MyStruct {
    type Error = Box<dyn std::error::Error>;

    fn try_from(capture: RegexCapture) -> Result<Self, Self::Error> {
        Ok(MyStruct {
            x: capture.named_groups[0].parse()?,
            y: capture.named_groups[1].parse()?,
            value: capture.named_groups[2].clone(),
        })
    }
}
```

### Parallel Parsing
```rust
// Parse lines in parallel
let numbers: Vec<i32> = parser.parallel_parse_lines(input, |line| {
    line.parse().ok()
});
```

## Parallel Operations

### Grid Parallel Operations
```rust
// Find all matching positions in parallel
let positions = grid.par_find_all(|&value| value == '#');

// Transform grid in parallel
grid.par_transform(|&value| value * 2);

// Count matching elements in parallel
let count = grid.par_count(|&value| value > 0);
```

### Parallel Search
```rust
// Parallel BFS from multiple starting points
let starts = vec![start1, start2, start3];
let visited = search::par_bfs(starts, |pos| {
    // Return neighbors
    grid.neighbors(pos.0, pos.1)
});
```

### Parallel Computation
```rust
// Process data in parallel chunks
let results = compute::parallel_chunks(&data, 1000, |chunk| {
    // Process each chunk
    chunk.iter().sum::<i32>()
});

// Parallel window search
let matches = compute::parallel_window_search(&data, 3, |window| {
    // Check condition on window
    window.iter().sum::<i32>() > 100
});
```

## Performance Considerations

### Parallel Processing Guidelines
1. **Choose Chunk Size Carefully**
```rust
// For small data sets, parallel overhead might not be worth it
let chunk_size = if data.len() < 1000 {
    data.len()
} else {
    data.len() / rayon::current_num_threads()
};
```

2. **Avoid Excessive Synchronization**
```rust
// Bad: Too much synchronization
let sum: i32 = data.par_iter()
    .map(|&x| x)
    .reduce(|| 0, |a, b| a + b);

// Better: Local processing first
let sum: i32 = data.par_chunks(1000)
    .map(|chunk| chunk.iter().sum::<i32>())
    .sum();
```

3. **Use ParallelIterator Methods**
```rust
// Efficient parallel operations
let result: Vec<_> = data.par_iter()
    .filter(|&&x| x > 0)
    .map(|&x| x * 2)
    .collect();
```

## Common Parallel Patterns

### Pattern 1: Map-Reduce
```rust
pub fn parallel_map_reduce<T, R, M, R1>(
    data: &[T],
    map_op: M,
    reduce_op: R1,
) -> R
where
    T: Send + Sync,
    R: Send + Default,
    M: Fn(&T) -> R + Send + Sync,
    R1: Fn(R, R) -> R + Send + Sync,
{
    data.par_iter()
        .map(map_op)
        .reduce(R::default, reduce_op)
}
```

### Pattern 2: Parallel Grid Processing
```rust
pub fn process_grid_regions<T, F>(
    grid: &mut Grid<T>,
    region_size: usize,
    f: F,
)
where
    T: Send + Sync,
    F: Fn(&mut [&mut [T]]) + Send + Sync,
{
    let regions = grid.par_chunks_mut(region_size)
        .map(|chunk| {
            // Process region
            f(chunk);
        });
}
```

## Testing Parallel Code

### Unit Tests
```rust
#[test]
fn test_parallel_operations() {
    let data = vec![1, 2, 3, 4, 5];
    
    // Test parallel sum
    let sum = data.par_iter().sum::<i32>();
    assert_eq!(sum, 15);
    
    // Test parallel transformation
    let doubled: Vec<_> = data.par_iter()
        .map(|&x| x * 2)
        .collect();
    assert_eq!(doubled, vec![2, 4, 6, 8, 10]);
}
```

### Benchmarking
```rust
#[cfg(test)]
mod benches {
    use test::Bencher;

    #[bench]
    fn bench_parallel_vs_sequential(b: &mut Bencher) {
        let data = vec![1; 1_000_000];
        
        b.iter(|| {
            // Parallel version
            let par_sum = data.par_iter().sum::<i32>();
            
            // Sequential version
            let seq_sum = data.iter().sum::<i32>();
            
            assert_eq!(par_sum, seq_sum);
        });
    }
}
```

## Best Practices

1. **Data Size Considerations**
   - Use parallel operations for large data sets
   - Fall back to sequential for small data
   - Consider overhead of parallelization

2. **Thread Pool Management**
   - Use rayon's thread pool effectively
   - Avoid nested parallel operations when possible
   - Consider custom thread pool configuration

3. **Memory Usage**
   - Be aware of memory pressure with parallel operations
   - Use appropriate chunk sizes
   - Consider memory locality

4. **Error Handling**
   - Handle errors appropriately in parallel operations
   - Use Result combinators effectively
   - Consider early termination strategies

Remember to:
- Profile before parallelizing
- Test both small and large inputs
- Consider the overhead of parallelization
- Use appropriate data structures for parallel operations
- Handle errors gracefully in parallel contexts
