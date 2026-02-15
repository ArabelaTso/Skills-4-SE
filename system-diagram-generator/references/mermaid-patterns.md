# Mermaid Diagram Patterns

## Architecture Diagrams

Use flowcharts or C4 diagrams for system architecture:

```mermaid
graph TB
    Client[Web Client]
    API[API Gateway]
    Auth[Auth Service]
    DB[(Database)]
    Cache[(Redis Cache)]
    Queue[Message Queue]
    Worker[Background Worker]

    Client -->|HTTPS| API
    API --> Auth
    API --> Cache
    API --> DB
    API --> Queue
    Queue --> Worker
    Worker --> DB
```

## Data Flow Diagrams

Use flowcharts with clear directional flow:

```mermaid
flowchart LR
    Input[User Input] --> Validate[Validation Layer]
    Validate --> Transform[Data Transformation]
    Transform --> Process[Business Logic]
    Process --> Store[(Data Store)]
    Store --> Output[API Response]
```

## Deployment Diagrams

Use C4 deployment diagrams or structured flowcharts:

```mermaid
graph TB
    subgraph "AWS Cloud"
        subgraph "VPC"
            subgraph "Public Subnet"
                LB[Load Balancer]
            end
            subgraph "Private Subnet"
                App1[App Server 1]
                App2[App Server 2]
            end
            subgraph "Data Subnet"
                DB[(RDS Database)]
                Cache[(ElastiCache)]
            end
        end
    end

    Users[Users] --> LB
    LB --> App1
    LB --> App2
    App1 --> DB
    App2 --> DB
    App1 --> Cache
    App2 --> Cache
```

## Sequence Diagrams

Use sequence diagrams for interactions over time:

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Auth
    participant Database

    User->>Frontend: Login Request
    Frontend->>API: POST /auth/login
    API->>Auth: Validate Credentials
    Auth->>Database: Query User
    Database-->>Auth: User Data
    Auth-->>API: JWT Token
    API-->>Frontend: Token + User Info
    Frontend-->>User: Redirect to Dashboard
```

## Best Practices

- Use descriptive node names
- Group related components in subgraphs
- Show clear data flow direction
- Include relevant protocols (HTTPS, gRPC, etc.)
- Use appropriate shapes: rectangles for services, cylinders for databases, etc.
