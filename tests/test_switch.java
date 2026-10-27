class Test {
    void test() {
        int val = 2;
        String label = switch (val) {
            case 1 -> "One";
            case 2 -> "Two";
            default -> "Other";
        };
    }
}
