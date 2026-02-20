# Docker and Docker Compose Rollback Guides

Platform-specific procedures and best practices for Docker deployments.

## Table of Contents

1. [Docker Container Rollback](#docker-container-rollback)
2. [Docker Compose Rollback](#docker-compose-rollback)
3. [Volume and Data Management](#volume-and-data-management)
4. [Network Rollback](#network-rollback)
5. [Multi-Container Coordination](#multi-container-coordination)

---

## Docker Container Rollback

### Basic Container Rollback

**Scenario:** Single container needs rollback to previous version

```bash
# 1. List available images
docker images | grep myapp
# myapp    v1.2.4    abc123    2 hours ago    500MB
# myapp    v1.2.3    def456    1 day ago      498MB
# myapp    v1.2.2    ghi789    2 days ago     495MB

# 2. Stop current container
docker stop myapp-container

# 3. Remove current container (preserves volumes if using named volumes)
docker rm myapp-container

# 4. Start container with previous image
docker run -d \
  --name myapp-container \
  --network myapp-network \
  -p 8080:8080 \
  -v myapp-data:/data \
  myapp:v1.2.3

# 5. Validate
docker ps | grep myapp
docker logs myapp-container --tail 50
```

### Rollback Without Downtime (Blue-Green Pattern)

Run old and new versions simultaneously, switch traffic:

```bash
# Current state: v1.2.4 running on port 8080

# 1. Start old version on different port
docker run -d \
  --name myapp-v1.2.3 \
  --network myapp-network \
  -p 8081:8080 \
  myapp:v1.2.3

# 2. Validate old version works
curl http://localhost:8081/health

# 3. Update load balancer/reverse proxy to point to port 8081
# (nginx config change, docker network alias, etc.)

# 4. Stop new version
docker stop myapp-container
docker rm myapp-container

# 5. Rename old version to standard name
docker rename myapp-v1.2.3 myapp-container

# 6. Remap to standard port (if needed)
docker stop myapp-container
docker run -d \
  --name myapp-container \
  --network myapp-network \
  -p 8080:8080 \
  myapp:v1.2.3
```

### Container Rollback with Volume Preservation

Ensure data persists across rollback:

```bash
# 1. Identify volumes in use
docker inspect myapp-container | grep -A 10 Mounts

# 2. Stop and remove container (volumes persist)
docker stop myapp-container
docker rm myapp-container

# 3. Start with previous image, same volumes
docker run -d \
  --name myapp-container \
  --network myapp-network \
  -p 8080:8080 \
  -v myapp-data:/data \
  -v myapp-config:/etc/myapp \
  myapp:v1.2.3

# 4. Verify volume data intact
docker exec myapp-container ls -la /data
```

---

## Docker Compose Rollback

### Full Stack Rollback

Rollback entire docker-compose application:

```bash
# 1. Backup current compose file
cp docker-compose.yml docker-compose.yml.backup

# 2. Restore previous compose file from git
git checkout HEAD~1 -- docker-compose.yml

# 3. Stop current services
docker-compose down

# 4. Start with previous configuration
docker-compose up -d

# 5. Validate all services
docker-compose ps
docker-compose logs --tail 50
```

### Selective Service Rollback

Rollback specific service within compose stack:

```bash
# Current docker-compose.yml:
# services:
#   app:
#     image: myapp:v1.2.4
#   db:
#     image: postgres:14

# 1. Update only app service image version
sed -i 's/myapp:v1.2.4/myapp:v1.2.3/g' docker-compose.yml

# 2. Recreate only app service
docker-compose up -d --no-deps app

# 3. Validate
docker-compose ps app
docker-compose logs app --tail 50

# --no-deps prevents recreating linked services (db stays running)
```

### Rollback with Environment Changes

Revert environment variables or config:

```bash
# 1. Restore previous .env file
git checkout HEAD~1 -- .env

# 2. Recreate services to pick up new env vars
docker-compose up -d --force-recreate

# Alternative: Update specific env var inline
docker-compose up -d \
  -e APP_VERSION=v1.2.3 \
  -e FEATURE_FLAG=false \
  app
```

### Pinned Version Rollback

If using image tags in compose file:

```yaml
# docker-compose.yml
services:
  app:
    image: myapp:v1.2.4  # Change to v1.2.3
    ports:
      - "8080:8080"

  db:
    image: postgres:14
    volumes:
      - db-data:/var/lib/postgresql/data
```

```bash
# 1. Edit docker-compose.yml to change image tag
sed -i 's/myapp:v1.2.4/myapp:v1.2.3/g' docker-compose.yml

# 2. Pull previous image (if not cached)
docker-compose pull app

# 3. Recreate app service
docker-compose up -d app

# 4. Validate
docker-compose logs app --tail 50
```

### Build-Based Rollback

If building from Dockerfile:

```yaml
# docker-compose.yml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
```

```bash
# 1. Checkout previous source code
git checkout HEAD~1

# 2. Rebuild and restart
docker-compose build app
docker-compose up -d app

# Or rebuild from specific git commit
git checkout abc123
docker-compose build app
docker-compose up -d app
```

---

## Volume and Data Management

### Volume Rollback Strategies

#### Strategy 1: Volume Snapshots (Manual Backup)

```bash
# Before risky changes, backup volume data
# 1. Stop services using volume
docker-compose stop app

# 2. Create backup
docker run --rm \
  -v myapp-data:/source \
  -v $(pwd)/backups:/backup \
  alpine \
  tar czf /backup/myapp-data-$(date +%Y%m%d_%H%M%S).tar.gz -C /source .

# 3. Restart services
docker-compose up -d app

# To restore:
# 1. Stop services
docker-compose stop app

# 2. Restore from backup
docker run --rm \
  -v myapp-data:/target \
  -v $(pwd)/backups:/backup \
  alpine \
  sh -c "rm -rf /target/* && tar xzf /backup/myapp-data-20260215_120000.tar.gz -C /target"

# 3. Start services
docker-compose up -d app
```

#### Strategy 2: Volume Cloning

```bash
# Clone volume before changes
# 1. Create new volume
docker volume create myapp-data-backup

# 2. Copy data to backup volume
docker run --rm \
  -v myapp-data:/source:ro \
  -v myapp-data-backup:/target \
  alpine \
  sh -c "cp -a /source/. /target/"

# If rollback needed:
# 1. Stop services
docker-compose stop app

# 2. Remove current volume
docker volume rm myapp-data

# 3. Clone backup back
docker volume create myapp-data
docker run --rm \
  -v myapp-data-backup:/source:ro \
  -v myapp-data:/target \
  alpine \
  sh -c "cp -a /source/. /target/"

# 4. Restart services
docker-compose up -d app
```

#### Strategy 3: Bind Mounts for Easy Backup

Use bind mounts for critical data:

```yaml
# docker-compose.yml
services:
  app:
    volumes:
      - ./data:/app/data  # Bind mount for easy backup
```

```bash
# Rollback bind mount data
# 1. Stop services
docker-compose stop app

# 2. Restore from git or backup
cp -r data.backup/* data/
# or
git checkout HEAD~1 -- data/

# 3. Restart
docker-compose up -d app
```

---

## Network Rollback

### Network Configuration Changes

Rollback network settings:

```bash
# Current state: Using custom network with specific subnet

# 1. List current networks
docker network ls
docker network inspect myapp-network

# 2. Stop services
docker-compose down

# 3. Remove current network
docker network rm myapp-network

# 4. Recreate previous network configuration
docker network create \
  --driver bridge \
  --subnet 172.20.0.0/16 \
  --gateway 172.20.0.1 \
  myapp-network

# 5. Restart services
docker-compose up -d

# Services will reconnect to recreated network
```

### Service Discovery Rollback

If using Docker DNS for service discovery:

```yaml
# docker-compose.yml
services:
  app:
    networks:
      default:
        aliases:
          - api-server  # Changed alias

  db:
    networks:
      default:
        aliases:
          - database
```

```bash
# Rollback network aliases
# 1. Restore previous docker-compose.yml
git checkout HEAD~1 -- docker-compose.yml

# 2. Recreate services with old aliases
docker-compose down
docker-compose up -d

# DNS names revert to previous configuration
```

---

## Multi-Container Coordination

### Coordinated Rollback (Database + Application)

Critical: Rollback in correct order:

```bash
# Scenario: App v1.2.4 + Database migration applied
# Need to rollback both

# 1. Stop application (prevent new requests)
docker-compose stop app

# 2. Rollback database migration
docker exec myapp-db alembic downgrade -1

# 3. Verify schema rollback
docker exec myapp-db psql -U user -d dbname -c "\d users"

# 4. Rollback application
sed -i 's/myapp:v1.2.4/myapp:v1.2.3/g' docker-compose.yml
docker-compose up -d app

# 5. Validate stack
docker-compose ps
docker-compose logs app --tail 50
docker-compose logs db --tail 50
```

### Dependency-Aware Rollback

When services have dependencies:

```yaml
# docker-compose.yml
services:
  app:
    depends_on:
      - db
      - cache
    image: myapp:v1.2.4

  db:
    image: postgres:14

  cache:
    image: redis:7
```

```bash
# Rollback with dependency awareness

# 1. Identify dependency graph
# app depends on db, cache
# db and cache are independent

# 2. Rollback in reverse dependency order:
# First: app (depends on others)
docker-compose stop app
sed -i 's/myapp:v1.2.4/myapp:v1.2.3/g' docker-compose.yml
docker-compose up -d app

# Then: db and cache (if needed)
# Usually not needed unless they changed too

# 3. Validate
docker-compose ps
```

### Health Check Integration

Use health checks to validate rollback:

```yaml
# docker-compose.yml
services:
  app:
    image: myapp:v1.2.3
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 30s
```

```bash
# After rollback, wait for health check
docker-compose up -d app

# Monitor health status
watch docker-compose ps

# app service should show "healthy" status
# If not healthy after start_period, rollback failed
```

---

## Automated Rollback Scripts

### Quick Rollback Script

```bash
#!/bin/bash
# quick-rollback.sh - Rollback to previous version

set -e

SERVICE_NAME=${1:-app}
PREVIOUS_VERSION=${2}

if [ -z "$PREVIOUS_VERSION" ]; then
  echo "Usage: ./quick-rollback.sh <service-name> <previous-version>"
  echo "Example: ./quick-rollback.sh app v1.2.3"
  exit 1
fi

echo "Rolling back $SERVICE_NAME to $PREVIOUS_VERSION..."

# Stop service
docker-compose stop "$SERVICE_NAME"

# Update compose file
sed -i "s/${SERVICE_NAME}:.*/${SERVICE_NAME}:${PREVIOUS_VERSION}/g" docker-compose.yml

# Restart service
docker-compose up -d "$SERVICE_NAME"

# Show status
docker-compose ps "$SERVICE_NAME"
docker-compose logs "$SERVICE_NAME" --tail 20

echo "Rollback complete. Monitor logs: docker-compose logs -f $SERVICE_NAME"
```

### Safe Rollback with Validation

```bash
#!/bin/bash
# safe-rollback.sh - Rollback with health checks

set -e

SERVICE_NAME=${1:-app}
PREVIOUS_VERSION=${2}
HEALTH_ENDPOINT=${3:-http://localhost:8080/health}

# Backup current state
docker-compose config > docker-compose-backup-$(date +%Y%m%d_%H%M%S).yml

# Rollback
docker-compose stop "$SERVICE_NAME"
sed -i "s/${SERVICE_NAME}:.*/${SERVICE_NAME}:${PREVIOUS_VERSION}/g" docker-compose.yml
docker-compose up -d "$SERVICE_NAME"

# Wait for service to start
echo "Waiting for service to start..."
sleep 10

# Health check
for i in {1..30}; do
  if curl -sf "$HEALTH_ENDPOINT" > /dev/null; then
    echo "✓ Service healthy"
    docker-compose ps "$SERVICE_NAME"
    exit 0
  fi
  echo "Waiting for health check... ($i/30)"
  sleep 2
done

echo "✗ Health check failed after rollback"
echo "Service logs:"
docker-compose logs "$SERVICE_NAME" --tail 50
exit 1
```

---

## Best Practices

1. **Tag images with versions** - Use semantic versioning or git SHAs
2. **Keep previous images** - Don't prune immediately after deploy
3. **Use named volumes** - Easier to backup and restore than anonymous volumes
4. **Pin image versions** - Don't use `latest` in production
5. **Test compose files** - `docker-compose config` validates syntax
6. **Health checks are critical** - Define healthchecks for all services
7. **Backup before changes** - Especially volumes with critical data
8. **Document dependencies** - Track which services depend on others
9. **Use .env files** - Easier to version and rollback environment vars
10. **Practice rollbacks** - Regular drills ensure procedures work
