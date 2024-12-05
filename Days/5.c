#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

#define MAX_RULES 10000
#define MAX_PAGES 1000
#define MAX_LINE 1024

// Structure to store a rule (X must come before Y)
typedef struct {
    int before;
    int after;
} Rule;

// Function to trim whitespace and newlines from a string
void trim(char* str) {
    if (!str) return;
    
    // Remove trailing newline/carriage return
    str[strcspn(str, "\r\n")] = 0;
    
    // Skip leading whitespace
    char* start = str;
    while (*start && isspace(*start)) start++;
    
    // Move string to beginning if there was leading whitespace
    if (start != str) {
        memmove(str, start, strlen(start) + 1);
    }
}

// Function to parse a line of numbers into an array
int parse_numbers(char* line, int* numbers) {
    int count = 0;
    trim(line);  // Trim the line first
    
    char* token = strtok(line, ",");
    while (token != NULL && count < MAX_PAGES) {
        // Skip empty tokens
        while (isspace(*token)) token++;
        if (*token) {
            numbers[count++] = atoi(token);
        }
        token = strtok(NULL, ",");
    }
    return count;
}

// Function to check if an update order is valid according to rules
bool is_valid_order(int* update, int update_size, Rule* rules, int rule_count) {
    // For each rule
    for (int k = 0; k < rule_count; k++) {
        int before_pos = -1;
        int after_pos = -1;
        
        // Find positions of both pages from the rule in the update
        for (int i = 0; i < update_size; i++) {
            if (update[i] == rules[k].before) before_pos = i;
            if (update[i] == rules[k].after) after_pos = i;
        }
        
        // If both pages exist in the update, check their order
        if (before_pos != -1 && after_pos != -1) {
            // If 'before' page comes after 'after' page, order is invalid
            if (before_pos > after_pos) {
                return false;
            }
        }
    }
    return true;
}

// New function to find correct order using bubble sort
void sort_by_rules(int* update, int update_size, Rule* rules, int rule_count) {
    bool swapped;
    do {
        swapped = false;
        for (int i = 0; i < update_size - 1; i++) {
            for (int k = 0; k < rule_count; k++) {
                if (update[i] == rules[k].after && update[i + 1] == rules[k].before) {
                    // Swap if order violates rule
                    int temp = update[i];
                    update[i] = update[i + 1];
                    update[i + 1] = temp;
                    swapped = true;
                }
            }
        }
    } while (swapped);
}

int main() {
    FILE* file = fopen("Data/5.txt", "r");
    if (!file) {
        fprintf(stderr, "Error: Could not open Data/5.txt\n");
        return 1;
    }

    Rule rules[MAX_RULES];
    int rule_count = 0;
    char line[MAX_LINE];
    int sum_part1 = 0;
    int sum_part2 = 0;
    bool reading_rules = true;  // Flag to track what section we're reading

    // Read each line
    while (fgets(line, sizeof(line), file)) {
        trim(line);
        if (strlen(line) == 0) continue;  // Skip empty lines
        
        if (reading_rules) {
            // Try to parse as rule
            int before, after;
            if (sscanf(line, "%d|%d", &before, &after) == 2) {
                if (rule_count >= MAX_RULES) {
                    fprintf(stderr, "Error: Too many rules (max: %d)\n", MAX_RULES);
                    fclose(file);
                    return 1;
                }
                rules[rule_count].before = before;
                rules[rule_count].after = after;
                rule_count++;
            } else {
                // If we can't parse as rule, we've hit the updates section
                reading_rules = false;
                printf("Switching to updates section. Total rules read: %d\n", rule_count);
                // Process this line as an update
                int update[MAX_PAGES];
                int update_size = parse_numbers(line, update);
                if (update_size > 0) {
                    printf("Processing update of size %d: ", update_size);
                    for (int i = 0; i < update_size; i++) {
                        printf("%d ", update[i]);
                    }
                    printf("\n");
                    
                    if (is_valid_order(update, update_size, rules, rule_count)) {
                        sum_part1 += update[update_size / 2];
                        printf("Valid order! Middle number: %d, Sum Part 1: %d\n", 
                               update[update_size / 2], sum_part1);
                    } else {
                        // Part 2: Fix incorrect orders
                        int fixed_update[MAX_PAGES];
                        memcpy(fixed_update, update, update_size * sizeof(int));
                        sort_by_rules(fixed_update, update_size, rules, rule_count);
                        sum_part2 += fixed_update[update_size / 2];
                        printf("Invalid order fixed. New order: ");
                        for (int i = 0; i < update_size; i++) {
                            printf("%d ", fixed_update[i]);
                        }
                        printf("\nMiddle number after fixing: %d, Sum Part 2: %d\n", 
                               fixed_update[update_size / 2], sum_part2);
                    }
                }
            }
        } else {
            // Process update line
            int update[MAX_PAGES];
            int update_size = parse_numbers(line, update);
            if (update_size > 0) {
                printf("Processing update of size %d: ", update_size);
                for (int i = 0; i < update_size; i++) {
                    printf("%d ", update[i]);
                }
                printf("\n");
                
                if (is_valid_order(update, update_size, rules, rule_count)) {
                    sum_part1 += update[update_size / 2];
                    printf("Valid order! Middle number: %d, Sum Part 1: %d\n", 
                           update[update_size / 2], sum_part1);
                } else {
                    // Part 2: Fix incorrect orders
                    int fixed_update[MAX_PAGES];
                    memcpy(fixed_update, update, update_size * sizeof(int));
                    sort_by_rules(fixed_update, update_size, rules, rule_count);
                    sum_part2 += fixed_update[update_size / 2];
                    printf("Invalid order fixed. New order: ");
                    for (int i = 0; i < update_size; i++) {
                        printf("%d ", fixed_update[i]);
                    }
                    printf("\nMiddle number after fixing: %d, Sum Part 2: %d\n", 
                           fixed_update[update_size / 2], sum_part2);
                }
            }
        }
    }

    // Update final output
    printf("Part 1 - Sum of middle numbers (valid orders): %d\n", sum_part1);
    printf("Part 2 - Sum of middle numbers (fixed invalid orders): %d\n", sum_part2);
    fclose(file);
    return 0;
}