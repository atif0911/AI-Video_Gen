import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_metadata(topic):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    You are a YouTube SEO expert. 
    Generate metadata for a video about: "{topic}".
    
    Strictly follow this JSON format:
    {{
        "title": "Clickbait style viral title (under 70 chars)",
        "description": "2 sentence description including keywords.",
        "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"]
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"❌ SEO Gen Error: {e}")
        return {
            "title": f"Amazing Facts About {topic}",
            "description": "Watch this video to learn more.",
            "tags": ["education", "ai", "video"]
        }