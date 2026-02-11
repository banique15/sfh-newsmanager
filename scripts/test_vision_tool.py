from src.tools.vision import analyze_image
import os
import requests

def test_vision():
    # Download a sample image
    img_url = "https://images.unsplash.com/photo-1542206395-9feb3edaa68d"
    img_path = "sample_image.jpg"
    
    with open(img_path, "wb") as f:
        f.write(requests.get(img_url).content)
        
    print(f"Downloaded sample image to {img_path}")
    
    # Test the tool
    print("Analyzing image...")
    # Note: analyze_image is a LangChain tool, so we call .run() or .invoke()
    # But CrewAI tools are often just functions wrapped. 
    # Let's check how it was defined. It used @tool decorator.
    # So we can call it directly or via .run depending on version.
    # The definition returned a StructuredTool.
    
    # Try calling the underlying function if accessible, or run()
    try:
        result = analyze_image.run({"image_path": img_path, "prompt": "What is in this image?"})
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error running tool: {e}")
        
    # Cleanup
    if os.path.exists(img_path):
        os.remove(img_path)

if __name__ == "__main__":
    test_vision()
