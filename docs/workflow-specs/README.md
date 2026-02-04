# Workflows Directory

This directory contains workflow definitions that orchestrate multi-step operations for the Newsletter Manager.

## Overview

Workflows coordinate multiple tools and handle complex user requests that require several steps to complete.

---

## Available Workflows

### 1. Create Article with Image
**File:** [create_with_image.md](create_with_image.md)  
**Blueprint:** Task 3.1  
**Complexity:** High

Orchestrates:
- Content generation
- Image generation
- Image storage
- Article creation
- User confirmation

**Example:** *"Create an article about the spring fundraiser with a hero image"*

---

### 2. Update and Publish
**File:** [update_and_publish.md](update_and_publish.md)  
**Blueprint:** Tasks 3.4 + 3.6  
**Complexity:** Medium

Orchestrates:
- Article identification
- Content update
- Publishing
- User confirmation

**Example:** *"Update the gala article with the new date and publish it"*

---

### 3. Bulk Publish
**File:** [bulk_publish.md](bulk_publish.md)  
**Blueprint:** Edge Case 4.7  
**Complexity:** High

Orchestrates:
- Article search and filtering
- List presentation
- Batch publishing
- Progress tracking
- Partial failure handling

**Example:** *"Publish all drafts"*

---

## Workflow Structure

Each workflow definition includes:

### 1. Metadata
- ID (unique identifier)
- Type (multi-step, batch, etc.)
- Blueprint reference

### 2. Steps
Detailed step-by-step execution plan:
- Tool to use
- Input parameters
- Expected output
- Error handling
- Next step logic

### 3. State Management
- What to store in memory
- When to clear state
- Context tracking

### 4. Error Handling
- Failure scenarios
- Retry strategies
- Partial success handling
- User notification

### 5. Success Criteria
- Full success conditions
- Partial success conditions
- Metrics to track

---

## Workflow vs Instruction Files

**Instructions** (`/instructions/`):
- Single-step or simple operations
- Direct user-to-tool interactions
- Minimal state management

**Workflows** (`/workflows/`):
- Multi-step orchestrations
- Complex state management
- Coordination between multiple tools
- Partial failure handling

---

## When to Use Workflows

Create a workflow for:
- ✅ Operations requiring 3+ tools
- ✅ Batch/bulk operations
- ✅ Operations with complex error recovery
- ✅ Multi-modal operations (content + image, update + publish)

Use simple instructions for:
- ✅ Single tool operations
- ✅ Read-only operations
- ✅ Simple confirmations

---

## Workflow Execution

Workflows are typically triggered by:
1. User intent detection
2. Workflow selector (based on intent complexity)
3. Workflow orchestrator execution
4. Result reporting

---

## Future Workflows

Potential additions as system grows:
- **Schedule and Publish** - Time-delayed publishing
- **Bulk Update** - Update multiple articles at once
- **Content Migration** - Import articles from external sources
- **Multi-language Support** - Create translated versions
- **SEO Optimization** - Auto-optimize article metadata
