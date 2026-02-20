# Document Structure Patterns

## README Structure

### Standard README Pattern
```markdown
# Project Title

Brief description of the project (1-2 sentences)

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

```bash
npm install package-name
```

## Usage

Basic usage examples

## Configuration

Configuration options and environment variables

## Contributing

Guidelines for contributing

## License

License information
```

### Minimal README Pattern
```markdown
# Project Title

Description

## Installation

Installation instructions

## Usage

Usage examples
```

## Technical Documentation Structure

### API Documentation Pattern
```markdown
# API Name

Overview and purpose

## Table of Contents
- [Authentication](#authentication)
- [Endpoints](#endpoints)
- [Error Handling](#error-handling)
- [Examples](#examples)

## Authentication

How to authenticate

## Endpoints

### GET /resource
Description and parameters

### POST /resource
Description and parameters

## Error Handling

Common errors and solutions

## Examples

Complete usage examples
```

### User Guide Pattern
```markdown
# Product Name User Guide

## Table of Contents
- [Getting Started](#getting-started)
- [Basic Concepts](#basic-concepts)
- [Common Tasks](#common-tasks)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)

## Getting Started

Prerequisites and initial setup

## Basic Concepts

Core concepts users need to understand

## Common Tasks

Step-by-step guides for common tasks

## Advanced Features

Advanced functionality

## Troubleshooting

Common issues and solutions
```

## Long-Form Content Structure

### Article/Blog Post Pattern
```markdown
# Article Title

Brief introduction or hook

## Table of Contents
- [Introduction](#introduction)
- [Main Topic 1](#main-topic-1)
- [Main Topic 2](#main-topic-2)
- [Conclusion](#conclusion)

## Introduction

Context and background

## Main Topic 1

First main section

## Main Topic 2

Second main section

## Conclusion

Summary and takeaways
```

### Tutorial Pattern
```markdown
# Tutorial: How to [Task]

What you'll learn and prerequisites

## Table of Contents
- [Prerequisites](#prerequisites)
- [Step 1: Setup](#step-1-setup)
- [Step 2: Implementation](#step-2-implementation)
- [Step 3: Testing](#step-3-testing)
- [Next Steps](#next-steps)

## Prerequisites

Required knowledge and tools

## Step 1: Setup

Initial setup instructions

## Step 2: Implementation

Main implementation steps

## Step 3: Testing

How to test the implementation

## Next Steps

Further learning and resources
```

## Section Organization Principles

### Logical Flow
1. General to specific
2. Simple to complex
3. Prerequisites before usage
4. Theory before practice
5. Common before advanced

### Section Ordering

**For README:**
1. Title and description
2. Badges/status (optional)
3. Table of contents
4. Features/highlights
5. Installation
6. Quick start
7. Usage examples
8. Configuration
9. API reference
10. Contributing
11. License
12. Acknowledgments

**For Technical Docs:**
1. Title
2. Overview
3. Table of contents
4. Prerequisites
5. Installation/setup
6. Basic usage
7. Advanced usage
8. API reference
9. Examples
10. Troubleshooting
11. FAQ
12. Additional resources

**For Tutorials:**
1. Title and goal
2. Prerequisites
3. Table of contents
4. Introduction/background
5. Step-by-step instructions
6. Verification/testing
7. Troubleshooting
8. Next steps
9. Additional resources

## Missing Section Detection

### README Files
Check for:
- Installation instructions
- Usage examples
- License information
- Contributing guidelines (for open source)

### Technical Documentation
Check for:
- Prerequisites
- Installation/setup
- Basic usage examples
- Troubleshooting section

### Tutorials
Check for:
- Prerequisites
- Clear step-by-step structure
- Verification/testing steps
- Next steps or further reading

## Section Consolidation Rules

### When to Merge Sections
- Multiple short sections covering same topic
- Duplicate information in different sections
- Overly fragmented content

### When to Split Sections
- Section is too long (>500 lines)
- Section covers multiple distinct topics
- Section has multiple subsections that could stand alone

### Consolidation Examples

**Before:**
```markdown
## Installation
npm install

## Installing Dependencies
npm install

## Setup
Run npm install
```

**After:**
```markdown
## Installation

Install the package and its dependencies:

```bash
npm install
```
```
