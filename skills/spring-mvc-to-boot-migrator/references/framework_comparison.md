# Spring MVC vs Spring Boot Comparison

## Architecture Overview

| Aspect | Spring MVC | Spring Boot |
|--------|------------|-------------|
| **Configuration** | XML or Java config | Auto-configuration |
| **Deployment** | External server (Tomcat, etc.) | Embedded server |
| **Dependency Management** | Manual | Starter dependencies |
| **Setup Time** | Hours | Minutes |
| **Boilerplate Code** | High | Minimal |
| **Production Ready** | Requires setup | Built-in features |

## Configuration Comparison

### Application Setup

**Spring MVC (web.xml):**
```xml
<web-app>
    <servlet>
        <servlet-name>dispatcher</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>/WEB-INF/spring-mvc-config.xml</param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>
    <servlet-mapping>
        <servlet-name>dispatcher</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
</web-app>
```

**Spring Boot:**
```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### Dependency Management

**Spring MVC (pom.xml):**
```xml
<dependencies>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-webmvc</artifactId>
        <version>5.3.20</version>
    </dependency>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-context</artifactId>
        <version>5.3.20</version>
    </dependency>
    <!-- Many more dependencies... -->
</dependencies>
```

**Spring Boot (pom.xml):**
```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>
</parent>

<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
</dependencies>
```

## Controller Comparison

### Basic Controller

**Spring MVC:**
```java
@Controller
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserService userService;

    @RequestMapping(method = RequestMethod.GET)
    @ResponseBody
    public List<User> getUsers() {
        return userService.findAll();
    }

    @RequestMapping(value = "/{id}", method = RequestMethod.GET)
    @ResponseBody
    public User getUser(@PathVariable Long id) {
        return userService.findById(id);
    }
}
```

**Spring Boot:**
```java
@RestController
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserService userService;

    @GetMapping
    public List<User> getUsers() {
        return userService.findAll();
    }

    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.findById(id);
    }
}
```

## Configuration Classes

### Bean Configuration

**Spring MVC (XML):**
```xml
<beans>
    <context:component-scan base-package="com.example"/>

    <bean id="dataSource" class="org.apache.commons.dbcp2.BasicDataSource">
        <property name="driverClassName" value="com.mysql.jdbc.Driver"/>
        <property name="url" value="jdbc:mysql://localhost:3306/mydb"/>
        <property name="username" value="root"/>
        <property name="password" value="password"/>
    </bean>

    <bean id="viewResolver"
          class="org.springframework.web.servlet.view.InternalResourceViewResolver">
        <property name="prefix" value="/WEB-INF/views/"/>
        <property name="suffix" value=".jsp"/>
    </bean>
</beans>
```

**Spring MVC (Java Config):**
```java
@Configuration
@EnableWebMvc
@ComponentScan(basePackages = "com.example")
public class WebConfig implements WebMvcConfigurer {

    @Bean
    public DataSource dataSource() {
        BasicDataSource dataSource = new BasicDataSource();
        dataSource.setDriverClassName("com.mysql.jdbc.Driver");
        dataSource.setUrl("jdbc:mysql://localhost:3306/mydb");
        dataSource.setUsername("root");
        dataSource.setPassword("password");
        return dataSource;
    }

    @Bean
    public ViewResolver viewResolver() {
        InternalResourceViewResolver resolver = new InternalResourceViewResolver();
        resolver.setPrefix("/WEB-INF/views/");
        resolver.setSuffix(".jsp");
        return resolver;
    }
}
```

**Spring Boot:**
```java
@Configuration
public class WebConfig {
    // Most configuration is auto-configured
    // Only customize what you need

    @Bean
    public DataSource dataSource() {
        // Or use application.properties:
        // spring.datasource.url=jdbc:mysql://localhost:3306/mydb
        // spring.datasource.username=root
        // spring.datasource.password=password
        return DataSourceBuilder.create().build();
    }
}
```

**Spring Boot (application.properties):**
```properties
# Database
spring.datasource.url=jdbc:mysql://localhost:3306/mydb
spring.datasource.username=root
spring.datasource.password=password

# View Resolver
spring.mvc.view.prefix=/WEB-INF/views/
spring.mvc.view.suffix=.jsp

# Server
server.port=8080
```

## Testing Comparison

### Controller Tests

**Spring MVC:**
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

    @Test
    public void testGetUsers() throws Exception {
        mockMvc.perform(get("/users"))
            .andExpect(status().isOk())
            .andExpect(content().contentType(MediaType.APPLICATION_JSON));
    }
}
```

**Spring Boot:**
```java
@SpringBootTest
@AutoConfigureMockMvc
public class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    public void testGetUsers() throws Exception {
        mockMvc.perform(get("/users"))
            .andExpect(status().isOk())
            .andExpect(content().contentType(MediaType.APPLICATION_JSON));
    }
}
```

## Deployment Comparison

### Packaging

**Spring MVC:**
- Package as WAR file
- Deploy to external Tomcat/Jetty
- Requires server configuration
- Separate server management

**Spring Boot:**
- Package as JAR file (executable)
- Embedded Tomcat/Jetty/Undertow
- Run with `java -jar app.jar`
- Self-contained application

### Running the Application

**Spring MVC:**
```bash
# Build WAR
mvn clean package

# Deploy to Tomcat
cp target/myapp.war $TOMCAT_HOME/webapps/

# Start Tomcat
$TOMCAT_HOME/bin/startup.sh
```

**Spring Boot:**
```bash
# Build JAR
mvn clean package

# Run directly
java -jar target/myapp.jar

# Or use Maven plugin
mvn spring-boot:run
```

## Key Differences Summary

### 1. Auto-Configuration
- **Spring MVC**: Manual configuration required
- **Spring Boot**: Automatic configuration based on classpath

### 2. Embedded Server
- **Spring MVC**: Requires external server
- **Spring Boot**: Embedded server included

### 3. Starter Dependencies
- **Spring MVC**: Individual dependencies
- **Spring Boot**: Grouped starter dependencies

### 4. Production Features
- **Spring MVC**: Manual setup for monitoring, health checks
- **Spring Boot**: Built-in Actuator for production features

### 5. Development Experience
- **Spring MVC**: More boilerplate, longer setup
- **Spring Boot**: Convention over configuration, rapid development

## Migration Benefits

1. **Reduced Configuration**: 80% less configuration code
2. **Faster Development**: Quick project setup and development
3. **Production Ready**: Built-in monitoring and health checks
4. **Modern Standards**: Latest Spring features and best practices
5. **Easier Deployment**: Self-contained executable JARs
6. **Better Testing**: Simplified test configuration
7. **Microservices Ready**: Perfect for microservices architecture

## When to Migrate

Migrate from Spring MVC to Spring Boot when:
- Starting new features or major refactoring
- Need faster development cycles
- Want to adopt microservices
- Require production monitoring
- Simplifying deployment process
- Updating to latest Spring versions
