// Lexer Comprehensive Test File for Java Syntax Checker
package com.example.test;

import java.util.List;
import java.util.Map;

/**
 * Javadoc documentation comment spanning multiple lines.
 * Line tracking test across comments.
 */
public sealed class LexerTest permits SubClass {
    // 1. Primitive and Object types
    private static final int DECIMAL_VAL = 1_000_000;
    private static final long HEX_VAL = 0xDead_BeefL;
    private static final int BIN_VAL = 0b1010_1100;
    private static final int OCT_VAL = 0755;
    
    // 2. Floating-point numbers
    double float1 = 3.14159;
    float float2 = .5f;
    double float3 = 1e-10;
    double hexFloat = 0x1.0p-3;

    // 3. Characters, Strings, and Text Blocks
    char ch1 = 'a';
    char ch2 = '\n';
    char ch3 = '\u0041';
    String str = "Hello \"Java\" \t \u005c \n World";
    String textBlock = """
        SELECT *
        FROM users
        WHERE age > 18
        """;

    // 4. Modern Java Keywords & Constructs
    record Point(int x, int y) {}
    var count = 42;

    // 5. Multi-character operators and separators
    public void testOperators() {
        int a = 10;
        int b = 20;
        a += b;
        a >>>= 2;
        boolean cond = (a >= 5) && (b != 0) || !(a == b);
        a++;
        --b;
        List<String> list = null;
        list.forEach(System.out::println);
        Runnable r = () -> {
            yieldVal: switch (a) {
                case 1 -> System.out.println("One");
                default -> yield 0;
            };
        };
    }
}
