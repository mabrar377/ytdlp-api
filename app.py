from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
# This line is critical: it permits your PHP site to request data from Render safely
CORS(app) 

@app.route('/extract', methods=['POST'])
def extract_video():
    data = request.json
    video_url = data.get('url')

    if not video_url:
        return jsonify({'error': 'URL parameter missing'}), 400

    # Minimal configuration to parse info without downloading the file locally
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

            response_data = {
                'title': info.get('title', 'Unknown Title'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration_string', 'N/A'),
                'download_url': info.get('url') # Direct temporary stream CDN link
            }
            return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
