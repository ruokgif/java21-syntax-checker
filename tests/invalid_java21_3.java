class InvalidJava21C {
    void test(int x) {
        if (x > 5 when true) {
            System.out.println("illegal when keyword in if condition");
        }
    }
}
