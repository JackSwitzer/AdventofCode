import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;

public class Day2 {
    private static boolean isSafeReport(String line) {
        // Convert string numbers to integers
        int[] nums = Arrays.stream(line.split(" "))
                          .mapToInt(Integer::parseInt)
                          .toArray();
        
        // Get differences between adjacent numbers
        boolean allIncreasing = true;
        boolean allDecreasing = true;
        
        for (int i = 0; i < nums.length - 1; i++) {
            int diff = nums[i + 1] - nums[i];
            
            // Check if difference is between 1 and 3 (absolute value)
            if (Math.abs(diff) < 1 || Math.abs(diff) > 3) {
                return false;
            }
            
            // Track if sequence is increasing or decreasing
            if (diff > 0) allDecreasing = false;
            if (diff < 0) allIncreasing = false;
        }
        
        return allIncreasing || allDecreasing;
    }

    private static boolean isSafeReportWithDampener(String line) {
        int[] nums = Arrays.stream(line.split(" "))
                          .mapToInt(Integer::parseInt)
                          .toArray();
        
        // First check if it's safe without removing any number
        if (isSafeReport(line)) {
            return true;
        }
        
        // Try removing each number one at a time
        for (int i = 0; i < nums.length; i++) {
            int[] reducedNums = new int[nums.length - 1];
            int index = 0;
            
            // Create new array without the current number
            for (int j = 0; j < nums.length; j++) {
                if (j != i) {
                    reducedNums[index++] = nums[j];
                }
            }
            
            // Check if this sequence is safe
            boolean allIncreasing = true;
            boolean allDecreasing = true;
            
            for (int j = 0; j < reducedNums.length - 1; j++) {
                int diff = reducedNums[j + 1] - reducedNums[j];
                
                if (Math.abs(diff) < 1 || Math.abs(diff) > 3) {
                    allIncreasing = false;
                    allDecreasing = false;
                    break;
                }
                
                if (diff > 0) allDecreasing = false;
                if (diff < 0) allIncreasing = false;
            }
            
            if (allIncreasing || allDecreasing) {
                return true;
            }
        }
        
        return false;
    }

    public static void main(String[] args) {
        int safeCount = 0;
        int safeCountWithDampener = 0;
        
        try (BufferedReader reader = new BufferedReader(new FileReader("Data/2.txt"))) {
            String line;
            while ((line = reader.readLine()) != null) {
                line = line.trim();
                if (isSafeReport(line)) {
                    safeCount++;
                }
                if (isSafeReportWithDampener(line)) {
                    safeCountWithDampener++;
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        System.out.println("Part 1 - Number of safe reports: " + safeCount);
        System.out.println("Part 2 - Number of safe reports with dampener: " + safeCountWithDampener);
    }
}
