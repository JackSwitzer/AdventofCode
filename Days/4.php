<?php

function readInput($filename) {
    $data = file_get_contents($filename);
    return array_map('str_split', explode("\n", $data));
}

function findPattern($matrix, $pattern, $width) {
    $matches = 0;
    for ($i = 0; $i < count($matrix) - $width + 1; $i++) {
        for ($j = 0; $j < count($matrix[$i]) - $width + 1; $j++) {
            $block = "";
            for ($d = 0; $d < $width; $d++) {
                $block .= implode("", array_slice($matrix[$i + $d], $j, $width));
            }
            if (preg_match("/$pattern/", $block)) {
                $matches++;
            }
        }
    }
    return $matches;
}

function rotateGrid($matrix) {
    if (empty($matrix) || empty($matrix[0])) {
        return [];
    }
    
    $height = count($matrix);
    $width = count($matrix[0]);
    
    $rotated = array();
    for ($i = 0; $i < $width; $i++) {
        $newRow = array();
        for ($j = $height - 1; $j >= 0; $j--) {
            if (isset($matrix[$j][$i])) {
                $newRow[] = $matrix[$j][$i];
            }
        }
        $rotated[] = $newRow;
    }
    return $rotated;
}

// Read input
$grid = readInput('Data/4.txt');

// Part 1
$part1 = 0;
$matrix = $grid;
for ($rotation = 0; $rotation < 4; $rotation++) {
    // Count horizontal XMAS
    foreach ($matrix as $row) {
        $part1 += substr_count(implode("", $row), "XMAS");
    }
    // Count diagonal XMAS
    $part1 += findPattern($matrix, "X.{4}M.{4}A.{4}S", 4);
    // Rotate the grid
    $matrix = rotateGrid($matrix);
}

// Part 2
$part2 = 0;
$matrix = $grid;
for ($rotation = 0; $rotation < 4; $rotation++) {
    $part2 += findPattern($matrix, "M.M.A.S.S", 3);
    $matrix = rotateGrid($matrix);
}

echo "Part 1: " . $part1 . "\n";
echo "Part 2: " . $part2 . "\n";

?> 