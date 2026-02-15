# Multi-stage Go Dockerfile
# Optimized for minimal image size

FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

# Build binary
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Production stage - minimal scratch image
FROM alpine:latest

RUN apk --no-cache add ca-certificates

WORKDIR /root/

# Create non-root user
RUN addgroup -g 1001 -S appuser && \
    adduser -S appuser -u 1001 -G appuser

# Copy binary from builder
COPY --from=builder /app/main .

# Change ownership
RUN chown appuser:appuser main

USER appuser

EXPOSE 8080

CMD ["./main"]
