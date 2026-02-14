# Database Rollback Patterns

Detailed strategies for rolling back database migrations safely and preserving data.

## Table of Contents

1. [Migration Rollback Fundamentals](#migration-rollback-fundamentals)
2. [Common Migration Scenarios](#common-migration-scenarios)
3. [Data Preservation Strategies](#data-preservation-strategies)
4. [Tool-Specific Rollback Procedures](#tool-specific-rollback-procedures)

---

## Migration Rollback Fundamentals

### The Golden Rule

**Always rollback database migrations BEFORE rolling back application code.**

Why? The new application code expects the new schema. If you rollback the app first, the new code will try to use the old schema and fail.

**Correct Order:**
1. Stop application traffic (optional but recommended)
2. Rollback database migration
3. Rollback application code
4. Restart application
5. Validate

**Incorrect Order (will cause errors):**
1. ❌ Rollback application code
2. ❌ New app code tries to use old schema → ERRORS
3. Rollback database migration

### Pre-Rollback Checklist

Before any database rollback:

```bash
# 1. Backup current database state
docker exec <db-container> pg_dump -U user dbname > backup_$(date +%Y%m%d_%H%M%S).sql

# 2. Verify backup integrity
pg_restore --list backup_20260215_143022.sql | head

# 3. Document current migration state
docker exec <db-container> alembic current
# or
docker exec <db-container> psql -U user -d dbname -c "SELECT * FROM schema_migrations;"

# 4. Stop application traffic (if possible)
docker-compose stop app

# 5. Identify target migration version
docker exec <db-container> alembic history
```

---

## Common Migration Scenarios

### Scenario 1: Add Column Migration

**Forward Migration:**
```sql
ALTER TABLE users ADD COLUMN email VARCHAR(255);
```

**Rollback Migration:**
```sql
ALTER TABLE users DROP COLUMN email;
```

**Considerations:**
- **Data Loss**: Dropping the column loses all email data
- **Mitigation**: Backup data before rollback, or create archive table
- **Application Impact**: Old app code doesn't use email column, so safe to remove

**Safe Rollback Procedure:**

```bash
# 1. Backup data from new column (if needed later)
docker exec <db-container> psql -U user -d dbname -c \
  "CREATE TABLE users_email_backup AS SELECT id, email FROM users WHERE email IS NOT NULL;"

# 2. Stop application
docker-compose stop app

# 3. Rollback migration
docker exec <db-container> alembic downgrade -1

# 4. Verify column removed
docker exec <db-container> psql -U user -d dbname -c "\d users"

# 5. Rollback app code
sed -i 's/myapp:v1.2.4/myapp:v1.2.3/g' docker-compose.yml
docker-compose up -d app
```

### Scenario 2: Remove Column Migration

**Forward Migration:**
```sql
ALTER TABLE users DROP COLUMN legacy_id;
```

**Rollback Migration:**
```sql
ALTER TABLE users ADD COLUMN legacy_id INT;
-- Problem: Data is lost! Need to restore from backup
```

**Considerations:**
- **Data Loss**: Original column data is gone
- **Critical**: Must restore from backup if data is needed
- **Application Impact**: Old app may depend on legacy_id column

**Rollback Procedure (with data restore):**

```bash
# 1. Stop application
docker-compose stop app

# 2. Rollback migration (recreates column but without data)
docker exec <db-container> alembic downgrade -1

# 3. Restore data from backup
docker exec <db-container> psql -U user -d dbname < backup_before_migration.sql

# Alternative: Restore only the missing column data
docker exec <db-container> psql -U user -d dbname -c \
  "UPDATE users u SET legacy_id = b.legacy_id FROM users_backup b WHERE u.id = b.id;"

# 4. Verify data restored
docker exec <db-container> psql -U user -d dbname -c \
  "SELECT COUNT(*) FROM users WHERE legacy_id IS NOT NULL;"

# 5. Rollback app code
sed -i 's/myapp:v1.2.4/myapp:v1.2.3/g' docker-compose.yml
docker-compose up -d app
```

### Scenario 3: Rename Column Migration

**Forward Migration:**
```sql
ALTER TABLE users RENAME COLUMN name TO full_name;
```

**Rollback Migration:**
```sql
ALTER TABLE users RENAME COLUMN full_name TO name;
```

**Considerations:**
- **No Data Loss**: Data is preserved, just column name changes
- **Safe Rollback**: Can rollback and re-apply safely
- **Application Impact**: App code must use correct column name

**Rollback Procedure:**

```bash
# 1. Stop application
docker-compose stop app

# 2. Rollback migration
docker exec <db-container> alembic downgrade -1

# 3. Verify column renamed back
docker exec <db-container> psql -U user -d dbname -c "\d users"

# 4. Rollback app code
sed -i 's/myapp:v1.2.4/myapp:v1.2.3/g' docker-compose.yml
docker-compose up -d app
```

### Scenario 4: Add Index Migration

**Forward Migration:**
```sql
CREATE INDEX idx_users_email ON users(email);
```

**Rollback Migration:**
```sql
DROP INDEX idx_users_email;
```

**Considerations:**
- **No Data Loss**: Indexes don't store data, just improve lookups
- **Safe Rollback**: Can rollback and re-apply without issues
- **Performance Impact**: Old app may be slower without index

**Rollback Procedure:**

```bash
# No need to stop application for index rollback (if using CONCURRENTLY)

# 1. Rollback migration
docker exec <db-container> alembic downgrade -1

# 2. Verify index removed
docker exec <db-container> psql -U user -d dbname -c "\d users"

# If application performance degrades, consider rolling back app too
```

### Scenario 5: Create Table Migration

**Forward Migration:**
```sql
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),
  total DECIMAL(10,2),
  created_at TIMESTAMP DEFAULT NOW()
);
```

**Rollback Migration:**
```sql
DROP TABLE orders;
```

**Considerations:**
- **Data Loss**: All data in the table is lost
- **Critical**: Backup table data before rollback if needed
- **Application Impact**: Old app doesn't use orders table, safe to remove

**Rollback Procedure:**

```bash
# 1. Backup table data (if needed later)
docker exec <db-container> pg_dump -U user -d dbname -t orders > orders_backup.sql

# 2. Stop application
docker-compose stop app

# 3. Rollback migration
docker exec <db-container> alembic downgrade -1

# 4. Verify table dropped
docker exec <db-container> psql -U user -d dbname -c "\dt"

# 5. Rollback app code
sed -i 's/myapp:v1.2.4/myapp:v1.2.3/g' docker-compose.yml
docker-compose up -d app
```

### Scenario 6: Data Migration (Update Existing Data)

**Forward Migration:**
```sql
-- Normalize phone numbers from various formats to E.164
UPDATE users SET phone = regexp_replace(phone, '[^0-9]', '', 'g');
UPDATE users SET phone = '+1' || phone WHERE phone NOT LIKE '+%';
```

**Rollback Migration:**
```sql
-- Problem: Original phone formats are lost!
-- Cannot reverse data transformation without backup
```

**Considerations:**
- **Data Loss**: Original data formats are overwritten
- **Critical**: Must have backup of original data
- **Risky**: Data migrations are hardest to rollback

**Rollback Procedure (requires backup):**

```bash
# 1. Stop application
docker-compose stop app

# 2. Restore original data from backup
docker exec <db-container> psql -U user -d dbname -c \
  "UPDATE users u SET phone = b.phone FROM users_backup b WHERE u.id = b.id;"

# 3. Rollback migration (if it has schema changes)
docker exec <db-container> alembic downgrade -1

# 4. Verify data restored
docker exec <db-container> psql -U user -d dbname -c \
  "SELECT phone FROM users LIMIT 10;"

# 5. Rollback app code
sed -i 's/myapp:v1.2.4/myapp:v1.2.3/g' docker-compose.yml
docker-compose up -d app
```

**Best Practice for Data Migrations:**

Create backup table BEFORE transformation:

```sql
-- In forward migration
CREATE TABLE users_phone_backup AS SELECT id, phone FROM users;

-- Transform data
UPDATE users SET phone = regexp_replace(phone, '[^0-9]', '', 'g');

-- In rollback migration
UPDATE users u SET phone = b.phone FROM users_phone_backup b WHERE u.id = b.id;
DROP TABLE users_phone_backup;
```

---

## Data Preservation Strategies

### Strategy 1: Backup Tables

Create backup table before destructive migration:

```sql
-- Forward migration
CREATE TABLE users_backup AS TABLE users;

ALTER TABLE users DROP COLUMN legacy_id;

-- Rollback migration
ALTER TABLE users ADD COLUMN legacy_id INT;
UPDATE users u SET legacy_id = b.legacy_id FROM users_backup b WHERE u.id = b.id;
DROP TABLE users_backup;
```

### Strategy 2: Shadow Columns

Keep old column while adding new one (transition period):

```sql
-- Migration 1: Add new column
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);
UPDATE users SET full_name = name;  -- Copy data

-- App deploys, uses full_name

-- Migration 2 (later): Remove old column
ALTER TABLE users DROP COLUMN name;

-- Rollback is easier because data exists in both columns initially
```

### Strategy 3: Archive Tables

Move old data to archive instead of deleting:

```sql
-- Forward migration
CREATE TABLE users_archive AS SELECT * FROM users WHERE deleted_at IS NOT NULL;
DELETE FROM users WHERE deleted_at IS NOT NULL;

-- Rollback migration
INSERT INTO users SELECT * FROM users_archive;
DROP TABLE users_archive;
```

### Strategy 4: Versioned Schema

Use separate schema versions for transition:

```sql
-- Create new schema version
CREATE SCHEMA v2;
CREATE TABLE v2.users (...new structure...);

-- Migrate data
INSERT INTO v2.users SELECT ... FROM public.users;

-- App points to v2 schema

-- Rollback: Point app back to public schema
-- Old schema still exists
```

---

## Tool-Specific Rollback Procedures

### Alembic (Python)

```bash
# View migration history
docker exec <db-container> alembic history

# Check current version
docker exec <db-container> alembic current

# Rollback one migration
docker exec <db-container> alembic downgrade -1

# Rollback to specific version
docker exec <db-container> alembic downgrade abc123

# Rollback to base (all migrations)
docker exec <db-container> alembic downgrade base
```

**Alembic Migration File:**

```python
# alembic/versions/001_add_email.py
def upgrade():
    op.add_column('users', sa.Column('email', sa.String(255)))

def downgrade():
    op.drop_column('users', 'email')
```

### Flyway (Java)

```bash
# View migration history
docker exec <app-container> flyway info

# Undo last migration (requires Flyway Teams/Enterprise)
docker exec <app-container> flyway undo

# Note: Flyway Community Edition doesn't support undo
# Must manually create rollback scripts
```

**Flyway Rollback Script:**

```sql
-- V1__add_email.sql (forward)
ALTER TABLE users ADD COLUMN email VARCHAR(255);

-- U1__add_email.sql (undo - Teams/Enterprise only)
ALTER TABLE users DROP COLUMN email;
```

### Django (Python)

```bash
# View migrations
docker exec <app-container> python manage.py showmigrations

# Rollback to specific migration
docker exec <app-container> python manage.py migrate myapp 0001_initial

# Rollback all migrations for app
docker exec <app-container> python manage.py migrate myapp zero
```

### Rails (Ruby)

```bash
# Rollback last migration
docker exec <app-container> rails db:rollback

# Rollback last N migrations
docker exec <app-container> rails db:rollback STEP=3

# Rollback to specific version
docker exec <app-container> rails db:migrate:down VERSION=20230115120000
```

### Liquibase (Java)

```bash
# View rollback SQL (preview)
docker exec <app-container> liquibase rollbackSQL <tag>

# Rollback to tag
docker exec <app-container> liquibase rollback <tag>

# Rollback N changesets
docker exec <app-container> liquibase rollbackCount 3
```

---

## Emergency Rollback Procedures

### When Migration Tool Fails

If migration tool can't rollback:

```bash
# 1. Connect to database
docker exec -it <db-container> psql -U user -d dbname

# 2. Manually reverse changes
ALTER TABLE users DROP COLUMN email;

# 3. Update migration tracking table
DELETE FROM alembic_version WHERE version_num = 'abc123';

# 4. Verify state
\d users
SELECT * FROM alembic_version;
```

### When Data is Corrupted

If rollback fails due to data issues:

```bash
# 1. Stop everything
docker-compose stop

# 2. Restore from backup
docker exec <db-container> psql -U user -d dbname < backup_20260215_120000.sql

# 3. Verify data integrity
docker exec <db-container> psql -U user -d dbname -c "SELECT COUNT(*) FROM users;"

# 4. Update migration state to match backup
docker exec <db-container> psql -U user -d dbname -c \
  "UPDATE alembic_version SET version_num = 'previous_version';"

# 5. Start with old app version
sed -i 's/myapp:v1.2.4/myapp:v1.2.3/g' docker-compose.yml
docker-compose up -d
```

---

## Best Practices

1. **Always backup before migration** - Automate this in CI/CD
2. **Test rollback in staging** - Ensure rollback migrations work
3. **Write reversible migrations** - Every up() should have a down()
4. **Avoid data transformations** - If unavoidable, backup original data
5. **Use transaction-safe migrations** - Wrap in BEGIN/COMMIT when possible
6. **Document migration dependencies** - Track what depends on what
7. **Version migration scripts** - Store in git with app code
8. **Coordinate with app deploys** - Database version must match app version
9. **Monitor migration execution** - Track timing and errors
10. **Practice rollbacks regularly** - Fire drills ensure procedures work
