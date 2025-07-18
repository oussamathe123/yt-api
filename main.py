
from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ API يعمل بنجاح!'

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    video_url = data.get('url')

    if not video_url:
        return jsonify({'error': 'يرجى إرسال رابط الفيديو'}), 400

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'format': 'bestvideo+bestaudio/best',
        'extract_flat': False
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get('formats', [])

            results = []
            for f in formats:
                if f.get('url') and f.get('filesize'):
                    results.append({
                        'ext': f.get('ext'),
                        'format_note': f.get('format_note'),
                        'resolution': f.get('resolution'),
                        'filesize_MB': round(f.get('filesize', 0) / 1024 / 1024, 2),
                        'url': f.get('url')
                    })

            return jsonify({
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'results': results
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
