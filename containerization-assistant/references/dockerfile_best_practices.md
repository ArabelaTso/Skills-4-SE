# Dockerfile Best Practices

## Multi-Stage Builds

Use multi-stage builds to reduce final image size:

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

**Benefits**:
- Smaller final image (build tools not included)
- Faster deployments
- Reduced attack surface

## Layer Caching Optimization

Order instructions from least to most frequently changing:

```dockerfile
# ✅ Good - Dependencies change less often than code
COPY package*.json ./
RUN npm ci
COPY . .

# ❌ Bad - Cache invalidated on every code change
COPY . .
RUN npm ci
```

## Security Best Practices

### 1. Use Non-Root Users

```dockerfile
# Create and use non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs

USER nodejs
```

### 2. Use Specific Base Image Tags

```dockerfile
# ✅ Good - Specific version
FROM node:18.17.0-alpine

# ❌ Bad - Latest tag (unpredictable)
FROM node:latest
```

### 3. Scan for Vulnerabilities

```bash
docker scan myapp:latest
```

### 4. Use .dockerignore

```.dockerignore
node_modules
npm-debug.log
.git
.env
.DS_Store
*.md
```

## Image Size Optimization

### 1. Use Alpine Images

```dockerfile
FROM node:18-alpine  # ~170MB
# vs
FROM node:18         # ~900MB
```

### 2. Clean Up in Same Layer

```dockerfile
RUN apt-get update && \
    apt-get install -y package && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### 3. Use .dockerignore

Exclude unnecessary files from build context.

## Health Checks

Define health checks for container monitoring:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

## Environment Variables

Use ARG for build-time variables, ENV for runtime:

```dockerfile
# Build-time variable
ARG NODE_VERSION=18

# Runtime variable
ENV NODE_ENV=production
```

## Common Patterns by Language

### Node.js

```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app .
USER node
EXPOSE 3000
CMD ["node", "index.js"]
```

### Python

```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

### Java (Spring Boot)

```dockerfile
FROM eclipse-temurin:17-jdk AS builder
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN ./mvnw package -DskipTests

FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Go

```dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o main .

FROM alpine:latest
RUN apk --no-cache add ca-certificates
COPY --from=builder /app/main .
CMD ["./main"]
```

## Build Arguments

Use build arguments for flexibility:

```dockerfile
ARG APP_VERSION=latest
ARG BUILD_DATE
ARG VCS_REF

LABEL org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${VCS_REF}"
```

Build with arguments:

```bash
docker build \
  --build-arg APP_VERSION=1.0.0 \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
  --build-arg VCS_REF=$(git rev-parse --short HEAD) \
  -t myapp:1.0.0 .
```

## Metadata Labels

Add metadata using labels:

```dockerfile
LABEL maintainer="team@example.com" \
      version="1.0.0" \
      description="My application"
```

## Volume Management

Define volumes for persistent data:

```dockerfile
VOLUME ["/app/data", "/app/logs"]
```

## Networking

Expose ports:

```dockerfile
EXPOSE 8080 8443
```

## Entrypoint vs CMD

**ENTRYPOINT**: Defines the executable

```dockerfile
ENTRYPOINT ["python", "app.py"]
```

**CMD**: Provides default arguments

```dockerfile
CMD ["--host", "0.0.0.0"]
```

**Combined**:

```dockerfile
ENTRYPOINT ["python", "app.py"]
CMD ["--host", "0.0.0.0"]
```

Override CMD at runtime:

```bash
docker run myapp --host 127.0.0.1
```

## Development vs Production

### Development Dockerfile

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install  # Install all deps including dev
COPY . .
CMD ["npm", "run", "dev"]
```

### Production Dockerfile

```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production  # Only production deps
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
CMD ["node", "dist/index.js"]
```

## Troubleshooting

### Build fails with permission error

```dockerfile
# Ensure correct ownership
RUN chown -R appuser:appuser /app
USER appuser
```

### Image too large

- Use multi-stage builds
- Use Alpine base images
- Clean up in same RUN layer
- Use .dockerignore

### Container exits immediately

- Check CMD/ENTRYPOINT
- Verify application starts correctly
- Check logs: `docker logs <container>`

### Cannot connect to container

- Verify EXPOSE matches application port
- Check port mapping: `-p 3000:3000`
- Verify application binds to `0.0.0.0`, not `localhost`
