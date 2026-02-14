import os
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, ImageClip
from moviepy.video.fx.all import resize
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import textwrap

def assemble_video(project_id, script_data):
    base_dir = f"static/output/{project_id}"
    output_path = os.path.join(base_dir, "final_video.mp4")
    
    final_clips = []
    
    for i, scene in enumerate(script_data):
        audio_path = os.path.join(base_dir, "audio", f"scene_{i}.mp3")
        video_path = os.path.join(base_dir, "visuals", f"scene_{i}.mp4")
        
        if os.path.exists(audio_path) and os.path.exists(video_path):
            audio = AudioFileClip(audio_path)
            video = VideoFileClip(video_path).resize(height=1080)
            
            # Crop to 16:9
            video = video.crop(x1=0, y1=0, width=1920, height=1080, x_center=1920/2, y_center=1080/2)
            
            # Loop/Cut video to match audio
            if video.duration < audio.duration:
                video = video.loop(duration=audio.duration)
            else:
                video = video.subclip(0, audio.duration)
            
            video = video.set_audio(audio)
            
            try:                
                subtitle_text = scene.get("audio_text", "")
                if subtitle_text.strip():
                    img_width = 1800
                    font_size = 60
                    
                    try:
                        font = ImageFont.truetype("arialbd.ttf", font_size)
                    except:
                        font = ImageFont.load_default()

                    wrapped_text = textwrap.fill(subtitle_text, width=40)

                    dummy_img = Image.new("RGB", (img_width, 500), (0, 0, 0))
                    draw = ImageDraw.Draw(dummy_img)
                    text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
                    text_width = text_bbox[2]
                    text_height = text_bbox[3]

                    img_height = text_height + 40
                    img = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
                    draw = ImageDraw.Draw(img)

                    draw.multiline_text(
                        (img_width // 2, 20),
                        wrapped_text,
                        font=font,
                        fill="white",
                        stroke_width=3,
                        stroke_fill="black",
                        anchor="ma",
                        align="center"
                    )

                    subtitle_clip = ImageClip(np.array(img)) \
                        .set_duration(audio.duration) \
                        .set_position(("center", "bottom"))

                    video = CompositeVideoClip([video, subtitle_clip])

            except Exception as e:
                print(f"⚠️ Subtitle failed (Pillow method): {e}")
            
            final_clips.append(video)
    
    if final_clips:
        final = concatenate_videoclips(final_clips)
        final.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
        return output_path
    return None

# Quick Test
if __name__ == "__main__":
    dummy_script = [{}, {}, {}]
    assemble_video("test_001", dummy_script)