<?php

function evaluateExpression(array $numbers, array $operators): int {
    $result = $numbers[0];
    for ($i = 0; $i < count($operators); $i++) {
        if ($operators[$i] === '+') {
            $result += $numbers[$i + 1];
        } elseif ($operators[$i] === '*') {
            $result *= $numbers[$i + 1];
        } else { // concatenation operator ||
            $result = intval($result . $numbers[$i + 1]);
        }
    }
    return $result;
}

function generateOperatorCombinations(int $count): array {
    $combinations = [];
    $totalCombinations = pow(3, $count); // Each position can be + (0), * (1), or || (2)
    
    for ($i = 0; $i < $totalCombinations; $i++) {
        $combination = [];
        $value = $i;
        for ($j = 0; $j < $count; $j++) {
            $operator = $value % 3;
            $combination[] = $operator === 0 ? '+' : ($operator === 1 ? '*' : '||');
            $value = intdiv($value, 3);
        }
        $combinations[] = $combination;
    }
    
    return $combinations;
}

function canMakeTestValue(int $testValue, array $numbers): bool {
    $operatorCount = count($numbers) - 1;
    $combinations = generateOperatorCombinations($operatorCount);
    
    foreach ($combinations as $operators) {
        if (evaluateExpression($numbers, $operators) === $testValue) {
            return true;
        }
    }
    
    return false;
}

function solve(string $input): int {
    $lines = explode("\n", trim($input));
    $sum = 0;
    
    foreach ($lines as $line) {
        if (empty($line)) continue;
        
        [$testValue, $numbersStr] = explode(': ', $line);
        $numbers = array_map('intval', explode(' ', trim($numbersStr)));
        $testValue = intval($testValue);
        
        if (canMakeTestValue($testValue, $numbers)) {
            $sum += $testValue;
        }
    }
    
    return $sum;
}

// Read input file
$input = file_get_contents(__DIR__ . '/../Data/7.txt');
echo solve($input);
