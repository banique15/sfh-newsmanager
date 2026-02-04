# Sample User Requests

## Article Creation Requests

### Simple Creation (No Image)
**User:** "Create an article about the summer concert series"

**Intent:** create_article  
**Entities:** topic="summer concert series", image_requested=false  
**Expected Flow:** [3.2_create_article_simple.md](../../instructions/core_tasks/3.2_create_article_simple.md)

---

### Creation with Image
**User:** "Write a newsletter about the spring fundraiser with a hero image"

**Intent:** create_article  
**Entities:** topic="spring fundraiser", image_requested=true  
**Expected Flow:** [3.1_create_article_with_image.md](../../instructions/core_tasks/3.1_create_article_with_image.md)

---

### Creation with Pasted Content
**User:** 
```
Create an article with this:

We're excited to announce our new youth music program launching this fall. 
The program will provide free music lessons to underserved communities 
across all five boroughs. Registration opens in August.
```

**Intent:** create_article  
**Entities:** user_provided_content=true  
**Expected Flow:** [4.3_user_pastes_content.md](../../instructions/edge_cases/4.3_user_pastes_content.md)

---

## Update Requests

### Simple Update
**User:** "Update the gala article with the new date: October 20th"

**Intent:** update_article  
**Entities:** article_reference="gala article", field="content", new_value="October 20th"  
**Expected Flow:** [3.4_update_content.md](../../instructions/core_tasks/3.4_update_content.md)

---

### Context Reference
**User (after creating article):** "Change the title to 'Annual Fundraising Gala 2026'"

**Intent:** update_article  
**Entities:** article_reference="it" (from context), field="title", new_value="Annual Fundraising Gala 2026"  
**Expected Flow:** [3.13_follow_up_context.md](../../instructions/core_tasks/3.13_follow_up_context.md) → [3.4_update_content.md](../../instructions/core_tasks/3.4_update_content.md)

---

### Typo Fix
**User:** "Fix the typo - change 'June 15' to 'June 20' in the concert article"

**Intent:** update_article  
**Entities:** article_reference="concert article", change="June 15" → "June 20"  
**Expected Flow:** [4.5_fix_typo.md](../../instructions/edge_cases/4.5_fix_typo.md)

---

## List/Search Requests

### Show All Drafts
**User:** "Show me all drafts"

**Intent:** list_articles  
**Entities:** status_filter="draft"  
**Expected Flow:** [3.3_list_show_content.md](../../instructions/core_tasks/3.3_list_show_content.md)

---

### What's Live
**User:** "What's currently published?"

**Intent:** list_articles  
**Entities:** status_filter="published"  
**Expected Flow:** [4.14_whats_live_vs_draft.md](../../instructions/edge_cases/4.14_whats_live_vs_draft.md)

---

### Search by Topic
**User:** "Show me articles about the pianos program"

**Intent:** list_articles  
**Entities:** keyword="pianos program"  
**Expected Flow:** [3.3_list_show_content.md](../../instructions/core_tasks/3.3_list_show_content.md)

---

## Publish/Unpublish Requests

### Publish
**User:** "Publish the gala announcement"

**Intent:** publish_article  
**Entities:** article_reference="gala announcement"  
**Expected Flow:** [3.6_publish_article.md](../../instructions/core_tasks/3.6_publish_article.md)

---

### Publish with Context
**User (after creating):** "Publish it"

**Intent:** publish_article  
**Entities:** article_reference="it" (from context)  
**Expected Flow:** [3.13_follow_up_context.md](../../instructions/core_tasks/3.13_follow_up_context.md) → [3.6_publish_article.md](../../instructions/core_tasks/3.6_publish_article.md)

---

### Unpublish
**User:** "Take down the old summer event article"

**Intent:** unpublish_article  
**Entities:** article_reference="old summer event article"  
**Expected Flow:** [3.7_unpublish_article.md](../../instructions/core_tasks/3.7_unpublish_article.md)

---

## Delete Requests

### Simple Delete
**User:** "Delete the draft about the spring concert"

**Intent:** delete_article  
**Entities:** article_reference="draft about spring concert"  
**Expected Flow:** [3.5_delete_content.md](../../instructions/core_tasks/3.5_delete_content.md)

---

## Image Requests

### Generate Standalone Image
**User:** "Generate a hero image for the fundraiser campaign"

**Intent:** generate_image  
**Entities:** image_description="fundraiser campaign"  
**Expected Flow:** [3.8_generate_image_standalone.md](../../instructions/core_tasks/3.8_generate_image_standalone.md)

---

### Add Image to Existing Article
**User:** "Add a hero image to the gala article"

**Intent:** add_image_to_article  
**Entities:** article_reference="gala article", image_requested=true  
**Expected Flow:** [3.9_add_hero_image.md](../../instructions/core_tasks/3.9_add_hero_image.md)

---

## Ambiguous/Unclear Requests

### Vague Request
**User:** "article"

**Intent:** unclear  
**Expected Flow:** [4.9_empty_vague_request.md](../../instructions/edge_cases/4.9_empty_vague_request.md)

---

### Missing Topic
**User:** "Create an article"

**Intent:** create_article  
**Entities:** topic=missing  
**Expected Flow:** [3.10_clarification.md](../../instructions/core_tasks/3.10_clarification.md)

---

### Multiple Matches
**User:** "Update the event article"

**Intent:** update_article  
**Entities:** article_reference="event article" (matches 3 articles)  
**Expected Flow:** [4.2_multiple_matches.md](../../instructions/edge_cases/4.2_multiple_matches.md)

---

## Out of Scope Requests

### Static Page
**User:** "Update the About Us page"

**Intent:** out_of_scope  
**Expected Flow:** [4.10_out_of_scope.md](../../instructions/edge_cases/4.10_out_of_scope.md)

---

### Event Calendar
**User:** "Add the concert to the events calendar"

**Intent:** out_of_scope  
**Expected Flow:** [4.10_out_of_scope.md](../../instructions/edge_cases/4.10_out_of_scope.md)

---

## Help Requests

### General Help
**User:** "What can you do?"

**Intent:** help  
**Expected Flow:** [4.15_asking_for_help.md](../../instructions/edge_cases/4.15_asking_for_help.md)

---

### Capabilities
**User:** "help"

**Intent:** help  
**Expected Flow:** [4.15_asking_for_help.md](../../instructions/edge_cases/4.15_asking_for_help.md)
