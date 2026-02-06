from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import markdown
import logging

from src.agents.state import state_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Dashboard")

app = FastAPI(title="Newsletter Manager Dashboard")

@app.get("/")
def home():
    return {"status": "online", "message": "Newsletter Manager Dashboard is running"}

@app.get("/preview/pending/{thread_ts}", response_class=HTMLResponse)
def preview_pending_action(thread_ts: str):
    """
    Render a preview of a pending action (e.g., Create Article).
    """
    action = state_manager.get_pending_action(thread_ts)
    
    if not action:
        return """
        <html>
            <head><title>No Pending Action</title></head>
            <body style="font-family: sans-serif; text-align: center; padding: 50px;">
                <h1>⚠️ No Pending Action Found</h1>
                <p>There is no pending action for this thread, or it has already been processed.</p>
            </body>
        </html>
        """

    tool_name = action.get("tool_name", "")
    args = action.get("tool_args", {})
    
    # We mainly preview 'Create Article' or 'Update Article'
    # If it's something else, we show a generic view
    
    title = args.get("title", "Untitled")
    content = args.get("content", args.get("body", "No content available."))
    image_url = args.get("image_url", "")
    
    # Convert Markdown content to HTML
    try:
        html_content = markdown.markdown(content)
    except:
        html_content = f"<pre>{content}</pre>"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Preview: {title}</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; color: #333; }}
            h1 {{ font-size: 2.5em; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            .hero-image {{ width: 100%; max-height: 400px; object-fit: cover; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            .metadata {{ background: #f9f9f9; padding: 10px; border-radius: 5px; font-size: 0.9em; color: #666; margin-bottom: 20px; }}
            .content {{ font-size: 1.1em; }}
            .badge {{ display: inline-block; padding: 3px 8px; border-radius: 3px; background: #e0e0e0; font-size: 0.8em; margin-right: 5px; }}
            .badge-action {{ background: #d4e1f5; color: #2b5797; }}
        </style>
    </head>
    <body>
        <div class="metadata">
            <span class="badge badge-action">ACTION: {tool_name}</span>
            <span>Thread ID: {thread_ts}</span>
        </div>
        
        {f'<img src="{image_url}" class="hero-image" alt="Hero Image">' if image_url else ''}
        
        <h1>{title}</h1>
        
        <div class="content">
            {html_content}
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
