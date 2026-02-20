# PlantUML Diagram Patterns

## Architecture Diagrams

Use component diagrams for system architecture:

```plantuml
@startuml
!include <C4/C4_Container>

Person(user, "User", "End user of the system")
System_Boundary(system, "Application System") {
    Container(web, "Web Application", "React", "Provides UI")
    Container(api, "API Gateway", "Node.js", "Handles requests")
    Container(auth, "Auth Service", "Python", "Authentication")
    ContainerDb(db, "Database", "PostgreSQL", "Stores data")
    Container(cache, "Cache", "Redis", "Caching layer")
}

Rel(user, web, "Uses", "HTTPS")
Rel(web, api, "Calls", "REST/JSON")
Rel(api, auth, "Validates", "gRPC")
Rel(api, db, "Reads/Writes")
Rel(api, cache, "Caches")
@enduml
```

## Data Flow Diagrams

Use activity diagrams for data flow:

```plantuml
@startuml
start
:Receive User Input;
:Validate Input;
if (Valid?) then (yes)
  :Transform Data;
  :Apply Business Rules;
  :Store in Database;
  :Return Success;
else (no)
  :Return Error;
endif
stop
@enduml
```

## Deployment Diagrams

Use deployment diagrams for infrastructure:

```plantuml
@startuml
node "AWS Cloud" {
  node "Load Balancer" as lb {
    [ALB]
  }

  node "Application Tier" {
    [App Server 1]
    [App Server 2]
  }

  node "Data Tier" {
    database "RDS" as db
    database "Redis" as cache
  }
}

[ALB] --> [App Server 1]
[ALB] --> [App Server 2]
[App Server 1] --> db
[App Server 2] --> db
[App Server 1] --> cache
[App Server 2] --> cache
@enduml
```

## Sequence Diagrams

Use sequence diagrams for interactions:

```plantuml
@startuml
actor User
participant "Frontend" as FE
participant "API Gateway" as API
participant "Auth Service" as Auth
database "Database" as DB

User -> FE: Login Request
FE -> API: POST /auth/login
API -> Auth: Validate Credentials
Auth -> DB: Query User
DB --> Auth: User Data
Auth --> API: JWT Token
API --> FE: Token + User Info
FE --> User: Redirect to Dashboard
@enduml
```

## Best Practices

- Use C4 model for architecture diagrams when possible
- Include stereotypes and technologies in component descriptions
- Use appropriate diagram types: component, deployment, sequence, activity
- Add notes for complex interactions
- Use colors and styling to highlight important components
