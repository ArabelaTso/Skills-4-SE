# Graphviz/DOT Diagram Patterns

## Architecture Diagrams

Use directed graphs with subgraphs for system architecture:

```dot
digraph SystemArchitecture {
    rankdir=TB;
    node [shape=box, style=rounded];

    // Define nodes
    client [label="Web Client", shape=box];
    api [label="API Gateway"];
    auth [label="Auth Service"];
    db [label="Database", shape=cylinder];
    cache [label="Redis Cache", shape=cylinder];
    queue [label="Message Queue", shape=parallelogram];
    worker [label="Background Worker"];

    // Define relationships
    client -> api [label="HTTPS"];
    api -> auth [label="validate"];
    api -> cache [label="read/write"];
    api -> db [label="query"];
    api -> queue [label="publish"];
    queue -> worker [label="consume"];
    worker -> db [label="update"];
}
```

## Data Flow Diagrams

Use directed graphs with clear flow:

```dot
digraph DataFlow {
    rankdir=LR;
    node [shape=box];

    input [label="User Input"];
    validate [label="Validation"];
    transform [label="Transformation"];
    process [label="Business Logic"];
    store [label="Data Store", shape=cylinder];
    output [label="API Response"];

    input -> validate -> transform -> process -> store -> output;
}
```

## Deployment Diagrams

Use clusters for infrastructure grouping:

```dot
digraph Deployment {
    rankdir=TB;
    compound=true;

    subgraph cluster_aws {
        label="AWS Cloud";
        style=dashed;

        subgraph cluster_vpc {
            label="VPC";

            subgraph cluster_public {
                label="Public Subnet";
                lb [label="Load Balancer", shape=box];
            }

            subgraph cluster_private {
                label="Private Subnet";
                app1 [label="App Server 1"];
                app2 [label="App Server 2"];
            }

            subgraph cluster_data {
                label="Data Subnet";
                db [label="RDS Database", shape=cylinder];
                cache [label="ElastiCache", shape=cylinder];
            }
        }
    }

    users [label="Users", shape=ellipse];

    users -> lb;
    lb -> app1;
    lb -> app2;
    app1 -> db;
    app2 -> db;
    app1 -> cache;
    app2 -> cache;
}
```

## Network Topology

Use undirected graphs for network diagrams:

```dot
graph NetworkTopology {
    node [shape=box];

    router [label="Core Router", shape=diamond];
    switch1 [label="Switch 1"];
    switch2 [label="Switch 2"];
    fw [label="Firewall", shape=hexagon];
    server1 [label="Server 1"];
    server2 [label="Server 2"];
    server3 [label="Server 3"];

    router -- fw;
    router -- switch1;
    router -- switch2;
    switch1 -- server1;
    switch1 -- server2;
    switch2 -- server3;
}
```

## Best Practices

- Use `rankdir` to control layout direction (TB, LR, BT, RL)
- Use clusters (subgraphs) to group related components
- Choose appropriate shapes: box, cylinder, diamond, ellipse, parallelogram
- Use edge labels to show protocols or data types
- Use `compound=true` for edges between clusters
- Apply styling with colors and line styles for emphasis
