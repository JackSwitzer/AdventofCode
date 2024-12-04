//
// Created by jacks on 2024-12-04.
//

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cassert>

using namespace std;

// Function to check if the "XMAS" pattern is found starting from a given position
bool findXMAS(const vector<string>& grid, int row, int col, int dRow, int dCol) {
    int numRows = grid.size();
    int numCols = grid[0].size();
    string target = "XMAS";

    // Check if we can fit the word "XMAS" starting from (row, col) in direction (dRow, dCol)
    for (int i = 0; i < 4; ++i) {
        int newRow = row + i * dRow;
        int newCol = col + i * dCol;
        if (newRow < 0 || newRow >= numRows || newCol < 0 || newCol >= numCols || grid[newRow][newCol] != target[i]) {
            return false;
        }
    }
    return true;
}

// Function to count all occurrences of the "XMAS" pattern
int countXMASOccurrences(const vector<string>& grid) {
    int count = 0;
    int numRows = grid.size();
    int numCols = grid[0].size();

    // Iterate through each position in the grid and try all 8 possible directions
    vector<pair<int, int>> directions = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}, {1, 1}, {-1, -1}, {1, -1}, {-1, 1}};
    for (int row = 0; row < numRows; ++row) {
        for (int col = 0; col < numCols; ++col) {
            for (const auto& [dRow, dCol] : directions) {
                if (findXMAS(grid, row, col, dRow, dCol)) {
                    ++count;
                }
            }
        }
    }

    return count;
}

// Function to check if the "X-MAS" pattern is found centered at a given position
bool findXMASPattern(const vector<string>& grid, int row, int col) {
    int numRows = grid.size();
    int numCols = grid[0].size();

    // Check if we can fit the "X-MAS" pattern centered at (row, col)
    if (row - 1 < 0 || row + 1 >= numRows || col - 1 < 0 || col + 1 >= numCols) {
        return false;
    }

    // The pattern is an 'M' at all four corners and an 'A' at the center
    if (grid[row - 1][col - 1] == 'M' && grid[row - 1][col + 1] == 'S' &&
        grid[row + 1][col - 1] == 'M' && grid[row + 1][col + 1] == 'S' &&
        grid[row][col] == 'A') {
        return true;
    }

    return false;
}

// Function to count all occurrences of the "X-MAS" pattern
int countXMASPatternOccurrences(const vector<string>& grid) {
    int count = 0;
    int numRows = grid.size();
    int numCols = grid[0].size();

    // Iterate through each position in the grid
    for (int row = 1; row < numRows - 1; ++row) {
        for (int col = 1; col < numCols - 1; ++col) {
            if (findXMASPattern(grid, row, col)) {
                ++count;
            }
        }
    }

    return count;
}

// Function to run test cases
void runTests() {
    vector<string> testGrid1 = {
        "XMAS",
        "....",
        "....",
        "...."
    };
    assert(countXMASOccurrences(testGrid1) == 1);

    vector<string> testGrid2 = {
        "XMASXMAS",
        "........",
        "........",
        "........"
    };
    assert(countXMASOccurrences(testGrid2) == 2);

    vector<string> testGrid3 = {
        "X.....S",
        ".M.A.S.",
        "M.....S"
    };
    assert(countXMASPatternOccurrences(testGrid3) == 1);

    vector<string> testGrid4 = {
        "XMAS",
        "SAMX",
        "AMXS",
        "MSAM"
    };
    assert(countXMASOccurrences(testGrid4) == 4);

    vector<string> testGrid5 = {
        "..M.S..",
        "..A....",
        "M.S.M.."
    };
    assert(countXMASPatternOccurrences(testGrid5) == 1);

    vector<string> testGrid6 = {
        "..M.S..",
        ".A.....",
        "S.M.S..",
        "..A.A..",
        "..M.S.."
    };
    assert(countXMASPatternOccurrences(testGrid6) == 3);

    cout << "All test cases passed!" << endl;
}

int main() {
    runTests();

    // Open the input file
    ifstream inputFile("C:/Users/jacks/Documents/Life/Projects/Puzzles/AdventOfCode/Data/4.txt");
    if (!inputFile) {
        cerr << "Error: Unable to open file Data/4.txt" << endl;
        return 1;
    }

    // Read the grid from the file
    vector<string> grid;
    string line;
    while (getline(inputFile, line)) {
        grid.push_back(line);
    }
    inputFile.close();

    // Count the number of occurrences of "XMAS" pattern
    int totalXMASPatternOccurrences = countXMASOccurrences(grid);
    cout << "Total occurrences of 'XMAS' pattern: " << totalXMASPatternOccurrences << endl;

    // Count the number of occurrences of "X-MAS" pattern (Part Two)
    int totalXMASPatternOccurrencesPartTwo = countXMASPatternOccurrences(grid);
    cout << "Total occurrences of 'X-MAS' pattern (Part Two): " << totalXMASPatternOccurrencesPartTwo << endl;

    return 0;
}
