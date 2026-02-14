import requests
import os
import random
from dotenv import load_dotenv

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def search_pexels_video(query, orientation="landscape", size="medium"):
    headers = {
        "Authorization": PEXELS_API_KEY
    }

    url = f"https://api.pexels.com/videos/search?query={query}&orientation={orientation}&size={size}&per_page=5"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            videos = data.get("videos",[])

            if not videos:
                print(f"No videos found for: {query}")
                return None
            video = random.choice(videos)

            video_files = video.get("video_files",[])
            best_file = None
            for f in video_files:
                if f['file_type'] == 'video/mp4' and f['width'] >= 1280:
                    best_file = f
                    break
            
            if not best_file:
                best_file = video_files[0]
                
            return best_file['link']
        else:
            print(f" Pexels API Error: {response.status_code}")
            return None

        
    except Exception as e:
        print(f"Error searching Pexels: {e}")
        return None

def download_video(url, output_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            return True
        return False
    except Exception as e:
        print(f"Download failed: {e}")
        return False
    
def fetch_visuals(script_data, project_id):
    visual_paths = []
    output_dir = f"static/output/{project_id}/visuals"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Fetching visuals for Project {project_id}...")
    
    for i, scene in enumerate(script_data):
        query = scene['visual_query']
        print(f"   🔍 Searching: '{query}'")
        
        video_url = search_pexels_video(query)
        
        if video_url:
            filename = os.path.join(output_dir, f"scene_{i}.mp4")
            success = download_video(video_url, filename)
            if success:
                visual_paths.append(filename)
            else:
                visual_paths.append(None)
        else:
            print(f"   Could not find video for scene {i}")
            visual_paths.append(None)
            
    print(f"Fetched {len(visual_paths)} video clips!")
    return visual_paths

if __name__ == "__main__":
    test_script = [{"visual_query": "cyberpunk city night rain"}]
    fetch_visuals(test_script, "test_001")