import java.io.ByteArrayInputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;

public class MultiTryResourcesTest {
    public void execute() throws Exception {
        try (
            ByteArrayInputStream bais = new ByteArrayInputStream(new byte[16]);
            InputStreamReader isr = new InputStreamReader(bais);
            BufferedReader br = new BufferedReader(isr);
        ) {
            String line = br.readLine();
        }
    }
}
