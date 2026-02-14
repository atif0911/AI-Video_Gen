import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

def generate_script(topic):
    print(f" Generating script for topic: {topic}...")
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    You are a professional YouTube video editor. 
    Create a 30-second engaging video script about: "{topic}".
    
    Strictly follow this JSON format (no markdown, no extra text):
    [
        {{
            "visual_query": "specific distinct 3-word visual description for stock footage search",
            "audio_text": "The exact sentence for the voiceover."
        }},
        ...
    ]
    
    Rules:
    1. Total duration should be roughly 40-60 seconds.
    2. 'visual_query' must be a simple, concrete and to the topic search term (e.g., "cyberpunk city night", "fresh coffee beans", "ancient rome colosseum").
    3. 'audio_text' must be engaging and conversational.
    4. Provide 8-10 scenes maximum.
    """
    try:
        response = model.generate_content(prompt)
        raw_text = response.text.replace("```json", "").replace("```","").strip()

        script_data = json.loads(raw_text)
        print("Script generated successfully")
        return script_data
    except Exception as e:
        print(f"Error generating script: {e}")
        return None

if __name__ == "__main__":
    test_topic = "The Mystery of the Pyramids"
    result = generate_script(test_topic)
    import pprint
    pprint.pprint(result)