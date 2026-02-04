# Confirmation Flow Examples

## Create Article Confirmation

### Initial Request
**User:** "Create an article about the spring fundraiser"

### Bot Response (Confirmation)
```
I'll create a new article titled 'Spring Fundraiser 2026' as a draft.

The article will cover the spring fundraiser event and how to participate.

Is this correct?

[Yes] [Cancel]
```

### User Clicks [Yes]

### Bot Response (Success)
```
✅ Created 'Spring Fundraiser 2026' as a draft.

[link to article]

You can publish it, edit it, or add a hero image. Need anything else?
```

---

## Update Article Confirmation

### Initial Request
**User:** "Update the gala article with the new date: October 20th"

### Bot Response (Confirmation)
```
I'll update 'Annual Gala 2026 - Save the Date' so the content includes the new date (October 20th).

Is this correct?

[Yes] [Cancel]
```

### User Clicks [Yes]

### Bot Response (Success)
```
✅ Updated 'Annual Gala 2026 - Save the Date'.

[link to article]

The article is still a draft. Let me know if you'd like to publish it!
```

---

## Publish Article Confirmation

### Initial Request
**User:** "Publish the gala article"

### Bot Response (Confirmation)
```
I'll publish 'Annual Gala 2026 - Save the Date' and make it live on the website.

Currently a draft.

Is this correct?

[Yes, Publish] [Cancel]
```

### User Clicks [Yes, Publish]

### Bot Response (Success)
```
✅ 'Annual Gala 2026 - Save the Date' is now live!

https://singforhope.org/news/annual-gala-2026-save-the-date

The article is visible on the website.
```

---

## Delete Article Confirmation

### Initial Request
**User:** "Delete the old event post"

### Bot Response (Confirmation)
```
⚠️ I'll permanently delete 'Old Event Post 2023' (currently published).

This can't be undone.

Are you sure?

[Yes, Delete] [Cancel]
```

### User Clicks [Yes, Delete]

### Bot Response (Success)
```
✅ Deleted 'Old Event Post 2023'.

The article has been permanently removed from the website.
```

---

## User Cancels

### Initial Request
**User:** "Create an article about the concert"

### Bot Response (Confirmation)
```
I'll create a new article titled 'Concert in the Park' as a draft.

Is this correct?

[Yes] [Cancel]
```

### User Clicks [Cancel]

### Bot Response (Cancelled)
```
No problem. The article wasn't created.

Let me know if you need anything else.
```

---

## Clarification Before Confirmation

### Initial Request
**User:** "Update the event article"

### Bot Response (Clarification - Multiple Matches)
```
Which one?

1. Summer Concert Series 2026 - draft - created Feb 4
2. Summer Fundraiser Event - published - published Jan 15
3. Spring Gala Announcement - draft - created Jan 20

Please choose by number or title.
```

### User Response
**User:** "2"

### Bot Response (Confirmation)
```
I'll update 'Summer Fundraiser Event' with... [what to change]

Is this correct?

[Yes] [Cancel]
```

---

## Follow-Up Context

### Initial Request (Create)
**User:** "Create an article about the piano program"

### Bot Response (Confirmation)
```
I'll create a new article titled '2026 Sing for Hope Pianos' as a draft.

Is this correct?

[Yes] [Cancel]
```

### User Clicks [Yes]

### Bot Response (Success)
```
✅ Created '2026 Sing for Hope Pianos' as a draft.

[link]

You can publish it, edit it, or add a hero image.
```

### Follow-Up Request (Publish)
**User:** "Publish it"

### Bot Response (Confirmation - Resolved "it")
```
I'll publish '2026 Sing for Hope Pianos' and make it live on the website.

Is this correct?

[Yes, Publish] [Cancel]
```

### User Clicks [Yes, Publish]

### Bot Response (Success)
```
✅ '2026 Sing for Hope Pianos' is now live!

https://singforhope.org/news/2026-sing-for-hope-pianos

The article is visible on the website.
```
