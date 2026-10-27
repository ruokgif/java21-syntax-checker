class InvalidJava21A {
    void test(Object o) {
        switch (o) {
            case String s when -> System.out.println("missing expression after when");
        }
    }
}
