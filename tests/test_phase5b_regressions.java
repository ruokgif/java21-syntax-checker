package com.example.regressions;

import java.util.List;
import java.util.function.Function;

@Deprecated
public class Phase5BRegressions {

    // Contextual keyword 'sealed' as modifier
    public sealed interface Node permits Leaf, Branch {}
    public final class Leaf implements Node {}
    public non-sealed class Branch implements Node {}

    // Qualified names & chained expressions
    public static void testExpressions() {
        int x = 10;
        int y = (x) + 5; // Parenthesized expression
        System.out.println(java.lang.Math.max(x, y));
    }

    // Lambdas: single param without parens, with explicit type in parens, and multi-param
    public void testLambdas() {
        Function<Integer, Integer> f1 = x -> x * 2;
        Function<Integer, Integer> f2 = (Integer x) -> x * 3;
        List<String> list = List.of("a", "b");
        list.forEach(s -> System.out.println(s));
    }

    // Switch case with constant, patterns, and guards
    public String testSwitch(Object obj, int code, boolean flag) {
        // Switch statement
        switch (code) {
            case 1 when flag:
                return "one";
            case 2:
                return "two";
            default:
                return "other";
        }
    }
}
