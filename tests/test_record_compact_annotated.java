public class RecordCompactAnnotatedTest {
    public record Range(@Deprecated int min, int max) {
        @SuppressWarnings("all")
        public Range {
            if (min > max) {
                throw new IllegalArgumentException();
            }
        }
    }

    public record Pair<A, B>(A first, B second) {
        public Pair {
        }
    }

    public static String eval(Object o) {
        return switch (o) {
            case Range(int a, int b) when a == b -> "point";
            case Pair(Range(int a, int b), String s) -> "nested " + s;
            default -> "other";
        };
    }
}
