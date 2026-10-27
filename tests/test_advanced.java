package com.example.features;

import java.util.*;
import java.io.Serializable;

@Deprecated
public class AdvancedFeaturesTest<T extends Number & Serializable> extends Object implements Serializable {

    // Sealed interface & Records
    public sealed interface Shape permits Circle, Rectangle {}
    public record Circle(double radius) implements Shape {}
    public record Rectangle(double width, double height) implements Shape {}

    // Enum with methods and fields
    public enum Level {
        LOW(1), MEDIUM(2), HIGH(3);
        private final int code;
        Level(int code) { this.code = code; }
        public int getCode() { return code; }
    }

    // Varargs, generics, arrays
    public static <E> List<E> createList(E... elements) {
        List<E> list = new ArrayList<>();
        for (E elem : elements) {
            list.add(elem);
        }
        return list;
    }

    public void testControlFlow() {
        int a = 10, b = 20;
        int max = (a > b) ? a : b;

        // While loop
        while (a > 0) {
            a--;
            if (a == 5) break;
        }

        // Do-while loop
        do {
            b++;
        } while (b < 30);

        // Switch expression with yield
        int score = 2;
        String grade = switch (score) {
            case 1:
                yield "F";
            case 2:
                yield "D";
            default:
                yield "A";
        };

        // Lambda expressions & method references
        Runnable r = () -> System.out.println("Hello Lambda");
        List<String> names = Arrays.asList("Alice", "Bob");
        names.forEach(System.out::println);
    }
}
