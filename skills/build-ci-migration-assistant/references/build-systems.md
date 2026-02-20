# Build System Migrations

## Maven to Gradle

### Basic Structure Mapping

**Maven (pom.xml):**
```xml
<project>
    <groupId>com.example</groupId>
    <artifactId>myapp</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
</project>
```

**Gradle (build.gradle):**
```groovy
group = 'com.example'
version = '1.0.0'

plugins {
    id 'java'
}
```

### Dependencies

**Maven:**
```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
        <version>2.7.0</version>
    </dependency>
    <dependency>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <version>4.13.2</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

**Gradle:**
```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web:2.7.0'
    testImplementation 'junit:junit:4.13.2'
}
```

### Repositories

**Maven:**
```xml
<repositories>
    <repository>
        <id>central</id>
        <url>https://repo.maven.apache.org/maven2</url>
    </repository>
</repositories>
```

**Gradle:**
```groovy
repositories {
    mavenCentral()
}
```

### Build Configuration

**Maven:**
```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.8.1</version>
            <configuration>
                <source>11</source>
                <target>11</target>
            </configuration>
        </plugin>
    </plugins>
</build>
```

**Gradle:**
```groovy
java {
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
}
```

## Gradle to Maven

### Reverse Mapping

**Gradle:**
```groovy
plugins {
    id 'java'
    id 'application'
}

application {
    mainClass = 'com.example.Main'
}
```

**Maven:**
```xml
<packaging>jar</packaging>
<build>
    <plugins>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>exec-maven-plugin</artifactId>
            <configuration>
                <mainClass>com.example.Main</mainClass>
            </configuration>
        </plugin>
    </plugins>
</build>
```

## npm to Yarn

### Package Management

**npm (package.json):**
```json
{
  "name": "myapp",
  "version": "1.0.0",
  "scripts": {
    "start": "node index.js",
    "test": "jest",
    "build": "webpack"
  },
  "dependencies": {
    "express": "^4.18.0"
  },
  "devDependencies": {
    "jest": "^28.0.0"
  }
}
```

**Yarn (same package.json, different lock file):**
- package.json remains the same
- yarn.lock replaces package-lock.json
- Commands change: `npm install` → `yarn install`

### Command Mapping

| npm | Yarn |
|-----|------|
| npm install | yarn install |
| npm install [package] | yarn add [package] |
| npm install --save-dev [package] | yarn add --dev [package] |
| npm uninstall [package] | yarn remove [package] |
| npm run [script] | yarn [script] |
| npm test | yarn test |

## Make to CMake

### Basic Makefile

**Makefile:**
```makefile
CC = gcc
CFLAGS = -Wall -O2
TARGET = myapp

SRCS = main.c utils.c
OBJS = $(SRCS:.c=.o)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)
```

**CMakeLists.txt:**
```cmake
cmake_minimum_required(VERSION 3.10)
project(myapp)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -O2")

add_executable(myapp main.c utils.c)
```

### Build Commands

**Make:**
```bash
make
make clean
```

**CMake:**
```bash
mkdir build && cd build
cmake ..
make
```

## Common Patterns

### Multi-Module Projects

**Maven:**
```xml
<modules>
    <module>core</module>
    <module>api</module>
    <module>web</module>
</modules>
```

**Gradle:**
```groovy
// settings.gradle
include 'core', 'api', 'web'
```

### Custom Tasks

**Maven:**
```xml
<plugin>
    <groupId>org.codehaus.mojo</groupId>
    <artifactId>exec-maven-plugin</artifactId>
    <executions>
        <execution>
            <id>custom-task</id>
            <phase>package</phase>
            <goals>
                <goal>exec</goal>
            </goals>
            <configuration>
                <executable>./custom-script.sh</executable>
            </configuration>
        </execution>
    </executions>
</plugin>
```

**Gradle:**
```groovy
task customTask(type: Exec) {
    commandLine './custom-script.sh'
}

build.dependsOn customTask
```

### Properties/Variables

**Maven:**
```xml
<properties>
    <java.version>11</java.version>
    <spring.version>5.3.0</spring.version>
</properties>

<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-core</artifactId>
    <version>${spring.version}</version>
</dependency>
```

**Gradle:**
```groovy
ext {
    javaVersion = '11'
    springVersion = '5.3.0'
}

dependencies {
    implementation "org.springframework:spring-core:${springVersion}"
}
```

## Migration Checklist

### Maven to Gradle

- [ ] Convert pom.xml to build.gradle
- [ ] Map dependencies with correct scopes
- [ ] Convert plugins to Gradle equivalents
- [ ] Migrate custom tasks
- [ ] Update build commands in documentation
- [ ] Test build and all tasks
- [ ] Verify artifact generation

### Gradle to Maven

- [ ] Convert build.gradle to pom.xml
- [ ] Map dependencies with correct scopes
- [ ] Convert Gradle plugins to Maven plugins
- [ ] Migrate custom tasks
- [ ] Update build commands
- [ ] Test build lifecycle
- [ ] Verify packaging

### npm to Yarn

- [ ] Keep package.json unchanged
- [ ] Generate yarn.lock
- [ ] Update CI/CD scripts
- [ ] Update documentation
- [ ] Test all scripts
- [ ] Verify dependencies resolve correctly

## Common Issues

### Dependency Scope Mapping

| Maven | Gradle |
|-------|--------|
| compile | implementation |
| provided | compileOnly |
| runtime | runtimeOnly |
| test | testImplementation |

### Plugin Equivalents

| Maven Plugin | Gradle Plugin |
|--------------|---------------|
| maven-compiler-plugin | java plugin |
| maven-surefire-plugin | test task |
| maven-jar-plugin | jar task |
| maven-assembly-plugin | application plugin |
