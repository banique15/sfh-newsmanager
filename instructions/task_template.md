---
blueprint_section: "task_template"
difficulty: [easy|medium|hard]
requires_confirmation: [yes|no]
channels: [slack|email|portal|all]
required_tools: [list tool names from tools/]
---

# [Task Name from Blueprint]

## Overview

[Copy from "What the user does" section in blueprint]

Brief description of what this task accomplishes.

## Why This Approach

[Copy from "Why we do it this way" section in blueprint]

Explanation of the rationale behind this procedural flow.

## Prerequisites

- **Required tools:**
  - `tool_name_1` - What it does
  - `tool_name_2` - What it does
  
- **Required data/context:**
  - What information is needed (article ID, topic, etc.)
  - Where it comes from (user request, conversation history, etc.)
  
- **Channel considerations:**
  - Any channel-specific behavior
  - Default: works identically across all channels

## Step-by-Step Procedure

[Map from "Expected behavior (procedural flow)" section in blueprint]

### 1. **[Step Name]**

**Action:** Describe what happens in this step

**Tool(s) used:** `tool_name`

**Parameters/inputs:**
- List what data is needed
- How to get it

**Decision points:**
- If [condition]: do X
- If [condition]: do Y

**Example reference:** [Link to relevant example file]

---

### 2. **[Next Step Name]**

**Action:** [Description]

**Tool(s) used:** `tool_name`

[Continue pattern...]

---

## Expected Outcome

[Copy from "Outcome for the user" section in blueprint]

Describe final state after task completion:
- What was created/changed/deleted
- What the user received (confirmation, link, etc.)
- What's stored for follow-up context

## Error Handling

| Error Scenario | Response/Action |
|---------------|-----------------|
| **[Error type]** | Plain language response and next step |
| **[Error type]** | Response and reference to relevant edge case doc |

## Cross-References

### Related Instructions
- [file.md](path/to/file.md) - Brief description of relationship

### Edge Cases
- [file.md](path/to/file.md) - When this applies

### Examples
- [file.json](../../examples/path/to/file.json) - What this demonstrates

### Tools
- [tool.json](../../tools/category/tool.json) - What it's used for
