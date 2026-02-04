# Workflow: Update and Publish

**ID:** `update_and_publish`  
**Type:** Multi-step orchestration  
**Blueprint Reference:** Tasks 3.4 + 3.6

---

## Overview

Updates an existing article and immediately publishes it in a single user request.

**User Request Example:**  
> "Update the gala article with the new date October 20th and publish it"

---

## Steps

### 1. Parse Intent & Identify Article

**Tool:** `intent_detection`, `context_resolution`

**Extract:**
- Article reference
- What to update
- New value
- Publish intent

**Resolve article reference:**
- Use `context_resolution` if pronoun ("it", "that one")
- Use `article_search` if title/keyword

**If multiple matches:**
- Use `clarification_prompt` with numbered list
- Wait for response

**If not found:**
- Use `clarification_prompt`: "Which article do you mean?"
- Wait for response

---

### 2. Fetch Current Article

**Tool:** `article_crud`

**Input:**
```json
{
  "operation": "read",
  "article_id": "[resolved_id]"
}
```

**Output:**
- Current article data
- Current status (draft/published)

---

### 3. Show Update Confirmation

**Tool:** `yes_no_prompt`

**Message:**
```
I'll update '[ARTICLE_TITLE]' so the [field] is '[new_value]', then publish it and make it live on the website.

Current status: [draft or published]

Is this correct?
```

**Buttons:** [Yes] [Cancel]

---

### 4. Wait for User Response

**On Yes:** Continue to step 5  
**On Cancel:** Exit workflow

---

### 5. Apply Update

**Tool:** `article_crud`

**Input:**
```json
{
  "operation": "update",
  "article_id": "[article_id]",
  "data": {
    "[field_to_update]": "[new_value]"
  }
}
```

**Output:**
- Updated article data
- Update timestamp

**On failure:**
- Use `error_handler`
- Report failure
- Exit workflow (don't proceed to publish)

---

### 6. Publish Article

**Tool:** `article_status`

**Input:**
```json
{
  "operation": "publish",
  "article_id": "[article_id]"
}
```

**Output:**
- Published article
- Public URL
- Published timestamp

**On failure:**
- Report partial success (updated but not published)
- Offer to retry publish

---

### 7. Report Success

#### Full Success
```
✅ Updated and published '[ARTICLE_TITLE]'!

Public URL: [website_url]

The article is now live with your changes.
```

#### Partial Success (updated but publish failed)
```
✅ Updated '[ARTICLE_TITLE]', but publishing failed.

The changes are saved, but the article is still [draft/published with old content].

Want me to try publishing again?
```

#### Cancellation
```
No problem. No changes were made.

Let me know if you need anything else.
```

---

## Error Handling

### Article Not Found
- Clear message: "I couldn't find that article"
- Suggest listing articles to find it

### Update Failure
- Report what went wrong
- Don't proceed to publish
- Offer to retry update

### Publish Failure (after successful update)
- Report partial success
- Note that changes are saved
- Offer to retry just the publish step

### Already Published with Same Content
- Note that update was applied
- Confirm article is already live
- No need to publish again

---

## State Management

Store in `conversation_memory`:
- Article ID being updated
- Original values (for potential rollback context)
- Update applied: Yes/No
- Published: Yes/No

---

## Variations

### Update Only (No Publish)
Follow steps 1-5, skip steps 6-7

### Publish Only (No Update)
Skip steps 1, 3, 5 - just confirm and publish

---

## Estimated Duration

- **Fast path:** 5-10 seconds
- **With failures:** 15-30 seconds
- **User response time:** Variable

---

## Success Metrics

- Article updated: Yes/No
- Article published: Yes/No
- Both operations successful: Yes/No
- Errors encountered: Count
