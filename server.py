from flask import Flask, render_template, request
from pytube import YouTube


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        url = request.form.get("search")
        video = YouTube(url)
        return render_template('videoCard.html',
                               title=video.title,
                               description=video.views,
                               thumbnail=video.thumbnail_url,
                               url=url)
    else:
        return "Video not found"


@app.route('/download', methods=["GET", "POST"])
def download():
    if request.method == "POST":
        url = request.form.get("video_url")
        try:
            video = YouTube(url)
            print('url:', url)
            # Get the stream with the lowest resolution (usually smallest file size)
            lowest_resolution_stream = video.streams.first()
            print('lowest_resolution_stream:', lowest_resolution_stream)
            if lowest_resolution_stream:
                lowest_resolution_stream.download()
                return "Video downloaded"
            else:
                return "No suitable stream found for download."
        except Exception as e:
            return f"Error: {str(e)}"
    else:
        return "Video not found"


if __name__ == "__main__":
    app.run(port=3400, debug=True)