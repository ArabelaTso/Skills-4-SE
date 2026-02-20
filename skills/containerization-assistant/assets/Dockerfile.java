# Multi-stage Java Dockerfile
# Optimized for Spring Boot applications

FROM eclipse-temurin:17-jdk-alpine AS builder

WORKDIR /app

# Copy Maven/Gradle files
COPY pom.xml .
# COPY build.gradle settings.gradle ./  # For Gradle

# Copy source code
COPY src ./src

# Build application (Maven example)
RUN ./mvnw clean package -DskipTests
# RUN ./gradlew build -x test  # For Gradle

# Production stage
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S spring && \
    adduser -S spring -u 1001 -G spring

# Copy JAR from builder
COPY --from=builder /app/target/*.jar app.jar

# Change ownership
RUN chown spring:spring app.jar

USER spring

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
