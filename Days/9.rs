use std::error::Error;
use std::fs;
use regex::Regex;

type Result<T> = std::result::Result<T, Box<dyn Error>>;

#[derive(Debug)]
struct FileBlock {
    id: usize,
}

#[derive(Debug)]
struct DiskState {
    blocks: Vec<Option<FileBlock>>, // None represents free space
}

impl DiskState {
    fn new(input: &str) -> Result<Self> {
        let pattern = r"(\d)(\d)?";
        let re = Regex::new(pattern)?;
        let mut blocks = Vec::new();
        let mut file_id = 0;

        for cap in re.captures_iter(input) {
            let file_size = cap[1].parse::<usize>()?;
            let space_size = cap.get(2).map_or(0, |m| m.as_str().parse::<usize>().unwrap_or(0));

            // Add file blocks
            for _ in 0..file_size {
                blocks.push(Some(FileBlock { id: file_id }));
            }
            file_id += 1;

            // Add free space
            for _ in 0..space_size {
                blocks.push(None);
            }
        }

        Ok(Self { blocks })
    }
    
    fn compact(&mut self) {
        let mut target = 0;
        
        for i in 0..self.blocks.len() {
            if let Some(file_block) = self.blocks[i].take() {
                self.blocks[target] = Some(file_block);
                target += 1;
            }
        }
        
        // Fill the rest with None (free space)
        for i in target..self.blocks.len() {
            self.blocks[i] = None;
        }
    }
    
    fn checksum(&self) -> usize {
        self.blocks.iter()
            .enumerate()
            .filter_map(|(pos, block)| {
                block.as_ref().map(|file| pos * file.id)
            })
            .sum()
    }
}

pub fn solve(input: &str) -> Result<(String, String)> {
    let mut disk = DiskState::new(input)?;
    disk.compact();
    let checksum = disk.checksum();
    
    Ok((checksum.to_string(), "N/A".to_string()))
}

fn main() -> Result<()> {
    let input = fs::read_to_string("Data/9.txt")?;
    let (checksum, _) = solve(&input)?;
    println!("Checksum: {}", checksum);
    Ok(())
}
