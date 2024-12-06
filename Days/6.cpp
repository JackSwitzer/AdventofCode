#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <set>
#include <utility>
#include <algorithm>

enum Direction { UP = 0, RIGHT = 1, DOWN = 2, LEFT = 3 };

struct Point {
    int x, y;
    
    bool operator<(const Point& other) const {
        return y < other.y || (y == other.y && x < other.x);
    }
    
    bool operator==(const Point& other) const {
        return x == other.x && y == other.y;
    }
};

struct Guard {
    Point pos;
    Direction facing = UP;
};

std::vector<std::string> read_input(const std::string& path) {
    std::vector<std::string> grid;
    std::ifstream file(path);
    std::string line;
    
    if (!file.is_open()) {
        std::cerr << "Failed to open file: " << path << std::endl;
        return grid;
    }
    
    while (std::getline(file, line)) {
        // Skip empty lines and ensure we have valid content
        if (!line.empty()) {
            grid.push_back(line);
        }
    }
    
    return grid;
}

bool creates_loop(const std::vector<std::string>& original_grid, Point obstruction, const std::set<Point>& guard_path) {
    // Don't place obstruction on guard path or existing obstacles
    if (guard_path.count(obstruction) > 0 || 
        original_grid[obstruction.y][obstruction.x] != '.') {
        return false;
    }

    std::vector<std::string> grid = original_grid;
    grid[obstruction.y][obstruction.x] = '#';

    Guard guard;
    // Find start position ('^' character)
    for (int y = 0; y < grid.size(); y++) {
        for (int x = 0; x < grid[y].length(); x++) {
            if (grid[y][x] == '^') {
                guard.pos = {x, y};
                goto found_start;
            }
        }
    }
    found_start:

    std::set<std::pair<Point, Direction>> visited_states;
    std::set<Point> loop_positions;
    bool in_loop = false;
    std::pair<Point, Direction> loop_start;
    
    const int max_steps = grid.size() * grid[0].length() * 4;
    int steps = 0;

    while (steps++ < max_steps) {
        auto state = std::make_pair(guard.pos, guard.facing);
        
        // Check if we've left the grid
        if (guard.pos.y < 0 || guard.pos.y >= grid.size() || 
            guard.pos.x < 0 || guard.pos.x >= grid[guard.pos.y].length()) {
            return false;
        }

        // If we've seen this state before, we might have found a loop
        if (visited_states.count(state) > 0) {
            if (!in_loop) {
                in_loop = true;
                loop_start = state;
                loop_positions.clear();
            } else if (state == loop_start) {
                // We've completed at least one full loop
                return loop_positions.size() >= 2;
            }
        }

        visited_states.insert(state);
        if (in_loop) {
            loop_positions.insert(guard.pos);
        }
        
        // Calculate next position
        Point next = guard.pos;
        switch (guard.facing) {
            case UP: next.y--; break;
            case RIGHT: next.x++; break;
            case DOWN: next.y++; break;
            case LEFT: next.x--; break;
        }

        // Check if we hit a wall or obstacle
        if (next.y < 0 || next.y >= grid.size() || 
            next.x < 0 || next.x >= grid[next.y].length() || 
            grid[next.y][next.x] == '#') {
            guard.facing = static_cast<Direction>((guard.facing + 1) % 4);
        } else {
            guard.pos = next;
        }
    }
    
    return false;
}

int solve_part1(const std::string& inputPath) {
    auto grid = read_input(inputPath);
    std::set<Point> guard_path;
    Guard guard;
    
    // Find starting position
    bool found = false;
    for (int y = 0; y < grid.size() && !found; y++) {
        for (int x = 0; x < grid[y].length(); x++) {
            if (grid[y][x] == '^') {
                guard.pos = {x, y};
                guard_path.insert(guard.pos);
                found = true;
                break;
            }
        }
    }

    if (!found) {
        std::cerr << "No starting position found!" << std::endl;
        return 0;
    }

    // Track the path until we either leave the grid or revisit a position
    while (true) {
        Point next = guard.pos;
        switch (guard.facing) {
            case UP: next.y--; break;
            case RIGHT: next.x++; break;
            case DOWN: next.y++; break;
            case LEFT: next.x--; break;
        }

        // Check if we're leaving the grid
        if (next.y < 0 || next.y >= grid.size() || 
            next.x < 0 || next.x >= grid[next.y].length()) {
            break;  // We've left the grid
        }

        // Check if we hit an obstacle
        if (grid[next.y][next.x] == '#') {
            guard.facing = static_cast<Direction>((guard.facing + 1) % 4);
        } else {
            guard.pos = next;
            if (guard_path.count(guard.pos) > 0) {
                // We've completed a loop, but keep going until we leave the grid
                continue;
            }
            guard_path.insert(guard.pos);
        }
    }

    return guard_path.size();
}

int solve_part2(const std::string& inputPath) {
    auto grid = read_input(inputPath);
    std::set<Point> guard_path;
    Guard guard;
    
    // Find starting position and track initial path
    for (int y = 0; y < grid.size(); y++) {
        for (int x = 0; x < grid[y].length(); x++) {
            if (grid[y][x] == '^') {
                guard.pos = {x, y};
                guard_path.insert(guard.pos);
                break;
            }
        }
    }

    // Track the original path
    while (true) {
        Point next = guard.pos;
        switch (guard.facing) {
            case UP: next.y--; break;
            case RIGHT: next.x++; break;
            case DOWN: next.y++; break;
            case LEFT: next.x--; break;
        }

        if (next.y < 0 || next.y >= grid.size() || 
            next.x < 0 || next.x >= grid[next.y].length() || 
            grid[next.y][next.x] == '#') {
            guard.facing = static_cast<Direction>((guard.facing + 1) % 4);
        } else {
            guard.pos = next;
            if (guard_path.count(guard.pos) > 0) break;
            guard_path.insert(guard.pos);
        }
    }

    int count = 0;
    // Check ALL possible positions in the grid
    for (int y = 0; y < grid.size(); y++) {
        for (int x = 0; x < grid[y].length(); x++) {
            Point pos = {x, y};
            // Skip the starting position and existing obstacles
            if (grid[y][x] == '^' || grid[y][x] == '#') {
                continue;
            }
            if (creates_loop(grid, pos, guard_path)) {
                count++;
            }
        }
    }

    return count;
}

int main() {
    std::string inputPath = "C:/Users/jacks/Documents/Life/Projects/Puzzles/AdventofCode/Data/6.txt";
    
    int result1 = solve_part1(inputPath);
    std::cout << "Part 1: " << result1 << std::endl;
    
    int result2 = solve_part2(inputPath);
    std::cout << "Part 2: " << result2 << std::endl;
    
    return 0;
}
