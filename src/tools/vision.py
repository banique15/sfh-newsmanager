from langchain.tools import tool
import base64
import os
from src.config.llm import get_llm
from langchain_core.messages import HumanMessage

@tool("Analyze Image")
def analyze_image(image_path: str, prompt: str = "Describe this image in detail.") -> str:
    """
    Analyze an image file using an AI vision model.
    Args:
        image_path: The local file path to the image
        prompt: What to ask about the image (default: "Describe this image in detail.")
    """
    if not os.path.exists(image_path):
        return f"Error: Image file not found at {image_path}"
        
    try:
        # Read image and encode to base64
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
            
        # Create multimodal message for Claude/OpenAI
        llm = get_llm()
        
        # Check if model supports vision (Claude Sonnet does)
        # Create LangChain compatible message
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                },
            ]
        )
        
        response = llm.invoke([message])
        return response.content
        
    except Exception as e:
        return f"Error analyzing image: {str(e)}"
