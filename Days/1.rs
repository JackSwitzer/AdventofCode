use std::error::Error;

type Result<T> = std::result::Result<T, Box<dyn Error>>;

pub fn solve(input: &str) -> Result<(String, String)> {
    let (left, right) = parse_input(input)?;
    
    let part1 = solve_part1(&left, &right)?;
    let part2 = solve_part2(&left, &right)?;
    
    Ok((part1.to_string(), part2.to_string()))
}

fn parse_input(input: &str) -> Result<(Vec<i64>, Vec<i64>)> {
    let mut left = Vec::new();
    let mut right = Vec::new();

    for line in input.lines() {
        if line.trim().is_empty() { continue; }
        
        let mut parts = line.split_whitespace();
        if let (Some(l), Some(r)) = (parts.next(), parts.next()) {
            left.push(l.parse::<i64>()?);
            right.push(r.parse::<i64>()?);
        }
    }

    Ok((left, right))
}

fn solve_part1(left: &[i64], right: &[i64]) -> Result<i64> {
    let mut left_sorted = left.to_vec();
    let mut right_sorted = right.to_vec();
    left_sorted.sort_unstable();
    right_sorted.sort_unstable();

    let total_distance: i64 = left_sorted.iter()
        .zip(right_sorted.iter())
        .map(|(a, b)| (a - b).abs())
        .sum();

    Ok(total_distance)
}

fn solve_part2(left: &[i64], right: &[i64]) -> Result<i64> {
    let similarity_score: i64 = left.iter()
        .map(|&num| {
            let count = right.iter().filter(|&&x| x == num).count() as i64;
            num * count
        })
        .sum();

    Ok(similarity_score)
}

#[cfg(test)]
mod tests {
    use super::*;
    
    const EXAMPLE: &str = r#"3   4
4   3
2   5
1   3
3   9
3   3"#;

    #[test]
    fn test_part1() {
        let (left, right) = parse_input(EXAMPLE).unwrap();
        assert_eq!(solve_part1(&left, &right).unwrap(), 11);
    }

    #[test]
    fn test_part2() {
        let (left, right) = parse_input(EXAMPLE).unwrap();
        assert_eq!(solve_part2(&left, &right).unwrap(), 31);
    }
}
