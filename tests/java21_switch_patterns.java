public class Java21SwitchPatterns {
    record Point(double x, double y) {}
    record Rect(Point topLeft, Point bottomRight) {}

    String formatValue(Object obj) {
        // C. Type pattern in switch, D. Record pattern in switch, E. when guard, F. null case
        return switch (obj) {
            case null -> "null value";
            case Integer i when i > 0 -> "positive int: " + i;
            case Integer i -> "non-positive int: " + i;
            case String s when s.isEmpty() -> "empty string";
            case String s -> "string of len: " + s.length();
            case Point(double x, double y) when x == 0 && y == 0 -> "origin";
            case Rect(Point(var x1, var y1), Point(var x2, var y2)) -> "rectangle";
            case default -> "something else";
        };
    }

    void testStatementSwitch(Object obj) {
        switch (obj) {
            case null, default:
                System.out.println("null or default");
                break;
            case String s when s.length() > 5:
                System.out.println("long string");
                break;
            case Point(double x, double y):
                System.out.println("point at " + x + ", " + y);
                break;
        }
    }
}
