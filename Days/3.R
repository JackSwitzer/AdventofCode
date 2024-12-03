# Read input file
input <- readLines("Data/3.txt")

# Function for Part 1 - ignores do/don't instructions
process_multiplications_part1 <- function(text) {
  # Pattern for instructions - using the exact specified pattern
  mul_pattern <- "mul\\((\\d{1,3}),(\\d{1,3})\\)"
  
  # Find all multiplication matches
  mul_matches <- gregexpr(mul_pattern, text, perl = TRUE)[[1]]
  
  # If no multiplications found, return empty
  if (mul_matches[1] == -1) return(numeric(0))
  
  # Get all multiplication strings
  mul_strings <- regmatches(text, list(mul_matches))[[1]]
  
  # Process all multiplications
  results <- numeric(0)
  for (mul_str in mul_strings) {
    nums <- as.numeric(unlist(strsplit(gsub("mul\\(|\\)", "", mul_str), ",")))
    result <- nums[1] * nums[2]
    results <- c(results, result)
  }
  
  return(results)
}

# Function for Part 2 - simplified approach
process_multiplications_part2 <- function(text) {
  chars <- strsplit(text, "")[[1]]
  results <- numeric(0)
  enabled <- TRUE
  i <- 1
  
  while (i <= length(chars)) {
    # Check for do() or don't()
    if (i + 3 <= length(chars) && paste0(chars[i:(i+3)], collapse="") == "do()") {
      enabled <- TRUE
      i <- i + 4
      next
    }
    if (i + 5 <= length(chars) && paste0(chars[i:(i+5)], collapse="") == "don't()") {
      enabled <- FALSE
      i <- i + 6
      next
    }
    
    # Look for "mul" anywhere (allowing for prefix characters)
    if (i + 2 <= length(chars) && 
        paste0(chars[i:(i+2)], collapse="") == "mul" || 
        (i > 0 && i + 2 <= length(chars) && 
         paste0(chars[(i):(i+2)], collapse="") == "mul")) {
      # Skip to after "mul"
      i <- i + 3
      # Collect first number
      num1 <- ""
      while (i <= length(chars) && !grepl("\\d", chars[i])) {
        i <- i + 1
      }
      while (i <= length(chars) && grepl("\\d", chars[i])) {
        num1 <- paste0(num1, chars[i])
        i <- i + 1
      }
      # Skip non-digits
      while (i <= length(chars) && !grepl("\\d", chars[i])) {
        i <- i + 1
      }
      # Collect second number
      num2 <- ""
      while (i <= length(chars) && grepl("\\d", chars[i])) {
        num2 <- paste0(num2, chars[i])
        i <- i + 1
      }
      
      # If we found two numbers and multiplication is enabled, calculate result
      if (num1 != "" && num2 != "" && enabled) {
        results <- c(results, as.numeric(num1) * as.numeric(num2))
      }
      next
    }
    i <- i + 1
  }
  
  return(results)
}

# Process actual input for both parts
total_part1 <- sum(unlist(lapply(input, process_multiplications_part1)))
total_part2 <- sum(unlist(lapply(input, process_multiplications_part2)))

# Output results
cat("Part 1:", total_part1, "\n")
cat("Part 2:", total_part2, "\n")
