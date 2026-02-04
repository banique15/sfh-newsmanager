# Instructions Directory

This directory contains **procedural workflows** mapped directly to the [Master AI Blue Prints](../Master%20AI%20Blue%20Prints.md) user stories and edge cases.

## Structure

### Core Principles
- **[00_principles.md](00_principles.md)** - Foundational principles from Blueprint Section 6

### Core Tasks (Section 3)
13 instruction files covering main user stories:

1. **[3.1_create_article_with_image.md](core_tasks/3.1_create_article_with_image.md)** - Full newsletter flow
2. **[3.2_create_article_simple.md](core_tasks/3.2_create_article_simple.md)** - Text-only article
3. **[3.3_list_show_content.md](core_tasks/3.3_list_show_content.md)** - Read-only queries
4. **[3.4_update_content.md](core_tasks/3.4_update_content.md)** - Modify existing article
5. **[3.5_delete_content.md](core_tasks/3.5_delete_content.md)** - Remove article
6. **[3.6_publish_article.md](core_tasks/3.6_publish_article.md)** - Make live
7. **[3.7_unpublish_article.md](core_tasks/3.7_unpublish_article.md)** - Take down
8. **[3.8_generate_image_standalone.md](core_tasks/3.8_generate_image_standalone.md)** - Image-only generation
9. **[3.9_add_hero_image.md](core_tasks/3.9_add_hero_image.md)** - Add image to existing article
10. **[3.10_clarification.md](core_tasks/3.10_clarification.md)** - When to ask questions
11. **[3.11_user_confirms.md](core_tasks/3.11_user_confirms.md)** - Yes/Do it flow
12. **[3.12_user_cancels.md](core_tasks/3.12_user_cancels.md)** - Cancel flow
13. **[3.13_follow_up_context.md](core_tasks/3.13_follow_up_context.md)** - Handle "it", "that one"

### Edge Cases (Section 4)
18 instruction files covering special scenarios:

- **[4.1_duplicate_titles.md](edge_cases/4.1_duplicate_titles.md)** - Handle similar/duplicate titles
- **[4.2_multiple_matches.md](edge_cases/4.2_multiple_matches.md)** - "Which article?" disambiguation
- **[4.3_user_pastes_content.md](edge_cases/4.3_user_pastes_content.md)** - Content provided in message
- **[4.4_user_provides_link.md](edge_cases/4.4_user_provides_link.md)** - URL-based requests
- **[4.5_fix_typo.md](edge_cases/4.5_fix_typo.md)** - Small edits
- **[4.6_undo_revert.md](edge_cases/4.6_undo_revert.md)** - Undo operations
- **[4.7_bulk_requests.md](edge_cases/4.7_bulk_requests.md)** - Multiple articles at once
- **[4.8_partial_failure.md](edge_cases/4.8_partial_failure.md)** - Error handling mid-operation
- **[4.9_empty_vague_request.md](edge_cases/4.9_empty_vague_request.md)** - Unclear user intent
- **[4.10_out_of_scope.md](edge_cases/4.10_out_of_scope.md)** - Non-news content requests
- **[4.11_no_results.md](edge_cases/4.11_no_results.md)** - Empty search/list results
- **[4.12_thread_vs_new_message.md](edge_cases/4.12_thread_vs_new_message.md)** - Context across threads
- **[4.13_switch_channel.md](edge_cases/4.13_switch_channel.md)** - Cross-channel context
- **[4.14_whats_live_vs_draft.md](edge_cases/4.14_whats_live_vs_draft.md)** - Status queries
- **[4.15_duplicate_article.md](edge_cases/4.15_duplicate_article.md)** - Copy and modify
- **[4.16_schedule_publish.md](edge_cases/4.16_schedule_publish.md)** - Delayed publishing
- **[4.17_email_request.md](edge_cases/4.17_email_request.md)** - Email-specific handling
- **[4.18_portal_request.md](edge_cases/4.18_portal_request.md)** - Future portal integration

## Format

Each instruction file follows this structure:

```markdown
---
blueprint_section: [section number]
difficulty: [easy|medium|hard]
requires_confirmation: [yes|no]
channels: [slack|email|portal|all]
required_tools: [tool names]
---

# [Task Name]
## Overview
## Why This Approach
## Prerequisites
## Step-by-Step Procedure
## Expected Outcome
## Error Handling
## Cross-References
```

## Usage

Each instruction maps to exactly one blueprint section and provides the complete procedural workflow for implementing that user story or edge case.
