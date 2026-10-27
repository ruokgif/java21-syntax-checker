import java.util.List;
public class StressGenericLambda {
    <T extends Comparable<T> > void sortAndProcess(List<T> list) {
        list.stream()
            .map(x -> {
                int len = x.toString().length();
                return len == ? 0 : len;
            })
            .forEach(System.out::println);
    }
}
