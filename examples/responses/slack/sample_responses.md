# Slack Response Examples

## Article Created Successfully

```json
{
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "✅ Created *'Annual Gala 2026 - Save the Date'* as a draft."
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "<https://app.singforhope.org/admin/articles/42|View article>"
      }
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "You can publish it, edit it, or add a hero image. Need anything else?"
        }
      ]
    }
  ]
}
```

---

## Confirmation Prompt (Yes/Cancel)

```json
{
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "I'll create a new article titled *'Summer Concert Series 2026'* as a draft.\n\nThe article will cover the summer concert series in Central Park.\n\nIs this correct?"
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "Yes"
          },
          "style": "primary",
          "value": "confirm_create_article_42",
          "action_id": "confirm_action"
        },
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "Cancel"
          },
          "value": "cancel_create_article",
          "action_id": "cancel_action"
        }
      ]
    }
  ]
}
```

---

## Publish Confirmation (Warning Style)

```json
{
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "I'll publish *'Annual Gala 2026 - Save the Date'* and make it live on the website.\n\nCurrently a draft.\n\nIs this correct?"
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "Yes, Publish"
          },
          "style": "primary",
          "value": "confirm_publish_42",
          "action_id": "confirm_publish"
        },
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "Cancel"
          },
          "value": "cancel_publish",
          "action_id": "cancel_action"
        }
      ]
    }
  ]
}
```

---

## Delete Confirmation (Danger Style)

```json
{
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "⚠️ I'll permanently delete *'Old Event Post 2023'* (currently published).\n\n*This can't be undone.*\n\nAre you sure?"
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "Yes, Delete"
          },
          "style": "danger",
          "value": "confirm_delete_38",
          "action_id": "confirm_delete"
        },
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "Cancel"
          },
          "value": "cancel_delete",
          "action_id": "cancel_action"
        }
      ]
    }
  ]
}
```

---

## Article List

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "Found 3 articles about the gala:"
      }
    },
    {
      "type": "divider"
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*📝 DRAFT: Gala Night 2026 - Save the Date*\nJoin us for our annual fundraising gala on October 15, 2026...\n• Created: Feb 4, 2026"
      },
      "accessory": {
        "type": "button",
        "text": {
          "type": "plain_text",
          "text": "View"
        },
        "value": "view_42",
        "action_id": "view_article"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*✅ PUBLISHED: Gala Night 2025 Recap*\nOur annual gala was a tremendous success...\n• Published: Nov 21, 2025\n<https://singforhope.org/news/gala-night-2025-recap|View on website>"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*📝 DRAFT: Gala Planning Committee Update*\nWe're excited to announce our planning committee...\n• Created: Jan 15, 2026"
      }
    }
  ]
}
```

---

## Clarification - Multiple Matches

```json
{
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "Which one?\n\n1. *Summer Concert Series 2026* - draft - created Feb 4\n2. *Summer Fundraiser Event* - published - published Jan 15\n3. *Summer Youth Program Launch* - draft - created Feb 1\n\nPlease choose by number or title."
      }
    }
  ]
}
```

---

## Error - Partial Failure

```json
{
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "The article *'Summer Concert 2026'* was created, but the image didn't generate.\n\n<https://app.singforhope.org/admin/articles/43|View article>\n\nYou can try adding an image again, or let me know if you need help."
      }
    }
  ]
}
```

---

## Out of Scope

```json
{
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "I only handle news articles (blog posts) for the website.\n\nFor changes to static pages like About Us, please contact the web development team.\n\nIs there a news article I can help you with instead?"
      }
    }
  ]
}
```
