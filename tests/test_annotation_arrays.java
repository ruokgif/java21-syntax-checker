@SuppressWarnings({"unchecked", "deprecation", "rawtypes"})
public class AnnotationArraysTest {
    @MyConfig(
        tags = {"fast", "beta", "experimental"},
        matrix = {{1, 2}, {3, 4}},
        emptyArr = {}
    )
    public void run() {
    }
}

@interface MyConfig {
    String[] tags() default {};
    int[][] matrix() default {};
    String[] emptyArr() default {};
}
