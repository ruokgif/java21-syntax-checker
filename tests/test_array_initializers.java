public class TestArrayInitializers {
    // Field declarations with array initializers
    private String[] fieldDepartments = {
        "CSE", "ECE", "IT", "EEE"
    };
    private int[] fieldEmpty = {};
    private int[][] fieldNested = {{1, 2}, {3, 4}};
    private int[] fieldCreated = new int[] {10, 20, 30};

    public static void main(String[] args) {
        // Form 1: Array initializer directly
        String[] departments = {
            "CSE", "ECE", "IT", "EEE"
        };

        // Form 2: Array creation expression with array initializer
        String[] values = new String[] {"A", "B", "C"};

        // Empty array initializers
        int[] empty1 = {};
        int[] empty2 = new int[] {};

        // Optional trailing comma
        String[] trailing = {"A", "B", "C",};
        String[] createdTrailing = new String[] {"X", "Y",};

        // Nested array initializers (multidimensional)
        int[][] matrix = {
            {1, 2, 3},
            {4, 5, 6}
        };

        int[][] nestedWithTrailing = {
            {10, 20,},
            {30, 40,},
        };

        int[][] emptyNested = {
            {},
            {}
        };

        int[][][] cube = {
            {{1, 2}, {3, 4}},
            {{5, 6}, {7, 8}}
        };

        int[][] newMatrix = new int[][] {
            {1, 2},
            {3, 4}
        };

        // Array indexing still works correctly
        int first = matrix[0][0];
        departments[0] = "CS";
    }
}
