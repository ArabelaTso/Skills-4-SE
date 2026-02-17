# Spring MVC to Spring Boot Migration Guide

## Overview

This guide provides detailed instructions for migrating Spring MVC applications to Spring Boot, covering all aspects from build configuration to testing.

## Pre-Migration Checklist

Before starting migration:

- [ ] Backup your code (create git branch)
- [ ] Document current application structure
- [ ] List all external dependencies
- [ ] Note custom configurations
- [ ] Identify integration points
- [ ] Review current Spring version
- [ ] Check Java version compatibility

## Migration Process

### Phase 1: Build Configuration

#### Maven Migration

**Step 1: Add Spring Boot Parent**

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>
    <relativePath/>
</parent>
```

**Step 2: Replace Dependencies**

Remove individual Spring dependencies:
```xml
<!-- Remove these -->
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-webmvc</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-context</artifactId>
</dependency>
```

Add Spring Boot starters:
```xml
<!-- Add these -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
```

**Step 3: Add Spring Boot Maven Plugin**

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
        </plugin>
    </plugins>
</build>
```

#### Gradle Migration

**Step 1: Add Spring Boot Plugin**

```gradle
plugins {
    id 'org.springframework.boot' version '3.2.0'
    id 'io.spring.dependency-management' version '1.1.4'
    id 'java'
}
```

**Step 2: Replace Dependencies**

```gradle
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
}
```

### Phase 2: Application Structure

#### Create Main Application Class

Create `Application.java` in your base package:

```java
package com.example.myapp;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

#### Update Package Structure

Recommended structure:
```
src/main/java/com/example/myapp/
├── Application.java
├── controller/
│   └── UserController.java
├── service/
│   └── UserService.java
├── repository/
│   └── UserRepository.java
├── model/
│   └── User.java
└── config/
    └── WebConfig.java
```

### Phase 3: Configuration Migration

#### XML to Java Configuration

**Before (XML):**
```xml
<beans>
    <context:component-scan base-package="com.example"/>
    <mvc:annotation-driven/>

    <bean id="dataSource" class="...">
        <property name="url" value="jdbc:mysql://localhost:3306/mydb"/>
    </bean>
</beans>
```

**After (Java + Properties):**

```java
@Configuration
public class DatabaseConfig {
    // Most configuration is auto-configured
    // Only add custom beans if needed
}
```

```properties
# application.properties
spring.datasource.url=jdbc:mysql://localhost:3306/mydb
spring.datasource.username=root
spring.datasource.password=password
```

#### web.xml Migration

Spring Boot doesn't use `web.xml`. Configuration is done through:

1. **Application properties**
2. **Java configuration classes**
3. **Annotations**

**Before (web.xml):**
```xml
<servlet>
    <servlet-name>dispatcher</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    <init-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>/WEB-INF/spring-config.xml</param-value>
    </init-param>
</servlet>
<servlet-mapping>
    <servlet-name>dispatcher</servlet-name>
    <url-pattern>/</url-pattern>
</servlet-mapping>
```

**After:** Not needed - Spring Boot auto-configures DispatcherServlet

### Phase 4: Controller Migration

#### Update Annotations

**Before:**
```java
@Controller
@RequestMapping("/users")
public class UserController {

    @RequestMapping(method = RequestMethod.GET)
    @ResponseBody
    public List<User> getUsers() {
        return userService.findAll();
    }

    @RequestMapping(value = "/{id}", method = RequestMethod.POST)
    @ResponseBody
    public User createUser(@RequestBody User user) {
        return userService.save(user);
    }
}
```

**After:**
```java
@RestController
@RequestMapping("/users")
public class UserController {

    @GetMapping
    public List<User> getUsers() {
        return userService.findAll();
    }

    @PostMapping("/{id}")
    public User createUser(@RequestBody User user) {
        return userService.save(user);
    }
}
```

**Key Changes:**
- `@Controller` + `@ResponseBody` → `@RestController`
- `@RequestMapping(method = RequestMethod.GET)` → `@GetMapping`
- `@RequestMapping(method = RequestMethod.POST)` → `@PostMapping`
- Similar for `@PutMapping`, `@DeleteMapping`, `@PatchMapping`

### Phase 5: Service Layer

Service layer typically requires minimal changes:

```java
@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    public List<User> findAll() {
        return userRepository.findAll();
    }

    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));
    }
}
```

### Phase 6: Data Access Layer

#### JPA/Hibernate Configuration

**Before (XML):**
```xml
<bean id="entityManagerFactory" class="...">
    <property name="dataSource" ref="dataSource"/>
    <property name="packagesToScan" value="com.example.model"/>
</bean>
```

**After (Properties):**
```properties
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL8Dialect
```

#### Repository Layer

Spring Data JPA works the same:

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByLastName(String lastName);
}
```

### Phase 7: Test Migration

#### Update Test Annotations

**Before:**
```java
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(classes = WebConfig.class)
@WebAppConfiguration
public class UserControllerTest {

    @Autowired
    private WebApplicationContext context;

    private MockMvc mockMvc;

    @Before
    public void setup() {
        mockMvc = MockMvcBuilders
            .webAppContextSetup(context)
            .build();
    }
}
```

**After:**
```java
@SpringBootTest
@AutoConfigureMockMvc
public class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    public void testGetUsers() throws Exception {
        mockMvc.perform(get("/users"))
            .andExpect(status().isOk());
    }
}
```

**Key Changes:**
- `@RunWith(SpringJUnit4ClassRunner.class)` → Not needed (JUnit 5)
- `@ContextConfiguration` → `@SpringBootTest`
- Manual MockMvc setup → `@AutoConfigureMockMvc`
- `@Before` → `@BeforeEach`
- `@Test` from `org.junit.Test` → `org.junit.jupiter.api.Test`

### Phase 8: Properties Configuration

Create `src/main/resources/application.properties`:

```properties
# Server Configuration
server.port=8080
server.servlet.context-path=/myapp

# Logging
logging.level.root=INFO
logging.level.com.example=DEBUG

# Database
spring.datasource.url=jdbc:mysql://localhost:3306/mydb
spring.datasource.username=root
spring.datasource.password=password

# JPA
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true

# View Resolver (if using JSP)
spring.mvc.view.prefix=/WEB-INF/views/
spring.mvc.view.suffix=.jsp
```

## Common Migration Patterns

### Pattern 1: Exception Handling

**Before:**
```java
@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(Exception.class)
    public ModelAndView handleException(Exception ex) {
        ModelAndView mav = new ModelAndView("error");
        mav.addObject("message", ex.getMessage());
        return mav;
    }
}
```

**After (REST API):**
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {
        ErrorResponse error = new ErrorResponse(
            HttpStatus.NOT_FOUND.value(),
            ex.getMessage()
        );
        return new ResponseEntity<>(error, HttpStatus.NOT_FOUND);
    }
}
```

### Pattern 2: Interceptors

**Before:**
```java
@Configuration
@EnableWebMvc
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new LoggingInterceptor());
    }
}
```

**After:** Same pattern works in Spring Boot

### Pattern 3: CORS Configuration

**Before:**
```java
@Configuration
@EnableWebMvc
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
            .allowedOrigins("http://localhost:3000");
    }
}
```

**After:** Same pattern or use properties:
```properties
spring.web.cors.allowed-origins=http://localhost:3000
spring.web.cors.allowed-methods=GET,POST,PUT,DELETE
```

## Post-Migration Steps

1. **Build the application**
   ```bash
   mvn clean package
   ```

2. **Run the application**
   ```bash
   java -jar target/myapp.jar
   # or
   mvn spring-boot:run
   ```

3. **Test endpoints**
   ```bash
   curl http://localhost:8080/users
   ```

4. **Run tests**
   ```bash
   mvn test
   ```

5. **Check actuator endpoints** (if enabled)
   ```bash
   curl http://localhost:8080/actuator/health
   ```

## Troubleshooting

### Issue: Application won't start

**Solution:** Check for:
- Missing `@SpringBootApplication` annotation
- Incorrect package structure
- Conflicting dependencies

### Issue: Controllers not found

**Solution:** Ensure:
- Controllers are in same package or sub-package as Application class
- `@ComponentScan` is not restricting scan

### Issue: Database connection fails

**Solution:** Verify:
- Database URL in application.properties
- Database driver dependency
- Database is running

### Issue: Tests fail

**Solution:** Update:
- JUnit 4 to JUnit 5
- Test annotations
- MockMvc setup

## Best Practices

1. **Migrate incrementally** - One module at a time
2. **Keep tests passing** - Run tests after each change
3. **Use Spring Boot starters** - Don't mix with individual dependencies
4. **Leverage auto-configuration** - Minimize custom configuration
5. **Use application.properties** - Externalize configuration
6. **Enable Actuator** - For production monitoring
7. **Follow conventions** - Use standard package structure

## Next Steps

After successful migration:

1. Enable Spring Boot Actuator for monitoring
2. Add Spring Boot DevTools for development
3. Configure profiles for different environments
4. Set up logging configuration
5. Add API documentation (Swagger/OpenAPI)
6. Configure security (Spring Security)
7. Optimize for production deployment
