# Java Deprecated APIs

## Java Core APIs

### Date and Calendar (Java 8+)

```java
// ❌ Deprecated
import java.util.Date;
import java.util.Calendar;

Date date = new Date();
date.setYear(2024);  // Deprecated
date.setMonth(5);  // Deprecated

Calendar cal = Calendar.getInstance();
cal.set(2024, 5, 15);

// ✅ Modern - java.time API
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.ZonedDateTime;
import java.time.Instant;

LocalDate date = LocalDate.of(2024, 6, 15);
LocalDateTime dateTime = LocalDateTime.now();
ZonedDateTime zonedDateTime = ZonedDateTime.now();
Instant instant = Instant.now();
```

### Thread.stop(), Thread.suspend(), Thread.resume()

```java
// ❌ Deprecated (unsafe - can corrupt state)
Thread thread = new Thread(runnable);
thread.start();
thread.stop();  // Dangerous
thread.suspend();  // Deadlock-prone
thread.resume();  // Deadlock-prone

// ✅ Modern - use interruption
class MyRunnable implements Runnable {
    private volatile boolean running = true;

    public void run() {
        while (running && !Thread.currentThread().isInterrupted()) {
            // Do work
        }
    }

    public void stop() {
        running = false;
    }
}

// Or use interrupt
thread.interrupt();
```

### finalize() method

```java
// ❌ Deprecated (unreliable, unpredictable)
public class Resource {
    @Override
    protected void finalize() throws Throwable {
        // Cleanup
        super.finalize();
    }
}

// ✅ Modern - use try-with-resources
public class Resource implements AutoCloseable {
    @Override
    public void close() {
        // Cleanup
    }
}

// Usage
try (Resource resource = new Resource()) {
    // Use resource
}

// ✅ Alternative - Cleaner API (Java 9+)
import java.lang.ref.Cleaner;

public class Resource {
    private static final Cleaner cleaner = Cleaner.create();

    static class State implements Runnable {
        public void run() {
            // Cleanup action
        }
    }

    private final Cleaner.Cleanable cleanable;

    public Resource() {
        State state = new State();
        this.cleanable = cleaner.register(this, state);
    }
}
```

### Integer constructor (Java 9+)

```java
// ❌ Deprecated
Integer num1 = new Integer(42);
Integer num2 = new Integer("42");

// ✅ Modern - use valueOf or autoboxing
Integer num1 = Integer.valueOf(42);
Integer num2 = Integer.valueOf("42");
Integer num3 = 42;  // Autoboxing (preferred)
```

### Class.newInstance() (Java 9+)

```java
// ❌ Deprecated (doesn't handle exceptions properly)
Class<?> clazz = MyClass.class;
MyClass instance = (MyClass) clazz.newInstance();

// ✅ Modern - use getDeclaredConstructor()
Class<?> clazz = MyClass.class;
MyClass instance = clazz.getDeclaredConstructor().newInstance();
```

### SecurityManager (Java 17+)

```java
// ❌ Deprecated
System.setSecurityManager(new SecurityManager());

// ✅ Modern - use OS-level security, containers, or Java module system
// No direct replacement - migrate to modern security approaches
```

## Spring Framework

### WebMvcConfigurerAdapter (Spring 5.0+)

```java
// ❌ Deprecated
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;

@Configuration
public class WebConfig extends WebMvcConfigurerAdapter {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**");
    }
}

// ✅ Modern - implement WebMvcConfigurer
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**");
    }
}
```

### @Autowired with @Nullable

```java
// ❌ Old style
import org.springframework.lang.Nullable;

public class MyService {
    @Autowired
    @Nullable
    private OptionalDependency dependency;
}

// ✅ Modern - use required=false
public class MyService {
    @Autowired(required = false)
    private OptionalDependency dependency;
}

// ✅ Best - constructor injection with Optional
public class MyService {
    private final Optional<OptionalDependency> dependency;

    @Autowired
    public MyService(Optional<OptionalDependency> dependency) {
        this.dependency = dependency;
    }
}
```

### RestTemplate (Spring 5.0+)

```java
// ❌ In maintenance mode
import org.springframework.web.client.RestTemplate;

RestTemplate restTemplate = new RestTemplate();
String result = restTemplate.getForObject(url, String.class);

// ✅ Modern - use WebClient (reactive)
import org.springframework.web.reactive.function.client.WebClient;

WebClient webClient = WebClient.create();
String result = webClient.get()
    .uri(url)
    .retrieve()
    .bodyToMono(String.class)
    .block();
```

## Hibernate

### Criteria API (Hibernate 5.2+)

```java
// ❌ Deprecated (legacy API)
import org.hibernate.Criteria;
import org.hibernate.criterion.Restrictions;

Criteria criteria = session.createCriteria(User.class);
criteria.add(Restrictions.eq("username", "john"));
List<User> users = criteria.list();

// ✅ Modern - JPA Criteria API
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Root;

CriteriaBuilder cb = entityManager.getCriteriaBuilder();
CriteriaQuery<User> query = cb.createQuery(User.class);
Root<User> root = query.from(User.class);
query.select(root).where(cb.equal(root.get("username"), "john"));
List<User> users = entityManager.createQuery(query).getResultList();
```

## JUnit

### JUnit 4 annotations (JUnit 5+)

```java
// ❌ JUnit 4
import org.junit.Test;
import org.junit.Before;
import org.junit.After;
import org.junit.BeforeClass;
import org.junit.AfterClass;
import org.junit.Ignore;

public class MyTest {
    @BeforeClass
    public static void setupClass() { }

    @Before
    public void setup() { }

    @Test
    public void testSomething() { }

    @Ignore
    @Test
    public void ignoredTest() { }

    @After
    public void teardown() { }

    @AfterClass
    public static void teardownClass() { }
}

// ✅ JUnit 5
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.Disabled;

class MyTest {
    @BeforeAll
    static void setupClass() { }

    @BeforeEach
    void setup() { }

    @Test
    void testSomething() { }

    @Disabled
    @Test
    void ignoredTest() { }

    @AfterEach
    void teardown() { }

    @AfterAll
    static void teardownClass() { }
}
```

## Apache Commons

### Commons IO - FileUtils.readFileToString (Commons IO 2.5+)

```java
// ❌ Old style
import org.apache.commons.io.FileUtils;

String content = FileUtils.readFileToString(file);

// ✅ Modern - specify charset
import java.nio.charset.StandardCharsets;

String content = FileUtils.readFileToString(file, StandardCharsets.UTF_8);

// ✅ Best - use Java NIO
import java.nio.file.Files;
import java.nio.file.Paths;

String content = Files.readString(Paths.get("file.txt"), StandardCharsets.UTF_8);
```

## JDBC

### DriverManager.getConnection without try-with-resources

```java
// ❌ Old style
import java.sql.Connection;
import java.sql.DriverManager;

Connection conn = null;
try {
    conn = DriverManager.getConnection(url, user, password);
    // Use connection
} finally {
    if (conn != null) {
        conn.close();
    }
}

// ✅ Modern - use try-with-resources
try (Connection conn = DriverManager.getConnection(url, user, password)) {
    // Use connection
}

// ✅ Best - use DataSource
import javax.sql.DataSource;

@Autowired
private DataSource dataSource;

try (Connection conn = dataSource.getConnection()) {
    // Use connection
}
```

## Android

### AsyncTask (Android 11+)

```java
// ❌ Deprecated
private class DownloadTask extends AsyncTask<URL, Integer, String> {
    protected String doInBackground(URL... urls) {
        // Background work
        return result;
    }

    protected void onPostExecute(String result) {
        // Update UI
    }
}

new DownloadTask().execute(url);

// ✅ Modern - use Kotlin Coroutines
import kotlinx.coroutines.*

lifecycleScope.launch {
    val result = withContext(Dispatchers.IO) {
        // Background work
    }
    // Update UI
}

// ✅ Alternative - use java.util.concurrent
import java.util.concurrent.Executors;

Executor executor = Executors.newSingleThreadExecutor();
Handler handler = new Handler(Looper.getMainLooper());

executor.execute(() -> {
    // Background work
    String result = doWork();

    handler.post(() -> {
        // Update UI
    });
});
```

### ProgressDialog (Android 8.0+)

```java
// ❌ Deprecated
ProgressDialog dialog = new ProgressDialog(context);
dialog.setMessage("Loading...");
dialog.show();

// ✅ Modern - use ProgressBar in layout
// Define in XML layout
<ProgressBar
    android:id="@+id/progressBar"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:visibility="gone" />

// Control visibility in code
progressBar.setVisibility(View.VISIBLE);
progressBar.setVisibility(View.GONE);
```

### startActivityForResult (Android 10+)

```java
// ❌ Deprecated
startActivityForResult(intent, REQUEST_CODE);

@Override
protected void onActivityResult(int requestCode, int resultCode, Intent data) {
    if (requestCode == REQUEST_CODE && resultCode == RESULT_OK) {
        // Handle result
    }
}

// ✅ Modern - use Activity Result API
ActivityResultLauncher<Intent> launcher = registerForActivityResult(
    new ActivityResultContracts.StartActivityForResult(),
    result -> {
        if (result.getResultCode() == RESULT_OK) {
            Intent data = result.getData();
            // Handle result
        }
    }
);

launcher.launch(intent);
```
