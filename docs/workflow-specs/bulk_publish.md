# Workflow: Bulk Publish

**ID:** `bulk_publish`  
**Type:** Multi-step orchestration  
**Blueprint Reference:** Edge Case 4.7

---

## Overview

Publishes multiple articles at once with explicit confirmation of full list.

**User Request Example:**  
> "Publish all drafts"

---

## Steps

### 1. Parse Intent & Criteria

**Tool:** `intent_detection`

**Extract:**
- Bulk operation: publish
- Filter criteria: "all drafts", "all about X", etc.

---

### 2. Fetch Matching Articles

**Tool:** `article_search`

**Input:**
```json
{
  "status": "draft",
  "keyword": "[if topic specified]",
  "limit": 50
}
```

**Output:**
- List of matching articles

**If no matches:**
- Use edge case 4.11 (no results)
- Exit workflow

---

### 3. Show List and Confirm

**Tool:** `yes_no_prompt`

**Message:**
```
This will publish the following [N] articles and make them live on the website:

1. [Title 1] - draft - created [date]
2. [Title 2] - draft - created [date]
3. [Title 3] - draft - created [date]
...

Total: [N] articles

Are you sure you want to proceed?
```

**Buttons:** [Yes, Publish All] [Cancel]

**Important:** Always show complete list, never "and X more..."

---

### 4. Wait for User Response

**On Yes:** Continue to step 5  
**On Cancel:** Exit workflow

---

### 5. Publish Each Article

**Loop through each article:**

**Tool:** `article_status`

**Input:**
```json
{
  "operation": "publish",
  "article_id": "[article_id]"
}
```

**Track:**
- Successfully published: count
- Failed: count and IDs
- Total processed: count

**Continue on individual failures** (don't abort entire operation)

---

### 6. Report Results

#### Full Success
```
✅ Published [N] articles!

All articles are now live on the website.

[Optional: Show first 5 URLs]
```

#### Partial Success
```
Published [X] of [N] articles.

✅ Successfully published:
1. [Title A]
2. [Title B]
...

❌ Failed to publish:
1. [Title X] - [reason]
2. [Title Y] - [reason]

The successful articles are live. Want me to retry the failed ones?
```

#### Complete Failure
```
None of the articles could be published.

Error: [common error if applicable]

Want to try again?
```

#### Cancellation
```
No problem. No articles were published.

Let me know if you need anything else.
```

---

## Safety Limits

### Maximum Articles
- Limit: 50 articles per bulk operation
- If more than 50 match:
  ```
  There are [total] articles matching your criteria.
  
  Bulk operations are limited to 50 articles at a time.
  
  Please narrow your criteria, or let me know which specific ones to publish.
  ```

### Timeout Protection
- If operation takes > 60 seconds
- Report progress so far
- Offer to continue remaining items

---

## Error Handling

### Search Failure
- Report error
- Exit workflow
- Suggest trying again

### Individual Publish Failures
- Continue with remaining articles
- Track failures
- Report summary at end

### Bulk Timeout
- Report what succeeded
- Report what's pending
- Offer to continue

---

## State Management

Store in `conversation_memory`:
- List of article IDs to publish
- Progress: [published_ids], [failed_ids]
- Total count
- Start time

Clear after reporting results.

---

## Alternative: Bulk Unpublish

Same workflow structure, but:
- Filter: `status: "published"`
- Operation: `unpublish`
- Warning level: higher (removing from public site)

---

## Alternative: Bulk Delete

**⚠️ DANGER LEVEL: CRITICAL**

Same workflow but with additional safeguards:
- Red/danger styling on confirmation
- Explicit warning about permanence
- Require typing "DELETE" to confirm (future enhancement)
- Show full article details in list (not just titles)

---

## Estimated Duration

- **Per article:** ~1-2 seconds
- **10 articles:** 10-20 seconds
- **50 articles:** 50-100 seconds
- **User response time:** Variable

---

## Success Metrics

- Articles processed: Count
- Successful operations: Count
- Failed operations: Count
- Success rate: Percentage
- Total duration: Seconds
