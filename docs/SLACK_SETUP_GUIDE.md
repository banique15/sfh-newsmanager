# Slack App Setup Guide

This guide will walk you through setting up a Slack Application for the Newsletter Manager Agent.

## Prerequisite
- You must have a Slack workspace where you have permission to create apps.

## Step 1: Create the App
1. Go to [api.slack.com/apps](https://api.slack.com/apps).
2. Click **Create New App**.
3. Select **From scratch**.
4. **App Name**: `Newsletter Manager`
5. **Pick a workspace**: Select your development workspace.
6. Click **Create App**.

## Step 2: Enable Socket Mode
*Socket Mode allows the app to run locally without exposing a public URL/tunnel.*

1. In the left sidebar, click **Socket Mode**.
2. Toggle **Enable Socket Mode** to ON.
3. **Generate an App-Level Token**:
   - **Token Name**: `Socket Mode Token`
   - **Scopes**: `connections:write` is auto-selected.
   - Click **Generate**.
4. **COPY** the token that starts with `xapp-`.
   - Paste this into your `.env` file as `SLACK_APP_TOKEN`.
   - Click **Done**.

## Step 3: Configure Event Subscriptions
1. In the left sidebar, click **Event Subscriptions**.
2. Toggle **Enable Events** to ON.
3. Scroll down to **Subscribe to bot events**.
4. Click **Add Bot User Event** and add:
   - `app_mention` (Allows bot to hear when mentioned)
   - `message.channels` (Allows bot to hear messages in public channels)
   - `message.im` (Allows bot to hear DMs)
5. Click **Save Changes** at the bottom (important!).

## Step 4: Configure Permissions (Scopes)
1. In the left sidebar, click **OAuth & Permissions**.
2. Scroll down to **Scopes** -> **Bot Token Scopes**.
3. Ensure the following are listed (some may have been added automatically):
   - `app_mention`
   - `channels:history`
   - `chat:write`
   - `im:history`
   - `users:read` (Optional, good for getting user names)
4. Scroll up to **OAuth Tokens for Your Workspace** and click **Install to Workspace**.
5. Click **Allow** on the authorization screen.

## Step 5: Get Bot Token
1. After installation, you will be on the **OAuth & Permissions** page.
2. Under **Bot User OAuth Token**, you will see a token starting with `xoxb-`.
3. **COPY** this token.
   - Paste this into your `.env` file as `SLACK_BOT_TOKEN`.

## Step 6: Get Signing Secret
1. In the left sidebar, click **Basic Information**.
2. Scroll down to **App Credentials**.
3. Find **Signing Secret**.
4. Click **Show** and **COPY** it.
   - Paste this into your `.env` file as `SLACK_SIGNING_SECRET`.

## Step 7: Update .env File
Open your `.env` file in the project root and ensure these lines are filled:

```env
SLACK_BOT_TOKEN=xoxb-your-token-here...
SLACK_APP_TOKEN=xapp-your-token-here...
SLACK_SIGNING_SECRET=your-secret...
```

## Step 8: Invite Bot to Channel
1. Go to your Slack Workspace.
2. Go to the channel you want to test in (e.g., `#testing` or created a new one).
3. Type `/invite @Newsletter Manager`.
4. The bot is now in the channel and ready to listen!
