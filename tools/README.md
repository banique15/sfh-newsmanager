# Tools Directory

This directory defines **what capabilities are available** for each task in the Newsletter Manager agent.

## Structure

- **[tool_registry.json](tool_registry.json)** - Master list of all available tools
- **[channel_tools/](channel_tools/)** - Communication interfaces (Slack, Email, Portal)
- **[content_tools/](content_tools/)** - Article operations (CRUD, search, status)
- **[ai_tools/](ai_tools/)** - AI capabilities (generation, intent detection, context)
- **[media_tools/](media_tools/)** - Asset management (image storage/linking)
- **[confirmation_tools/](confirmation_tools/)** - User interaction (Yes/No, clarification)
- **[utility_tools/](utility_tools/)** - Support functions (memory, error handling)

## Tool Definition Format

Each tool is defined in JSON with the following structure:

```json
{
  "tool_name": "string",
  "version": "string",
  "description": "Brief description of what this tool does",
  "category": "channel|content|ai|media|confirmation|utility",
  "blueprint_tasks": ["3.1", "3.2", "3.4"],
  "required_params": [
    {
      "name": "param_name",
      "type": "string|number|boolean|object",
      "description": "What this parameter does"
    }
  ],
  "optional_params": [],
  "dependencies": ["other_tool_name"],
  "applicable_channels": ["slack", "email", "portal"],
  "examples": "../../examples/path/to/example",
  "error_codes": {
    "ERROR_CODE": "Plain language explanation"
  }
}
```

## Categories

### Channel Tools
Interfaces for communicating with users across different platforms (Slack, Email, Portal).

### Content Tools
Core database operations for article management (create, read, update, delete, search, publish/unpublish).

### AI Tools
LLM-powered capabilities for content generation, image creation, intent detection, and context resolution.

### Media Tools
Image and asset management including storage, linking, and URL generation.

### Confirmation Tools
User interaction tools for generating confirmation prompts (Yes/Cancel) and clarification questions.

### Utility Tools
Supporting tools for conversation memory, error handling, and common operations.

## Usage

When implementing instructions from [../instructions/](../instructions/), reference the `required_tools` field to identify which tool definitions to use. Each tool specifies which blueprint tasks it supports via the `blueprint_tasks` field.
