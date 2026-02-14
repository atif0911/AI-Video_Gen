import os
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_thumbnail(project_id, topic, title):
    print(f"🖼️ Generating Thumbnail for Project {project_id}...")
    
    # 1. Fetch a Background Image (Using Pollinations for variety/AI art)
    # It's easier than Pexels for static images and requires no API key for this specific URL
    image_url = f"https://image.pollinations.ai/prompt/hyper-realistic {topic} cinematic lighting 4k?width=1280&height=720"
    
    save_path = f"static/output/{project_id}/thumbnail.jpg"
    
    try:
        # Download Image
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
        else:
            return None

        # 2. Open Image & Apply Blur (to make text pop)
        img = Image.open(save_path)
        img = img.filter(ImageFilter.GaussianBlur(2)) # Slight blur
        
        # 3. Draw Text
        draw = ImageDraw.Draw(img)
        
        # Try to load a font (Windows usually has Arial)
        try:
            font = ImageFont.truetype("arial.ttf", 80)
        except:
            font = ImageFont.load_default() 

        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (img.width - text_width) / 2
        y = (img.height - text_height) / 2
        
        draw.text((x+5, y+5), title, font=font, fill="black")
        draw.text((x, y), title, font=font, fill="white", stroke_width=2, stroke_fill="black")
        
        img.save(save_path)
        print(f"✅ Thumbnail saved: {save_path}")
        return save_path

    except Exception as e:
        print(f"❌ Thumbnail Error: {e}")
        return None