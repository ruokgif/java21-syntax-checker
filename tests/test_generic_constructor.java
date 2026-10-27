public class GenericConstructorTest {
    public static class Box<T> {
        public <E> Box(E element) {
        }
    }

    public void test() {
        Box<Integer> b1 = new <String>Box<Integer>("element");
        Box<Double> b2 = new <Integer>Box<Double>(123);
    }
}
