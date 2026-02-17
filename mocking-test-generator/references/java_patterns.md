# Java Mocking Patterns (Mockito + JUnit)

## Common Mock Patterns

### External API Calls

```java
import static org.mockito.Mockito.*;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.junit.jupiter.api.extension.ExtendWith;

@ExtendWith(MockitoExtension.class)
class ApiServiceTest {
    @Mock
    private HttpClient httpClient;

    @Test
    void testApiCall() throws Exception {
        HttpResponse mockResponse = mock(HttpResponse.class);
        when(httpClient.send(any(), any())).thenReturn(mockResponse);
        when(mockResponse.statusCode()).thenReturn(200);
        when(mockResponse.body()).thenReturn("{\"data\":\"value\"}");

        ApiService service = new ApiService(httpClient);
        String result = service.fetchData();

        assertEquals("value", result);
        verify(httpClient).send(any(), any());
    }
}
```

### Database Operations

```java
@ExtendWith(MockitoExtension.class)
class DatabaseServiceTest {
    @Mock
    private Connection connection;

    @Mock
    private PreparedStatement statement;

    @Mock
    private ResultSet resultSet;

    @Test
    void testDatabaseQuery() throws SQLException {
        when(connection.prepareStatement(anyString())).thenReturn(statement);
        when(statement.executeQuery()).thenReturn(resultSet);
        when(resultSet.next()).thenReturn(true, false);
        when(resultSet.getString("column")).thenReturn("value");

        DatabaseService service = new DatabaseService(connection);
        List<String> results = service.query();

        assertEquals(1, results.size());
        assertEquals("value", results.get(0));
        verify(statement).executeQuery();
    }
}
```

### File System Operations

```java
@ExtendWith(MockitoExtension.class)
class FileServiceTest {
    @Mock
    private FileReader fileReader;

    @Test
    void testFileRead() throws IOException {
        when(fileReader.read(any(char[].class)))
            .thenAnswer(invocation -> {
                char[] buffer = invocation.getArgument(0);
                "test content".getChars(0, 12, buffer, 0);
                return 12;
            });

        FileService service = new FileService(fileReader);
        String content = service.readFile();

        assertEquals("test content", content);
    }
}
```

### Void Methods with Side Effects

```java
@Test
void testVoidMethod() {
    EmailService emailService = mock(EmailService.class);
    doNothing().when(emailService).sendEmail(anyString());

    NotificationService service = new NotificationService(emailService);
    service.notify("message");

    verify(emailService).sendEmail("message");
}
```

### Exception Handling

```java
@Test
void testExceptionHandling() {
    ExternalService externalService = mock(ExternalService.class);
    when(externalService.call()).thenThrow(new IOException("Network error"));

    MyService service = new MyService(externalService);

    assertThrows(ServiceException.class, () -> service.process());
    verify(externalService).call();
}
```

### Argument Captors

```java
@Test
void testArgumentCapture() {
    EmailService emailService = mock(EmailService.class);
    ArgumentCaptor<Email> emailCaptor = ArgumentCaptor.forClass(Email.class);

    NotificationService service = new NotificationService(emailService);
    service.sendNotification("user@example.com", "Hello");

    verify(emailService).send(emailCaptor.capture());
    Email capturedEmail = emailCaptor.getValue();
    assertEquals("user@example.com", capturedEmail.getTo());
    assertEquals("Hello", capturedEmail.getBody());
}
```

### Spy Objects (Partial Mocking)

```java
@Test
void testPartialMocking() {
    UserService userService = spy(new UserService());
    doReturn(true).when(userService).isValidUser(anyString());

    // Real method calls work normally
    String result = userService.processUser("john");

    // Mocked method returns stubbed value
    assertTrue(userService.isValidUser("john"));
}
```

### Multiple Return Values

```java
@Test
void testMultipleReturnValues() {
    StatusService statusService = mock(StatusService.class);
    when(statusService.getStatus())
        .thenReturn("pending")
        .thenReturn("processing")
        .thenReturn("complete");

    MyService service = new MyService(statusService);
    service.waitForCompletion();

    verify(statusService, times(3)).getStatus();
}
```

### Static Method Mocking (Mockito 3.4+)

```java
@Test
void testStaticMethod() {
    try (MockedStatic<Utility> mockedStatic = mockStatic(Utility.class)) {
        mockedStatic.when(() -> Utility.staticMethod(anyString()))
                    .thenReturn("mocked");

        String result = MyService.process();

        assertEquals("mocked", result);
        mockedStatic.verify(() -> Utility.staticMethod(anyString()));
    }
}
```

### Constructor Mocking

```java
@Test
void testConstructorMocking() {
    try (MockedConstruction<ExternalService> mocked =
         mockConstruction(ExternalService.class,
             (mock, context) -> {
                 when(mock.getData()).thenReturn("mocked data");
             })) {

        MyService service = new MyService();
        String result = service.process();

        assertEquals("mocked data", result);
    }
}
```

## Setup and Teardown

```java
@ExtendWith(MockitoExtension.class)
class ServiceTest {
    @Mock
    private Dependency dependency;

    private ServiceUnderTest service;

    @BeforeEach
    void setUp() {
        service = new ServiceUnderTest(dependency);
    }

    @AfterEach
    void tearDown() {
        // Cleanup if needed
    }

    @Test
    void testMethod() {
        when(dependency.method()).thenReturn("value");
        String result = service.execute();
        assertEquals("value", result);
    }
}
```

## Verification Modes

```java
// Verify exact number of calls
verify(mock, times(3)).method();

// Verify at least/at most
verify(mock, atLeast(1)).method();
verify(mock, atMost(5)).method();

// Verify never called
verify(mock, never()).method();

// Verify no more interactions
verifyNoMoreInteractions(mock);

// Verify order of calls
InOrder inOrder = inOrder(mock1, mock2);
inOrder.verify(mock1).firstMethod();
inOrder.verify(mock2).secondMethod();
```
