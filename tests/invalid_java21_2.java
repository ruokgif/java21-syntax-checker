class InvalidJava21B {
    record Point(int x, int y) {}
    void test(Object o) {
        if (o instanceof Point(int x, int y {
            System.out.println("unclosed record pattern parens");
        }
    }
}
