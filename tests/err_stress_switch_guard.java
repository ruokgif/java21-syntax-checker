public class StressSwitchGuard {
    void test(Object o) {
        switch (o) {
            case String s when s.length() > 5 -> {
                System.out.println(s);
            }
            case Integer i when -> System.out.println("bad guard");
            default -> System.out.println("def");
        }
    }
}
