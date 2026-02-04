# Agents Directory

This directory contains agent definitions that describe the behavior, capabilities, and configuration of AI agents in the Newsletter Manager system.

## Agent: Newsletter Manager

**File:** [newsletter_manager.md](newsletter_manager.md)

The primary agent responsible for managing news articles across all channels.

### Responsibilities
- Create, update, delete news articles
- Publish and unpublish content
- Generate and manage images
- Search and list articles
- Handle user interactions across Slack, Email, and Portal

### Key Characteristics
- Professional, calm, helpful tone
- Confirms before any changes
- Plain language communication
- Follows core principles from Master AI Blue Prints

---

## Agent Structure

Each agent definition includes:

### 1. Identity
- Name, role, version
- Scope and boundaries

### 2. Capabilities
- Primary functions
- Supported channels
- Tool access

### 3. Behavior Configuration
- Tone and style guidelines
- Core principles
- Response patterns

### 4. Permissions
- Allowed operations
- Restricted operations
- Confirmation requirements

### 5. Error Handling
- Failure strategies
- Ambiguity resolution
- Partial failure handling

### 6. Memory & Context
- Short-term memory scope
- Context resolution rules
- Cross-channel behavior

### 7. Workflow Integration
- Simple vs complex operations
- Workflow orchestration

---

## Usage

Agent definitions serve as:
- **Reference documentation** for implementation teams
- **Behavior specifications** for AI agent configuration
- **Testing criteria** for validation
- **Onboarding materials** for team members

---

## Future Agents

As the system grows, additional specialized agents may be added:
- **Image Curator** - Specialized in visual content management
- **Content Reviewer** - Automated quality checks
- **Analytics Reporter** - Content performance insights
