package com.example.app;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;

public class ValidFullTest {
    private int id = 100;
    public static final String APP_NAME = "SyntaxChecker";

    public interface Service<T> {
        T process(T input);
    }

    public record Person(String name, int age) {}

    public void runDemo() {
        List<String> items = new ArrayList<>();
        items.add("Java 17");

        int val = 2;
        String label = switch (val) {
            case 1 -> "One";
            case 2 -> "Two";
            default -> "Other";
        };

        for (int i = 0; i < 10; i++) {
            if (i % 2 == 0) {
                System.out.println(i);
            } else {
                continue;
            }
        }

        try (BufferedReader reader = new BufferedReader(new FileReader("test.txt"))) {
            String line = reader.readLine();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
