# Read input file as a single string (like Python's approach)
input <- paste(readLines("Data/3.txt"), collapse = "\n")

# Function for Part 1 - strict pattern matching
process_multiplications_part1 <- function(text) {
  # Match pattern exactly as in Python
  mul_pattern <- "mul\\((\\d{1,3}),(\\d{1,3})\\)"
  
  # Find all matches
  matches <- gregexpr(mul_pattern, text, perl = TRUE)[[1]]
  
  # If no matches found, return 0
  if (matches[1] == -1) return(0)
  
  # Get all matches
  mul_strings <- regmatches(text, list(matches))[[1]]
  
  # Sum all multiplications
  total <- 0
  for (mul_str in mul_strings) {
    nums <- as.numeric(unlist(strsplit(gsub("mul\\(|\\)", "", mul_str), ",")))
    total <- total + nums[1] * nums[2]
  }
  
  return(total)
}

# Function for Part 2 - with state tracking
process_multiplications_part2 <- function(text) {
  # Patterns exactly as in Python
  mul_pattern <- "mul\\((\\d{1,3}),(\\d{1,3})\\)"
  control_pattern <- "do\\(\\)|don't\\(\\)"
  
  # Find all matches with positions
  mul_matches <- gregexpr(mul_pattern, text, perl = TRUE)[[1]]
  control_matches <- gregexpr(control_pattern, text, perl = TRUE)[[1]]
  
  # Get all matches
  mul_strings <- if (mul_matches[1] != -1) regmatches(text, list(mul_matches))[[1]] else character(0)
  control_strings <- if (control_matches[1] != -1) regmatches(text, list(control_matches))[[1]] else character(0)
  
  # Create events list similar to Python
  events <- data.frame(
    position = c(mul_matches, if(length(control_strings) > 0) control_matches else numeric(0)),
    type = c(rep("mul", length(mul_matches)), 
             if(length(control_strings) > 0) rep("control", length(control_strings)) else character(0)),
    value = c(mul_strings, control_strings),
    stringsAsFactors = FALSE
  )
  events <- events[order(events$position), ]
  
  # Process events in order - exactly like Python
  enabled <- TRUE
  total <- 0
  
  for (i in seq_len(nrow(events))) {
    if (events$type[i] == "control") {
      enabled <- events$value[i] == "do()"
    } else {
      if (enabled) {
        nums <- as.numeric(unlist(strsplit(gsub("mul\\(|\\)", "", events$value[i]), ",")))
        total <- total + nums[1] * nums[2]
      }
    }
  }
  
  return(total)
}

# Process input directly (not using lapply anymore)
total_part1 <- process_multiplications_part1(input)
total_part2 <- process_multiplications_part2(input)

# Output results
cat("Part 1:", total_part1, "\n")
cat("Part 2:", total_part2, "\n")
