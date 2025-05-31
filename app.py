
from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.form['url']
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        filename = stream.download()
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Error: {e}"

# Needed for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

