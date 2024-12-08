use rayon::prelude::*;
use regex::Regex;
use std::collections::{HashMap, HashSet, VecDeque};
use std::str::FromStr;
use std::sync::Mutex;
use num_cpus;

/// parsing.rs - Enhanced parsing utilities with regex support
pub mod parsing {
    use super::*;

    pub struct Parser {
        number_delimiter: String,
        section_delimiter: String,
        trim_whitespace: bool,
    }

    #[derive(Debug)]
    pub struct RegexCapture {
        pub pattern: String,
        pub named_groups: Vec<String>,
    }

    impl Parser {
        // Previous Parser implementation...

        pub fn parse_with_regex<T>(&self, input: &str, pattern: &str) -> Result<Vec<T>, Box<dyn std::error::Error>>
        where
            T: TryFrom<RegexCapture>,
            <T as TryFrom<RegexCapture>>::Error: std::error::Error + 'static,
        {
            let re = Regex::new(pattern)?;
            let captures = re.captures_iter(input)
                .map(|cap| {
                    let named_groups = re.capture_names()
                        .flatten()
                        .filter_map(|name| cap.name(name).map(|m| m.as_str().to_string()))
                        .collect();
                    
                    RegexCapture {
                        pattern: cap[0].to_string(),
                        named_groups,
                    }
                })
                .collect::<Vec<_>>();

            captures.into_iter()
                .map(T::try_from)
                .collect::<Result<Vec<_>, _>>()
                .map_err(Box::from)
        }

        pub fn parallel_parse_lines<T, F>(&self, input: &str, f: F) -> Vec<T>
        where
            T: Send,
            F: Fn(&str) -> Option<T> + Send + Sync,
        {
            input.par_lines()
                .filter_map(f)
                .collect()
        }
    }
}

/// grid.rs - Enhanced grid with parallel operations
pub mod grid {
    use super::*;

    impl<T: Clone + Send + Sync> Grid<T> {
        pub fn par_find_all<P>(&self, predicate: P) -> Vec<(i32, i32)>
        where
            P: Fn(&T) -> bool + Send + Sync,
        {
            (0..self.height).into_par_iter()
                .flat_map(|y| {
                    (0..self.width).into_par_iter()
                        .filter_map(move |x| {
                            if predicate(&self.data[y][x]) {
                                Some((x as i32, y as i32))
                            } else {
                                None
                            }
                        })
                })
                .collect()
        }

        pub fn par_transform<F>(&mut self, f: F)
        where
            F: Fn(&T) -> T + Send + Sync,
            T: Send,
        {
            self.data.par_iter_mut()
                .for_each(|row| {
                    row.par_iter_mut()
                        .for_each(|cell| {
                            *cell = f(cell);
                        });
                });
        }

        pub fn par_count<P>(&self, predicate: P) -> usize
        where
            P: Fn(&T) -> bool + Send + Sync,
        {
            self.data.par_iter()
                .map(|row| {
                    row.par_iter()
                        .filter(|cell| predicate(cell))
                        .count()
                })
                .sum()
        }
    }
}

/// search.rs - Parallel search algorithms
pub mod search {
    use super::*;

    pub fn par_bfs<T, F, I>(
        starts: Vec<T>,
        neighbors: F,
    ) -> HashSet<T>
    where
        T: Clone + Eq + std::hash::Hash + Send + Sync,
        F: Fn(&T) -> I + Send + Sync,
        I: IntoIterator<Item = T>,
    {
        let mut visited: HashSet<T> = HashSet::new();
        let mut frontier: Vec<T> = starts;
        
        while !frontier.is_empty() {
            visited.extend(frontier.iter().cloned());
            
            frontier = frontier.into_par_iter()
                .flat_map(|node| {
                    neighbors(&node)
                        .into_iter()
                        .filter(|n| !visited.contains(n))
                        .collect::<Vec<_>>()
                })
                .collect();
        }
        
        visited
    }
}

/// compute.rs - Enhanced computation utilities
pub mod compute {
    use super::*;

    pub fn optimal_chunk_size<T>(data_len: usize) -> usize {
        let cpu_count = num_cpus::get();
        let cache_line_size = 64; // Common cache line size
        let type_size = std::mem::size_of::<T>();
        
        // Calculate optimal chunk size based on CPU cache and core count
        let items_per_cache_line = cache_line_size / type_size;
        let base_chunk_size = (data_len / cpu_count).max(items_per_cache_line);
        
        // Round up to nearest cache line
        (base_chunk_size + items_per_cache_line - 1) / items_per_cache_line * items_per_cache_line
    }
}

/// geometry.rs - Enhanced geometric utilities
pub mod geometry {
    use super::*;
    
    #[derive(Clone, Copy, Hash, Eq, PartialEq)]
    pub struct Point64 {
        pub x: i64,
        pub y: i64,
    }

    impl Point64 {
        pub fn new(x: i64, y: i64) -> Self {
            Self { x, y }
        }
        
        pub fn manhattan_distance(&self, other: &Self) -> i64 {
            (self.x.abs_diff(other.x) + self.y.abs_diff(other.y)) as i64
        }
        
        pub fn euclidean_distance_squared(&self, other: &Self) -> i64 {
            let dx = self.x - other.x;
            let dy = self.y - other.y;
            dx * dx + dy * dy
        }
        
        pub fn direction_to(&self, other: &Self) -> (i64, i64) {
            let dx = other.x - self.x;
            let dy = other.y - self.y;
            let gcd = gcd(dx.abs(), dy.abs()).max(1);
            (dx / gcd, dy / gcd)
        }
        
        pub fn is_collinear_with(&self, p2: &Self, p3: &Self) -> bool {
            let area = (p2.x - self.x) * (p3.y - self.y) - 
                      (p3.x - self.x) * (p2.y - self.y);
            area == 0
        }
        
        pub fn is_between(&self, p1: &Self, p2: &Self) -> bool {
            if !self.is_collinear_with(p1, p2) {
                return false;
            }
            
            let dx = p2.x - p1.x;
            let dy = p2.y - p1.y;
            
            if dx != 0 {
                (p1.x <= self.x && self.x <= p2.x) || 
                (p2.x <= self.x && self.x <= p1.x)
            } else {
                (p1.y <= self.y && self.y <= p2.y) || 
                (p2.y <= self.y && self.y <= p1.y)
            }
        }
    }

    pub struct LineIterator {
        current: Point64,
        end: Point64,
        step: (i64, i64),
        finished: bool,
    }

    impl Iterator for LineIterator {
        type Item = Point64;

        fn next(&mut self) -> Option<Self::Item> {
            if self.finished {
                return None;
            }
            
            let current = self.current;
            if current == self.end {
                self.finished = true;
            } else {
                self.current = Point64::new(
                    self.current.x + self.step.0,
                    self.current.y + self.step.1
                );
            }
            
            Some(current)
        }
    }

    pub fn line_points(start: Point64, end: Point64) -> LineIterator {
        let step = start.direction_to(&end);
        LineIterator {
            current: start,
            end,
            step,
            finished: false,
        }
    }

    fn gcd(a: i64, b: i64) -> i64 {
        if b == 0 { a } else { gcd(b, a % b) }
    }

    pub struct GeometryProcessor {
        points: Vec<Point64>,
        batch_size: usize,
    }

    impl GeometryProcessor {
        pub fn new(points: Vec<Point64>) -> Self {
            Self {
                points,
                batch_size: optimal_chunk_size::<Point64>(points.len()),
            }
        }

        pub fn process_point_pairs<F, T>(&self, f: F) -> HashSet<T>
        where
            F: Fn(Point64, Point64) -> Vec<T> + Send + Sync,
            T: Send + Sync + Eq + Hash + Clone,
        {
            let results = Mutex::new(HashSet::new());
            
            self.points.par_chunks(self.batch_size).for_each(|chunk| {
                let mut local_results = HashSet::new();
                for (i, &p1) in chunk.iter().enumerate() {
                    for &p2 in chunk[i+1..].iter() {
                        local_results.extend(f(p1, p2));
                    }
                }
                results.lock().unwrap().extend(local_results);
            });

            results.into_inner().unwrap()
        }

        pub fn find_collinear_points(&self) -> HashSet<Point64> {
            let mut results = HashSet::new();
            
            for (i, &p1) in self.points.iter().enumerate() {
                for (j, &p2) in self.points[i+1..].iter().enumerate() {
                    for &p3 in self.points[i+j+2..].iter() {
                        if p1.is_collinear_with(&p2, &p3) {
                            results.insert(p1);
                            results.insert(p2);
                            results.insert(p3);
                        }
                    }
                }
            }
            
            results
        }
    }
}
