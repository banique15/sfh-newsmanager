# SFH Newsletter Manager

AI agent for managing news/newsletter content at Sing for Hope. Handles article creation, editing, publishing, and organization across Slack, Email, and Portal channels.

## Overview

This agent is the single point of contact for staff who need news content created or changed, following these core principles:
- **News only** - Scope limited to articles/blog posts
- **Confirm before change** - Never create/update/delete without approval
- **Clarify when ambiguous** - Ask specific questions instead of guessing
- **Same procedures everywhere** - Consistent behavior across all channels
- **Plain language** - No technical jargon exposed to users

## Project Structure

### Core Directories

- **[examples/](examples/)** - Source of truth files
  - Article templates and reference data
  - AI prompt templates
  - Sample responses and confirmations
  - Real-world request examples

- **[instructions/](instructions/)** - Task completion guidelines
  - Core tasks (create, update, delete, publish, etc.)
  - Edge cases and error scenarios
  - Procedural workflows for each user story

- **[tools/](tools/)** - Available capabilities
  - Channel integrations (Slack, Email, Portal)
  - Content operations (CRUD, search, status)
  - AI tools (generation, intent detection)
  - Confirmation and clarification flows

### Implementation Directories

- **[agents/](agents/)** - Agent role definitions
- **[workflows/](workflows/)** - Multi-step orchestration
- **[config/](config/)** - Environment configurations
- **[tests/](tests/)** - Test coverage

### Documentation

- **[Master AI Blue Prints.md](Master%20AI%20Blue%20Prints.md)** - Complete specification of all user stories, edge cases, and principles

## Quick Start

[To be added: setup instructions]

## Supported Use Cases

See [Master AI Blue Prints.md](Master%20AI%20Blue%20Prints.md) for complete details. Key capabilities:

- ✅ Create articles with optional hero images
- ✅ Update existing content
- ✅ Publish/unpublish articles
- ✅ List and search articles by status
- ✅ Generate standalone images
- ✅ Handle multi-channel requests (Slack/Email/Portal)
- ✅ Context-aware follow-ups ("update it", "publish that one")
- ✅ Comprehensive error handling and clarification flows

## Implementation Status

[To be tracked as features are built]