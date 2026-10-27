public class Java21RecordPatterns {
    record Point(int x, int y) {}
    record ColoredPoint(Point p, String color) {}
    record Box<T>(T content) {}

    void testInstanceof(Object obj) {
        // A. Simple record pattern in instanceof
        if (obj instanceof Point(int x, int y)) {
            System.out.println(x + y);
        }

        // Simple record pattern with var
        if (obj instanceof Point(var x, var y)) {
            System.out.println(x + y);
        }

        // B. Nested record pattern in instanceof
        if (obj instanceof ColoredPoint(Point(int x, int y), String c)) {
            System.out.println(c + x + y);
        }

        // Nested with generic box
        if (obj instanceof Box<Point>(Point(var x, var y))) {
            System.out.println(x);
        }

        // Nested record pattern with multiple levels
        if (obj instanceof ColoredPoint(Point(var x, var y), var color)) {
            System.out.println(color + x + y);
        }
    }
}
