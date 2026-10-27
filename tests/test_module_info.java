open module com.example.myapp {
    requires java.base;
    requires transitive java.logging;
    requires static java.compiler;
    exports com.example.myapp;
    exports com.example.myapp.internal to com.example.other, com.example.tool;
    opens com.example.myapp.reflect to com.google.gson;
    uses com.example.myapp.spi.ServicePlugin;
    provides com.example.myapp.spi.ServicePlugin with com.example.myapp.spi.impl.DefaultPlugin;
}
