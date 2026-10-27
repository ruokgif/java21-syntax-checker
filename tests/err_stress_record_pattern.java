public class StressRecordPattern {
    record Point(double x, double y) {}
    record Rect(Point p1, Point p2) {}
    String eval(Object o) {
        return switch (o) {
            case Rect(Point(double x1, double y1), Point(double x2, )) -> "rect";
            default -> "other";
        };
    }
}
