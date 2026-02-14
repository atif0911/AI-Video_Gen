import os
import threading
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from utils.script_generator import generate_script
from utils.voice_generator import create_audio_files
from utils.visual_fetcher import fetch_visuals
from utils.video_editor import assemble_video
from utils.seo_generator import generate_metadata
from utils.thumbnail_generator import create_thumbnail
from utils.youtube_uploader import upload_to_youtube

from models import db, VideoProject

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'dev_key_123')

db.init_app(app)

with app.app_context():
    db.create_all()
    print("✅ Database tables ready!")

import json

def run_pipeline(project_id, topic):
    with app.app_context():
        try:
            print(f"🚀 Starting/Resuming pipeline for Project {project_id}")
            project = VideoProject.query.get(project_id)
            base_dir = f"static/output/{project_id}"
            
            # Scripting
            if project.script_text:
                print("   ⏩ Script already exists in DB. Loading...")
                script_data = json.loads(project.script_text)
                # Seo data
                seo_data = generate_metadata(topic)
            else:
                project.status = "scripting"
                db.session.commit()
                
                seo_data = generate_metadata(topic)
                script_data = generate_script(topic)
                
                if not script_data:
                    raise Exception("Script generation failed.")
                
                # Save script to DB 
                project.script_text = json.dumps(script_data)
                db.session.commit()

            # TTS
            audio_dir = os.path.join(base_dir, "audio")
            if os.path.exists(audio_dir) and len(os.listdir(audio_dir)) > 0:
                print("   ⏩ Audio assets found. Skipping TTS...")
            else:
                project.status = "voiceover"
                db.session.commit()
                create_audio_files(script_data, project_id)

            # Visuals
            visuals_dir = os.path.join(base_dir, "visuals")
            if os.path.exists(visuals_dir) and len(os.listdir(visuals_dir)) > 0:
                print("   ⏩ Visual assets found. Skipping Pexels fetch...")
            else:
                project.status = "visuals"
                db.session.commit()
                fetch_visuals(script_data, project_id)

            # Rendering
            project.status = "rendering"
            db.session.commit()
            output_path = assemble_video(project_id, script_data)
            
            if not output_path:
                raise Exception("Video assembly failed.")

            # Thumbnail
            thumb_path = os.path.join(base_dir, "thumbnail.jpg")
            if not os.path.exists(thumb_path):
                print("   🖼️ Creating Thumbnail...")
                create_thumbnail(project_id, topic, seo_data.get('title', topic))
            
            # YouTube Upload Check
            if not project.youtube_link:
                print("   🚀 Attempting YouTube Upload...")
                youtube_link = upload_to_youtube(output_path, seo_data)
                if youtube_link:
                    project.youtube_link = youtube_link

            project.status = "completed"
            project.video_path = output_path
            db.session.commit()
            print(f"🏁 Project {project_id} finished successfully!")

        except Exception as e:
            print(f"❌ Pipeline Error for Project {project_id}: {str(e)}")
            project = VideoProject.query.get(project_id)
            project.status = "failed"
            db.session.commit()

@app.route('/')
def index():
    projects = VideoProject.query.order_by(VideoProject.created_at.desc()).all()
    return render_template('index.html', projects=projects)

@app.route('/create', methods=['POST'])
def create_video():
    data = request.json
    topic = data.get('topic')

    if not topic:
        return jsonify({'error': 'Topic is required'}), 400

    new_project = VideoProject(topic=topic, status="pending")
    db.session.add(new_project)
    db.session.commit()

    thread = threading.Thread(target=run_pipeline, args=(new_project.id, topic))
    thread.start()
    
    return jsonify({
        'message': 'Video generation started!', 
        'id': new_project.id
    })

@app.route('/status')
def get_all_status():
    projects = VideoProject.query.order_by(VideoProject.created_at.desc()).all()
    return jsonify([{
        'id': p.id,
        'topic': p.topic,
        'status': p.status,
        'video_path': p.video_path,
        'youtube_link': p.youtube_link
    } for p in projects])

@app.route('/watch/<int:project_id>')
def watch_video(project_id):
    project = VideoProject.query.get_or_404(project_id)
    if project.video_path:
        filename = project.video_path.split('static/output/')[1]
        return render_template('video_player.html', project=project, video_file=filename)
    return "Video not ready yet", 404

@app.route('/video/<path:filename>')
def serve_video(filename):
    return send_from_directory('static/output', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)