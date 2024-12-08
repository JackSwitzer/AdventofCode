mod utils {
    pub mod geometry {
        #[derive(Clone, Copy, Hash, Eq, PartialEq)]
        pub struct Point64 {
            pub x: i64,
            pub y: i64,
        }

        impl Point64 {
            pub fn new(x: i64, y: i64) -> Self {
                Self { x, y }
            }
            
            pub fn direction_to(&self, other: &Self) -> (i64, i64) {
                let dx = other.x - self.x;
                let dy = other.y - self.y;
                let gcd = gcd(dx.abs(), dy.abs()).max(1);
                (dx / gcd, dy / gcd)
            }
        }

        fn gcd(a: i64, b: i64) -> i64 {
            if b == 0 { a } else { gcd(b, a % b) }
        }

        pub struct GeometryProcessor {
            points: Vec<Point64>,
        }

        impl GeometryProcessor {
            pub fn new(points: Vec<Point64>) -> Self {
                Self { points }
            }

            pub fn process_point_pairs<F, T>(&self, f: F) -> Vec<T>
            where
                F: Fn(Point64, Point64) -> Vec<T>,
            {
                let mut results = Vec::new();
                for (i, &p1) in self.points.iter().enumerate() {
                    for &p2 in self.points[i+1..].iter() {
                        results.extend(f(p1, p2));
                    }
                }
                results
            }
        }
    }
}

use std::collections::{HashMap, HashSet};
use std::error::Error;
use utils::geometry::{Point64, GeometryProcessor};

type Result<T> = std::result::Result<T, Box<dyn Error>>;

fn parse_input(input: &str) -> Result<HashMap<char, Vec<Point64>>> {
    let mut antennas: HashMap<char, Vec<Point64>> = HashMap::new();
    
    for (y, line) in input.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c != '.' {
                antennas.entry(c)
                    .or_default()
                    .push(Point64::new(x as i64, y as i64));
            }
        }
    }
    
    Ok(antennas)
}

fn solve_part1(antennas: &HashMap<char, Vec<Point64>>) -> Result<usize> {
    let mut antinodes = HashSet::new();
    
    for (_, points) in antennas {
        let processor = GeometryProcessor::new(points.clone());
        
        let new_antinodes = processor.process_point_pairs(|p1, p2| {
            let dx = p2.x - p1.x;
            let dy = p2.y - p1.y;
            
            vec![
                Point64::new(p2.x + dx, p2.y + dy),
                Point64::new(p1.x - dx, p1.y - dy)
            ]
        });
        
        antinodes.extend(new_antinodes);
    }
    
    Ok(antinodes.len())
}

fn solve_part2(antennas: &HashMap<char, Vec<Point64>>) -> Result<usize> {
    let mut antinodes = HashSet::new();
    
    for (_, points) in antennas {
        let processor = GeometryProcessor::new(points.clone());
        
        // First add all antenna points
        antinodes.extend(points.iter().cloned());
        
        // Process all point pairs
        let new_points = processor.process_point_pairs(|p1, p2| {
            let mut points = Vec::new();
            let dir = p1.direction_to(&p2);
            
            // Add all points between p1 and p2
            let mut current = p1;
            while current != p2 {
                points.push(current);
                current = Point64::new(current.x + dir.0, current.y + dir.1);
            }
            points.push(p2);
            
            // Add points beyond
            points.push(Point64::new(p1.x - dir.0, p1.y - dir.1));
            points.push(Point64::new(p2.x + dir.0, p2.y + dir.1));
            
            points
        });
        
        antinodes.extend(new_points);
    }
    
    Ok(antinodes.len())
}

pub fn solve(input: &str) -> Result<(String, String)> {
    let antennas = parse_input(input)?;
    let part1 = solve_part1(&antennas)?;
    let part2 = solve_part2(&antennas)?;
    Ok((part1.to_string(), part2.to_string()))
}

fn main() -> Result<()> {
    let input = std::fs::read_to_string("Data/8.txt")?;
    let (part1, part2) = solve(&input)?;
    println!("Part 1: {}", part1);
    println!("Part 2: {}", part2);
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    
    const EXAMPLE: &str = "\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............";

    #[test]
    fn test_part1() {
        let parsed = parse_input(EXAMPLE).unwrap();
        assert_eq!(solve_part1(&parsed).unwrap(), 14);
    }

    #[test]
    fn test_part2() {
        let parsed = parse_input(EXAMPLE).unwrap();
        assert_eq!(solve_part2(&parsed).unwrap(), 34);
    }
}
