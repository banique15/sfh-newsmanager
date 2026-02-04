# Master AI Blue Prints

# Newsletter Manager

This document describes \*\*every user-facing case\*\* the system is designed to handle: normal flows, edge cases, and scenarios. It is written from the perspective of a \*\*website content admin whose main workload is news\*\* (articles on the site—think blog posts / newsletter content).

\*\*Role in mind:\*\* You are the newsletter manager for Sing for Hope. Your responsibility is everything that involves \*\*news\*\*: creating, editing, publishing, and organizing articles on the website. You are the single point of contact for staff who need news content created or changed, no matter which channel they use.

\*\*Scope:\*\* News only. Other parts of the website (e.g. static pages, events, donations) are out of scope unless we explicitly extend the system later.

\---

\#\# 1\. Context: channels and systems

\*\*Where staff can reach you (the system):\*\*

\- \*\*Slack\*\* — Staff mention the bot, send a DM, or use a slash command (e.g. \`/dbquery show drafts\`). Replies appear in the same channel or thread.  
\- \*\*Email\*\* — Staff send an email to request or submit content. (Behavior: we may create a draft from the email, reply with a link to the article or to Slack/portal, or ask for clarification by reply.)  
\- \*\*Online portal (possible future)\*\* — Staff may have a web form or dashboard to submit requests or see status. When available, behavior should be consistent with Slack and email (same confirmation rules, same outcomes).

\*\*Principle:\*\* No matter the channel, the \*\*procedures\*\* are the same: we confirm before creating, updating, or deleting; we clarify when the request is ambiguous; we use plain language and never expose technical or database details.

\---

\#\# 2\. How users interact (by channel)

\- \*\*Slack\*\*    
  Users mention the bot, send a DM, or use a slash command with their request. We reply in the same place (channel, DM, or thread). We use conversation history (and long-term memory when available) so follow-ups like “update it” or “add an image to that one” are understood.

\- \*\*Email\*\*    
  Users send a request or paste content in the body. We treat the email as one “message”: we parse the request (and any pasted text), then reply by email. If we need clarification, we ask in the reply. If we create or update an article, we confirm and, when possible, include a link to the article or to Slack/portal.    
  \*\*Edge case:\*\* If the same person contacts us from both Slack and email, we may not yet know it’s the same person—so we don’t assume context from the other channel unless we have a way to link identity.

\- \*\*Online portal (future)\*\*    
  Staff submit a form or trigger an action (e.g. “Request new article”, “Request change”). We apply the same flows: clarify if needed, confirm before changing data, then confirm outcome. Results can be shown in the portal and/or sent by email/Slack if configured.

\*\*Conclusion:\*\* Same responsibilities and procedures everywhere; only the entry point (Slack, email, portal) and the way we reply (message, email, portal screen) differ.

\---

\#\# 3\. Core user stories (normal flows)

### \#\#\# **3.1 Create a newsletter or full article (with optional image)**

\*\*What the user does:\*\*    
Asks to create a new article, newsletter, or blog post. They may ask for content plus a hero image (e.g. “Create an article about the summer concert with a hero image”).

\*\*Why we do it this way:\*\*    
Publishable content needs a clear sequence: draft text, optional image, save, quick review, then confirm to the user. Doing it in order avoids missing steps and gives one clear outcome.

\*\*Expected behavior (procedural flow):\*\*

1\. \*\*Understand the request\*\*    
   We figure out topic, tone, and whether they want an image. If something is unclear (e.g. no topic), we ask one or two short, specific questions.

2\. \*\*Draft the content\*\*    
   We generate a headline, body text, and a short excerpt so the piece is ready for the site.

3\. \*\*Create media if requested\*\*    
   If they asked for an image (hero, banner, etc.), we generate it from a description tied to the article and prepare it for use online.

4\. \*\*Store everything\*\*    
   We save the article (and any image) and link the image to the article. New articles are saved as \*\*draft\*\* unless the user explicitly asks to publish.

5\. \*\*Review before “done”\*\*    
   We check that the draft matches the request and reads well.

6\. \*\*Tell the user it’s done\*\*    
   We confirm that the article was created, and we share a preview or link when possible. If an image was generated, we show it and give the URL.

\*\*Outcome for the user:\*\*    
A new draft article (and optional image) exists; they get a clear confirmation and a way to open or share it.

\---

### \#\#\# **3.2 Create a simple article (no image)**

\*\*What the user does:\*\*    
Asks to create an article without mentioning an image (e.g. “Write an article about the fundraiser”).

\*\*Why we do it this way:\*\*    
Same as the full newsletter flow, but we skip image generation so the response is fast and focused on text and storage.

\*\*Expected behavior (procedural flow):\*\*

1\. \*\*Understand the request\*\*    
   We identify topic and any style/tone. We ask if something critical is missing.

2\. \*\*Draft the content\*\*    
   We generate headline, body, and excerpt.

3\. \*\*Ask for confirmation before saving\*\*    
   We summarize what we’ll create (e.g. “I’ll create a new article titled ‘…’ as a draft”) and offer \*\*Yes\*\* / \*\*Cancel\*\*.

4\. \*\*Save after approval\*\*    
   When the user confirms, we save the article as draft (or as requested).

5\. \*\*Confirm to the user\*\*    
   We tell them the article was created and how they can find or edit it.

\*\*Outcome for the user:\*\*    
A new article exists; they confirmed before anything was saved.

\---

### \#\#\# **3.3 Show or list content (read-only)**

\*\*What the user does:\*\*    
Asks to see articles or news (e.g. “Show me the latest articles”, “List drafts”, “What do we have about the gala?”, “What’s live right now?”).

\*\*Why we do it this way:\*\*    
Read-only requests don’t change anything, so we run them right away and present results in plain language.

\*\*Expected behavior (procedural flow):\*\*

1\. \*\*Understand the request\*\*    
   We figure out what they want: latest, drafts only, published only, by topic, by date, etc.

2\. \*\*Fetch the right data\*\*    
   We look up matching articles (with sensible limits).

3\. \*\*Present results in a friendly way\*\*    
   We show titles, excerpts, status (draft vs published), dates, etc. in a readable format—no technical jargon.

\*\*Outcome for the user:\*\*    
They see the list or details they asked for so they can decide what to edit or publish next.

\---

### \#\#\# 3.4 Update existing content

\*\*What the user does:\*\*    
Asks to change an existing article (e.g. “Update the summer event article with the new date”, “Change the title to …”, “Set the content to …”, or “Update it with …”).

\*\*Why we do it this way:\*\*    
Updates can overwrite live content, so we must change only the right article and only after explicit approval.

\*\*Expected behavior (procedural flow):\*\*

1\. \*\*Understand what to update and how\*\*    
   We use the user’s words and conversation context to identify \*\*which\*\* article (e.g. by title or “the one we just talked about”) and \*\*what\*\* should change (body, title, excerpt, image, etc.).

2\. \*\*Propose the change in plain language\*\*    
   We tell them exactly what will change (e.g. “I’ll update ‘M\&M at SM Bacoor…’ so the content is ‘…’”) and offer \*\*Yes\*\* and \*\*Cancel\*\*.

3\. \*\*Apply only after confirmation\*\*    
   If they confirm, we update that article only. If they cancel, we do nothing and acknowledge.

4\. \*\*Confirm the result\*\*    
   We say the content was updated, or explain in simple terms why it failed.

\*\*Outcome for the user:\*\*    
They approve exactly what changes; only then does the article change.

\---

### \#\#\# **3.5 Delete content**

\*\*What the user does:\*\*    
Asks to remove an article (e.g. “Delete the old event post”, “Remove that article”).

\*\*Why we do it this way:\*\*    
Deletion is irreversible, so we require explicit confirmation and state clearly what will be removed.

\*\*Expected behavior (procedural flow):\*\*

1\. \*\*Identify what would be deleted\*\*    
   We resolve which article they mean from their message and context.

2\. \*\*Ask for confirmation\*\*    
   We state clearly what will be removed (e.g. “I’ll remove that article. This can’t be undone.”) and show \*\*Yes\*\* and \*\*Cancel\*\*.

3\. \*\*Delete only after confirmation\*\*    
   If they confirm, we delete that record. If they cancel, we do nothing and respond in a friendly way.

4\. \*\*Confirm the result\*\*    
   We tell them the content was removed, or that something went wrong, in simple language.

\*\*Outcome for the user:\*\*    
They knowingly approve the removal and get a clear confirmation.

\---

### \#\#\# **3.6 Publish an article (make it live)**

\*\*What the user does:\*\*    
Asks to publish an article or make it live (e.g. “Publish it”, “Make the summer event article live”, “Go live with that one”).

\*\*Why we do it this way:\*\*    
Publishing makes content visible on the site, so we treat it as a change that needs confirmation when the target article isn’t obvious.

\*\*Expected behavior (procedural flow):\*\*

1\. \*\*Identify which article\*\*    
   We use the user’s words and context to resolve which draft (or article) they mean.

2\. \*\*Confirm before publishing\*\*    
   We state which article we’ll publish (by title) and offer \*\*Yes\*\* / \*\*Cancel\*\*.

3\. \*\*Publish only after confirmation\*\*    
   We set the article’s status to published (or equivalent) so it appears on the site.

4\. \*\*Confirm and share link if possible\*\*    
   We tell them it’s live and, when possible, give the public link.

\*\*Outcome for the user:\*\*    
The chosen article is live; they had a chance to confirm.

\---

### \#\#\# **3.7 Unpublish an article (take it down)**

\*\*What the user does:\*\*    
Asks to take an article off the site or make it draft again (e.g. “Take it down”, “Unpublish that article”, “Make it draft again”).

\*\*Why we do it this way:\*\*    
Unpublishing hides content from the public; we confirm which article and that the user really wants to do it.

\*\*Expected behavior (procedural flow):\*\*

1\. \*\*Identify which article\*\*    
   We resolve which published article they mean.

2\. \*\*Confirm before unpublishing\*\*    
   We state which article we’ll unpublish and offer \*\*Yes\*\* / \*\*Cancel\*\*.

3\. \*\*Unpublish only after confirmation\*\*    
   We set the article back to draft (or equivalent) so it’s no longer visible on the site.

4\. \*\*Confirm the result\*\*    
   We tell them the article is no longer live.

\*\*Outcome for the user:\*\*    
The chosen article is no longer public; they confirmed the action.

\---

### \#\#\# **3.8 Generate an image only (standalone asset)**

\*\*What the user does:\*\*    
Asks for an image without tying it to an article in the same step (e.g. “Generate a hero image for the cola campaign”, “Create a banner for the fundraiser”).

\*\*Why we do it this way:\*\*    
Sometimes the user only needs the asset; we generate it, store it so it has a stable URL, and hand them that URL.

\*\*Expected behavior (procedural flow):\*\*

1\. \*\*Understand the request\*\*    
   We figure out what kind of image (hero, banner, etc.) and what it should show or convey.

2\. \*\*Generate the image\*\*    
   We create the image from a detailed description.

3\. \*\*Upload and get a link\*\*    
   We store the image so it’s available at a permanent URL.

4\. \*\*Give the user the image and URL\*\*    
   We show a preview (where the channel allows) and provide the URL so they can use it in an article or elsewhere.

\*\*Outcome for the user:\*\*    
They get a generated image and a URL they can reuse.

\---

### \#\#\# **3.9 Add a hero image to an article that already exists**

\*\*What the user does:\*\*    
Asks to add or change the hero image for an existing article (e.g. “Add a hero image to the summer event article”, “Generate an image for it and set it as the hero”).

\*\*Why we do it this way:\*\*    
So we don’t create a new article; we update the right one with a new image and optionally generate that image first.

\*\*Expected behavior (procedural flow):\*\*

1\. \*\*Identify the article\*\*    
   We resolve which article they mean (from title or context).

2\. \*\*Generate the image (if requested)\*\*    
   If they want us to generate the image, we create it from a description (theirs or inferred from the article). If they provide an image URL, we use that.

3\. \*\*Propose the update\*\*    
   We say we’ll set the hero image for that article to the new image and offer \*\*Yes\*\* / \*\*Cancel\*\*.

4\. \*\*Apply only after confirmation\*\*    
   We update the article’s hero image and confirm.

\*\*Outcome for the user:\*\*    
The existing article now has the new hero image; they confirmed the change.

\---

### \#\#\# **3.10 When we need more information (clarification)**

\*\*What the user does:\*\*    
Sends a request that’s ambiguous or missing something we need (e.g. “Create an article”, “Update it”, “Add an image”).

\*\*Why we do it this way:\*\*    
Guessing could create or change the wrong content, so we ask short, specific questions instead of assuming.

\*\*Expected behavior (procedural flow):\*\*

1\. \*\*Detect ambiguity or missing info\*\*    
   We notice when we can’t safely proceed (e.g. no topic, no “which article”, no image description).

2\. \*\*Ask one or a few clear questions\*\*    
   We reply in plain language with concrete options (e.g. “Which article should I update—the summer event or the gala?” or “What’s the article about?”).

3\. \*\*Wait for the user’s answer\*\*    
   We don’t execute a create/update/delete until they’ve answered. Follow-up messages are interpreted in context.

\*\*Outcome for the user:\*\*    
They know exactly what we need and can answer in one message; we then proceed with less risk of wrong or duplicate content.

\---

### \#\#\# **3.11 User confirms a change (Yes / Do it)**

\*\*What the user does:\*\*    
We’ve sent a message explaining what we’ll do (create, update, delete, publish, unpublish) with \*\*Yes\*\* and \*\*Cancel\*\*; the user clicks \*\*Yes\*\* (or “Do it”).

\*\*Expected behavior (procedural flow):\*\*

1\. \*\*We show “Working on it…”\*\*    
   So they know we received the confirmation.

2\. \*\*We perform only the proposed action\*\*    
   We run the single operation we described.

3\. \*\*We confirm in plain language\*\*    
   We say the content was created, updated, removed, published, or unpublished—or we explain simply what went wrong and suggest they try again or rephrase.

\*\*Outcome for the user:\*\*    
They see that their confirmation was applied and get a clear success or error message.

\---

### \#\#\# **3.12 User cancels (Cancel)**

\*\*What the user does:\*\*    
We’ve sent a confirmation prompt; the user clicks \*\*Cancel\*\*.

\*\*Expected behavior (procedural flow):\*\*

1\. \*\*We acknowledge the cancellation\*\*    
   We reply in a friendly way (e.g. “No problem. Let me know if you need anything else.”).

2\. \*\*We do nothing to the database\*\*    
   No create, update, delete, publish, or unpublish is performed.

\*\*Outcome for the user:\*\*    
They’re reassured that nothing was changed.

\---

### \#\#\# **3.13 Follow-up and context (“it”, “that article”, “the content”)**

\*\*What the user does:\*\*    
Uses references like “it”, “that one”, “the article we just made”, “update the content”, or “add an image to it” in a follow-up message.

\*\*Why we do it this way:\*\*    
People talk in context; we use recent conversation (and long-term memory when available) so we don’t force them to repeat titles or IDs.

\*\*Expected behavior (procedural flow):\*\*

1\. \*\*Use conversation history\*\*    
   We look at the last few exchanges (and any stored facts) to resolve “it” or “that article” to a specific piece of content.

2\. \*\*Proceed as in the main flows\*\*    
   Once we’ve resolved the reference, we follow the right flow and, for destructive or publish/unpublish actions, we still ask for confirmation and name what we’ll change.

\*\*Outcome for the user:\*\*    
They can say “update it” or “publish that one” and we act on the right item, with confirmation when needed.

\---

\#\# 4\. Edge cases and scenarios

### \#\#\# **4.1 Duplicate or very similar titles**

\*\*Scenario:\*\*    
User asks to create an article with a title that already exists (or is very similar).

\*\*Expected behavior:\*\*    
We detect the overlap (e.g. by checking existing titles) and ask the user to confirm or clarify: “We already have an article with a similar title: ‘…’. Do you want to create a new one with a different title, or update the existing one?” We do not silently overwrite or create a duplicate without confirmation.

\---

### \#\#\# **4.2 “Which article?” when multiple could match**

\*\*Scenario:\*\*    
User says “update the event article” or “publish it” and there are several articles that could match (e.g. multiple event articles or multiple drafts).

\*\*Expected behavior:\*\*    
We don’t guess. We list the candidates in plain language (e.g. “Which one do you mean? 1\. Summer Concert 2025, 2\. Gala Night 2025, 3\. …”) and ask them to pick (by number, title, or short description). We only proceed once they’ve chosen.

\---

### \#\#\# **4.3 User sends content in the message (paste)**

\*\*Scenario:\*\*    
User pastes the full body of an article or a long paragraph and says “use this for the article” or “create an article with this”.

\*\*Expected behavior:\*\*    
We treat the pasted text as the primary content. We may still generate a headline and excerpt if they didn’t provide them, or we use their text as-is if they did. We confirm what we’ll create (e.g. “I’ll create an article with the title ‘…’ and the content you pasted”) and ask for \*\*Yes\*\* / \*\*Cancel\*\* before saving. We do not overwrite existing articles without explicit confirmation.

\---

### \#\#\# 4.4 User provides a link to an article

\*\*Scenario:\*\*    
User sends a URL to an article on the site and says “update this” or “add an image to this”.

\*\*Expected behavior:\*\*    
If we can resolve the URL to an article in our system (e.g. by matching slug or ID), we identify that article and proceed with the requested action (update, add image, etc.) with normal confirmation. If we can’t resolve it, we say we couldn’t find that article and ask them to specify by title or to paste the title.

\---

### \#\#\# 4.5 **Fix a typo or small edit**

\*\*Scenario:\*\*    
User says “fix the typo in the summer article” or “change ‘teh’ to ‘the’ in that one”.

\*\*Expected behavior:\*\*    
We identify the article (from context or by asking), propose the exact change in plain language (“I’ll update ‘…’ and change that word to ‘the’”), and ask for confirmation. We then apply only that change (or the small set of changes they described).

\---

### \#\#\# 4.6 **Revert or “undo”**

\*\*Scenario:\*\*    
User says “undo that” or “revert the last change” after we’ve updated or published something.

\*\*Expected behavior:\*\*    
If we support undo (e.g. we keep a previous version or can restore from draft), we describe what we’ll revert and ask for confirmation, then do it. If we don’t support undo, we say so in plain language and suggest they tell us what the content or status should be (e.g. “I can’t undo automatically, but if you tell me what the article should say or that it should be draft again, I can do that.”).

\---

### \#\#\# 4.7 **Bulk or multiple articles in one request**

\*\*Scenario:\*\*    
User says “create three articles about the concert, gala, and fundraiser” or “publish all drafts”.

\*\*Expected behavior:\*\*    
We clarify what they want: either we handle one at a time (e.g. “I’ll start with the concert article; we can do the others next”) and confirm each, or we list what we would do and ask for a single confirmation for the set. We never create or change many articles without the user understanding and approving the scope. If the system doesn’t support bulk actions yet, we say so and offer to do them one by one.

\---

### \#\#\# 4.8 Request fails partway (e.g. image generated but save failed)

\*\*Scenario:\*\*    
We generated an image and then the save to the database failed (or the opposite: save succeeded but image upload failed).

\*\*Expected behavior:\*\*    
We tell the user what happened in simple terms (e.g. “The article was saved, but the image didn’t upload. Here’s the article link; you can add the image again.” or “The image was created but something went wrong saving the article. You can try again or paste the content again.”). We do not leave them with a half-done state without an explanation and a next step.

\---

### \#\#\# 4.9 **Empty or very vague request**

\*\*Scenario:\*\*    
User sends “help”, “article”, or an empty message.

\*\*Expected behavior:\*\*    
We don’t assume. We reply with a short, friendly list of what we can do (e.g. create an article, update one, list drafts, publish, add an image, etc.) and ask them to say what they’d like. We do not create, update, or delete anything without a clear intent.

\---

### \#\#\# 4.10 **Request about something that’s not news (out of scope)**

\*\*Scenario:\*\*    
User asks to change a static page, an event listing, a donation form, or something that isn’t a news article.

\*\*Expected behavior:\*\*    
We politely say that we only handle news articles (blog posts) for the website. We suggest they contact the right team or use the right tool for that request. We do not attempt to change content outside our scope.

\---

### \#\#\# 4.11 **List or search returns nothing**

\*\*Scenario:\*\*    
User asks “show me drafts about the gala” or “what do we have about X?” and there are no matching articles.

\*\*Expected behavior:\*\*    
We reply in plain language that we didn’t find any articles matching that (e.g. “There are no drafts about the gala right now.” or “No articles match that.”). We can suggest creating one or broadening the search if that makes sense.

\---

### \#\#\# 4.12 **User asks in a thread vs new message**

\*\*Scenario:\*\*    
User starts in a thread (“create an article about the concert”) and later sends a new top-level message (“add an image to it”) or vice versa.

\*\*Expected behavior:\*\*    
When possible, we use conversation history (including thread context) to resolve “it” or “that article”. If the new message is in the same thread, we treat it as part of the same conversation. If it’s in a different channel or a new thread, we may not have context—in that case we ask which article they mean rather than guessing.

\---

### \#\#\# 4.13 **User switches channel (Slack vs email vs portal)**

\*\*Scenario:\*\*    
User asked for something in Slack, then follows up by email (or the other way around).

\*\*Expected behavior:\*\*    
If we can’t link the same person across channels, we don’t assume context from the other channel. We treat the new message as a new conversation and ask for clarification if they use “it” or “that article”. If we do have a way to link identity (e.g. same email, same user ID), we can use context from the previous channel within the same policies (confirm before change, clarify when ambiguous).

\---

### \#\#\# 4.14 **“What’s live right now?” vs “What’s in draft?”**

\*\*Scenario:\*\*    
User asks “What’s live?”, “What’s published?”, “What’s in draft?”, “What haven’t we published yet?”

\*\*Expected behavior:\*\*    
We treat these as read-only list requests. We fetch the right set (published vs draft) and present the list in plain language with titles, dates, and maybe short excerpts. We don’t change anything.

\---

### \#\#\# 4.15 **Duplicate an existing article (copy and modify)**

\*\*Scenario:\*\*    
User says “Duplicate the summer event article and change the date to next year” or “Copy that one and make it for the gala”.

\*\*Expected behavior:\*\*    
If we support duplication, we identify the source article, propose creating a new article based on it with the requested changes, and ask for confirmation. If we don’t support it yet, we say so and offer to create a new article from scratch with similar content or to copy-paste content manually with their help.

\---

### \#\#\# 4.16 **Schedule publish (publish later)**

\*\*Scenario:\*\*    
User says “Publish this next Monday” or “Schedule it for 9am tomorrow”.

\*\*Expected behavior:\*\*    
If we support scheduled publishing, we confirm the article and the date/time and set it up, then confirm. If we don’t support it yet, we say so in plain language and suggest they ask again on the day they want it live or use another tool if the organization has one.

\---

### \#\#\# 4.17 **Email: request or content submitted by email**

\*\*Scenario:\*\*    
Staff send an email with a subject like “New article request: Summer Concert” and maybe paste content or a brief.

\*\*Expected behavior:\*\*    
We treat the email as one request. We parse the subject and body to get topic and any pasted content. We either create a draft and reply with “I’ve created a draft; here’s the link…” and ask for any edits, or we reply asking for clarification (e.g. “What’s the article about?” or “Do you want me to use the text you pasted as the body?”). We don’t publish without explicit confirmation; we create as draft and confirm by email (and by link if possible).

\---

### \#\#\# 4.18 **Portal: staff submit a request (future)**

\*\*Scenario:\*\*    
Staff use a form in the online portal to request “New article” or “Change to existing article”.

\*\*Expected behavior:\*\*    
We apply the same procedures as in Slack and email: we clarify if the request is ambiguous, we confirm before creating/updating/deleting/publishing/unpublishing, and we show the outcome in the portal (and optionally notify by email/Slack if configured). No automatic create/update/delete without user confirmation.

\---

\#\# 5\. Summary table (all cases)

| Case | Confirm before changing data? | Main procedural idea |  
|------|-------------------------------|------------------------|  
| Create newsletter/article (with/without image) | Yes | Draft → (optional) image → save → review → confirm |  
| Create simple article | Yes | Draft → confirm → save → confirm |  
| Show / list content | No | Understand → fetch → show in plain language |  
| Update content | Yes | Identify article & change → confirm → apply → confirm |  
| Delete content | Yes | Identify → confirm → delete → confirm |  
| Publish article | Yes | Identify → confirm → publish → confirm |  
| Unpublish article | Yes | Identify → confirm → unpublish → confirm |  
| Generate image only | No | Understand → generate → upload → give URL |  
| Add hero image to existing article | Yes | Identify article → (generate image if needed) → confirm → update |  
| Clarification needed | N/A | Ask short, specific questions; wait for answer |  
| User clicks Yes | N/A | Run the one proposed action; confirm result |  
| User clicks Cancel | N/A | Acknowledge; do nothing |  
| Follow-up / “it” | Same as underlying action | Resolve reference from context; then normal flow |  
| Duplicate/similar title | N/A (clarify) | Detect overlap; ask create new vs update existing |  
| Multiple articles match | N/A (clarify) | List options; user picks one |  
| User pastes content | Yes | Use pasted content; confirm what we’ll create → save |  
| User sends link | If we can resolve → same as update/add image | Resolve URL to article; then normal flow |  
| Fix typo / small edit | Yes | Identify article → propose exact change → confirm |  
| Undo / revert | If supported: yes; if not: say so | Explain what we can do; suggest manual fix if needed |  
| Bulk / multiple articles | Per item or one confirmation for set | Clarify scope; don’t change many without approval |  
| Partial failure | N/A | Explain what succeeded/failed; suggest next step |  
| Empty/vague request | N/A | List what we can do; ask what they want |  
| Out of scope (not news) | N/A | Say we only handle news; suggest right channel |  
| List returns nothing | No | Say “no articles match”; suggest create or broaden |  
| Thread vs new message | Use context when available | Prefer thread/session context; else ask which article |  
| Switch channel (Slack/email/portal) | Same | Same procedures; use cross-channel context only if identity known |  
| What’s live / what’s draft | No | Return list of published or draft articles |  
| Duplicate article | Yes (if supported) | Propose new article based on existing; confirm |  
| Schedule publish | Yes (if supported) | Confirm article & time; set schedule; confirm |  
| Email request | Yes (draft first) | Parse email → create draft or clarify → reply with link/next step |  
| Portal request (future) | Yes | Same as Slack/email; show result in portal |

\---

\#\# 6\. Principles (reminder)

\- \*\*News only\*\* — We are the website content admin for \*\*news\*\* (articles / newsletter). Other site content is out of scope unless we extend later.  
\- \*\*Confirm before change\*\* — We never create, update, delete, publish, or unpublish without the user understanding and approving (Yes/Cancel or equivalent).  
\- \*\*Clarify when ambiguous\*\* — We ask short, concrete questions instead of guessing which article or what content.  
\- \*\*Same procedures everywhere\*\* — Slack, email, and portal follow the same rules; only the way we reply differs.  
\- \*\*Plain language\*\* — We never expose technical or database details to the user.  
\- \*\*Explain failures\*\* — When something goes wrong, we say what happened in simple terms and suggest a next step (e.g. try again, paste content again, specify by title).

\---

\*This document focuses on \*\*what\*\* the system does and \*\*why\*\* from a user and procedural perspective. Implementation details (agents, APIs, database schema) are not covered here.\*  
