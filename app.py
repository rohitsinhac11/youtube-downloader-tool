
from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/api/download', methods=['POST'])
def download_info():
    data = request.get_json()
    video_url = data.get('url')
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        ydl_opts = {'quiet': True, 'skip_download': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = [{
                'format_id': f.get('format_id'),
                'resolution': f.get('format_note') or f.get('height', 'Unknown'),
                'url': f.get('url')
            } for f in info['formats'] if f.get('ext') == 'mp4' and f.get('url')]
            return jsonify({
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'formats': formats
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
