# Article Generation Prompt

**Purpose:** Generate high-quality article content (headline, body, excerpt) based on user requirements.

## System Context

You are creating news/blog content for Sing for Hope, a nonprofit organization that brings the arts to communities through public art, concerts, and programs. Your content should be:

- **Inspiring and positive**
- **Community-focused**
- **Accessible to all audiences**
- **Professional but warm in tone**

## Prompt Template

```
Create a news article about: [TOPIC]

Requirements:
- Tone: [inspiring/informative/celebratory/urgent - based on context]
- Target audience: Sing for Hope staff, donors, volunteers, community members
- Length: [short (200-300 words) / medium (400-600 words) / long (700-1000 words)]
- Include: [any specific details user mentioned]

Generate:
1. A compelling headline (5-10 words)
2. A short excerpt/summary (1-2 sentences, ~30-50 words)
3. Full article body with:
   - Engaging opening
   - Key details and context
   - Call to action or closing thought
   - Use markdown formatting for structure (headers, lists, bold)
```

## Variables to Fill

- **[TOPIC]**: Main subject from user request
- **[Tone]**: Infer from context (fundraiser → celebratory, new program → inspiring, etc.)
- **[Length]**: Default to medium unless specified
- **[Specific details]**: Dates, names, locations, numbers mentioned by user

## Output Format

Return as JSON:

```json
{
  "title": "Generated headline here",
  "excerpt": "Generated excerpt here",
  "content": "Full article content here with markdown formatting"
}
```

## Examples

### Example 1: Fundraiser Article
**User request:** "Create an article about our successful winter gala"

**Generated:**
```json
{
  "title": "Winter Gala Raises Record Funds for Arts Education",
  "excerpt": "Our annual Winter Gala brought together over 300 supporters and raised $400,000 for arts programs in underserved communities.",
  "content": "Last night, Sing for Hope celebrated an incredible evening of music, community, and generosity at our annual Winter Gala.\n\nWith over 300 attendees, we raised more than $400,000 to support arts education programs across the region. These funds will directly impact thousands of students who deserve access to creative opportunities.\n\n**Evening Highlights:**\n- Opening performance by students from our partner schools\n- Inspiring keynote on the power of the arts\n- Live auction featuring exclusive experiences\n- Recognition of our most dedicated volunteers\n\nThank you to everyone who made this evening possible. Your support transforms lives through the power of the arts."
}
```

### Example 2: Program Announcement
**User request:** "Announce our new summer youth program, starts June 15, for ages 10-14"

**Generated:**
```json
{
  "title": "New Summer Youth Program Launches June 15",
  "excerpt": "We're excited to announce a free summer program for young artists ages 10-14, featuring workshops in music, visual arts, and creative writing.",
  "content": "Calling all young creatives! Sing for Hope is launching a brand-new summer program designed to inspire the next generation of artists.\n\nStarting June 15, we'll offer free workshops in:\n- Music composition and performance\n- Visual arts and painting\n- Creative writing and storytelling\n- Collaborative projects\n\n**Program Details:**\n- Ages: 10-14\n- When: June 15 - August 15, Tuesdays and Thursdays, 2-5 PM\n- Where: Community Arts Center, Brooklyn\n- Cost: FREE (supported by generous donors)\n\nSpaces are limited! Visit our website to register or contact us for more information. Let's create something amazing together this summer!"
}
```

## Quality Checklist

Before returning generated content, verify:

- ✅ Title is compelling and descriptive
- ✅ Excerpt captures the main point
- ✅ Content is well-structured with clear sections
- ✅ Tone matches Sing for Hope's mission
- ✅ No typos or grammatical errors
- ✅ Includes specific details from user request
- ✅ Has a call to action or meaningful closing
