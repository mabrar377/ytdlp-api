from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app) 

@app.route('/extract', methods=['POST'])
def extract_video():
    data = request.json
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'URL parameter missing'}), 400

    # Path to the cookies file we uploaded
    cookies_path = os.path.join(os.path.dirname(__file__), 'cookies.txt')

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': cookies_path, # <-- CRITICAL NEW LINE
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            response_data = {
                'title': info.get('title', 'Unknown Title'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration_string', 'N/A'),
                'download_url': info.get('url') 
            }
            return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
