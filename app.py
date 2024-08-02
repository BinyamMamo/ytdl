from flask import Flask, request, render_template_string, send_file, redirect, url_for, flash
import yt_dlp
import os
import logging

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# Basic HTML template
html_template = '''
<!doctype html>
<html lang="en">
  <head>
    <title>Download YouTube Video</title>
  </head>
  <body>
    <h1>Download YouTube Video</h1>
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        <ul class="flashes">
        {% for category, message in messages %}
          <li class="{{ category }}">{{ message }}</li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    <form method="post">
      <label for="url">YouTube URL:</label>
      <input type="text" id="url" name="url" required>
      <button type="submit">Download</button>
    </form>
    {% if video_path %}
      <h2>Download Successful!</h2>
      <a href="{{ url_for('download_file', filename=video_filename) }}">Download Video</a>
    {% endif %}
  </body>
</html>
'''

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_filename = ydl.prepare_filename(info_dict)
        return video_filename

@app.route('/', methods=['GET', 'POST'])
def index():
    video_path = None
    video_filename = None

    if request.method == 'POST':
        url = request.form['url']
        try:
            video_filename = download_video(url)
            video_path = os.path.abspath(video_filename)
            flash('Video downloaded successfully!', 'success')
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            flash(f"An error occurred: {str(e)}", 'error')
            return redirect(url_for('index'))

    return render_template_string(html_template, video_path=video_path, video_filename=video_filename)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(port=7120, debug=True)
