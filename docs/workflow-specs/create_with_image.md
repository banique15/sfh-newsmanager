# Workflow: Create Article with Image

**ID:** `create_with_image`  
**Type:** Multi-step orchestration  
**Blueprint Reference:** Task 3.1

---

## Overview

Creates a new article with AI-generated hero image in a single user request.

**User Request Example:**  
> "Create an article about the spring fundraiser with a hero image"

---

## Steps

### 1. Parse Intent & Gather Information

**Tool:** `intent_detection`

**Extract:**
- Topic for article
- Image requested: true
- Any specific details provided

**If missing topic:**
- Use `clarification_prompt`: "What should the article be about?"
- Wait for response, then continue

---

### 2. Generate Article Content

**Tool:** `content_generation`

**Input:**
- Topic from user
- Tone: "inspiring" (default)
- Length: "medium" (default)
- Organization context: Sing for Hope

**Output:**
- Generated title
- Generated content (HTML)
- Generated excerpt

---

### 3. Generate Hero Image

**Tool:** `image_generation`

**Input:**
- Description: Based on article topic
- Style: "vibrant" (default for Sing for Hope)
- Aspect ratio: "16:9"
- Organization branding: true

**Output:**
- Image data (base64 or temp URL)

**On failure:**
- Continue to step 4 without image
- Note partial failure for later reporting

---

### 4. Upload Image to Storage

**Tool:** `image_storage`

**Input:**
- Image data from step 3
- Alt text: Generated from topic
- Optimize: true

**Output:**
- Permanent image URL

**On failure:**
- Continue without image
- Note partial failure

---

### 5. Show Confirmation

**Tool:** `yes_no_prompt`

**Message:**
```
I'll create a new article titled '[GENERATED_TITLE]' as a draft with a hero image.

Topic: [user's topic]

Preview:
[First 100 chars of content...]

[Image preview if available]

Is this correct?
```

**Buttons:** [Yes] [Cancel]

---

### 6. Wait for User Response

**On Yes:** Continue to step 7  
**On Cancel:** Exit workflow, use cancellation handler (see step 8)

---

### 7. Create Article in Database

**Tool:** `article_crud`

**Input:**
```json
{
  "operation": "create",
  "data": {
    "news_title": "[generated_title]",
    "news_excerpt": "[generated_excerpt]",
    "newscontent": "[generated_content]",
    "news_image": "[permanent_url or null]",
    "news_image_caption": "[auto-generated]",
    "draft": true,
    "news_author": "Newsletter Manager Bot"
  }
}
```

**Output:**
- Article ID
- Article title
- Admin link

**On failure:**
- Use `error_handler`
- Report failure to user
- Exit workflow

---

### 8. Report Success (or Partial Failure)

#### Full Success
```
✅ Created '[ARTICLE_TITLE]' as a draft with hero image.

[Admin link]

You can publish it, edit it, or make changes. Need anything else?
```

#### Partial Success (article created, image failed)
```
The article '[ARTICLE_TITLE]' was created, but the image didn't generate.

[Admin link]

You can try adding an image again, or let me know if you need help.
```

#### Cancellation
```
No problem. The article wasn't created.

Let me know if you need anything else.
```

---

## Error Handling

### Content Generation Failure
- Ask for more details about topic
- Offer to try again
- Suggest user provides content instead

### Image Generation Failure
- Continue with article creation (mark as partial failure)
- Offer to generate image separately later

### Image Storage Failure
- Continue with article creation (mark as partial failure)
- Note that image can be added later

### Article Creation Failure
- Report clear error message
- Offer to retry
- All previous work (content/image) is lost - note this limitation

---

## State Management

Store in `conversation_memory`:
- Generated content (until article created)
- Generated image URL (until article created)
- Article ID (after creation)
- Workflow status (pending_confirmation, completed, cancelled)

Clear memory after workflow completes or fails.

---

## Estimated Duration

- **Fast path:** 10-15 seconds (all tools succeed)
- **With failures/retries:** 30-60 seconds
- **User response time:** Variable (wait for confirmation)

---

## Success Metrics

- Article created: Yes/No
- Image included: Yes/No
- User confirmation received: Yes/No
- Errors encountered: Count
- Workflow completion time: Seconds
